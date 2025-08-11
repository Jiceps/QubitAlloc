#include "../include/node.hpp"
#include "../include/heuristics.hpp"
#include "../include/objective.hpp"

#include <boost/mpi.hpp>
#include <boost/serialization/vector.hpp>

namespace mpi = boost::mpi;


// ARGUMENTS:
// argv[1] = interaction matrix path
// argv[2] = distance matrix path
// argv[3] = it_max                     (optional, default: 5)

// example execution command: (2 nodes, 9 proc per node, 4 threads per proc)
// mpirun -machinefile \$OAR_NODEFILE -np 18 --map-by ppr:9:node:pe=2 -x OMP_NUM_THREADS=4 ./qapbb_mp inter/rd_14.csv dist/20_boeblingen.csv 3

int main (int argc, char** argv)
{

    //----------------------------------- MPI initialization -----------------------------------//

    mpi::environment env;
    mpi::communicator world;
    int rank = world.rank();
    int nb_proc = world.size();

    MPI_Comm raw_comm = world;

    // display process->node assignement
    if (nb_proc <= 64)
    {
        char hostname[256];
        gethostname(hostname, sizeof(hostname));
        std::cout << "Rank " << rank << " running on [" << hostname << "] and using " << omp_get_max_threads() << " threads" << std::endl;
    }
    else if (rank == 0)
    {
        std::cout << "\nnumber of processes = " << nb_proc << "\n";
        std::cout << "number of threads per process = " << omp_get_max_threads() << std::endl;
    }
    world.barrier();


    //----------------------------------- Variables -----------------------------------//

    // parameter
    int it_max = 5;

    // initialization variables
    vector<vector<int>> D, F;
    vector<int> priority;
    int n, m, min_cost;

    // tree exploration variables
    vector<vector<int>> optimal_solutions;
    Solution sol;
    std::vector<char> send_flags;
    vector<Node> Pool, initial_tasks, shared;
    int nb_init_task, lb, it;
    Node node;
    double nb_nodes_visited_loc{0};
    double nb_nodes_visited{0};

    // profiling variables
    std::chrono::high_resolution_clock::time_point begin, end;
    std::chrono::duration<double> duration;
    double rt, rt_bound{0};


    //----------------------------------- Initialization (master) -----------------------------------//

    if (rank == 0)
    {
        // assertion
        if (argc < 3)
        {
            std::cerr << "Error: two arguments are required\n";
            std::cerr << "(1): interaction matrix path\n";
            std::cerr << "(2): distance matrix path" << std::endl;
            exit(1);
        }

        // distance matrix & physical qubits
        string distance_matrix_path = argv[2];
        m = Load_distanceMatrix(D, distance_matrix_path);

        // interaction matrix & logical qubits
        string interaction_matrix_path = argv[1];
        n = Load_interactionMatrix(F, interaction_matrix_path, m);

        // maximal number of bounding iterations
        if (argc > 3)
        {
            it_max = std::stoi(argv[3]);
        }
        
        // displays
        std::cout << "\nnumber of physical qubits = " << m << "\n";
        std::cout << "number of logical qubits = " << n << std::endl;
        std::cout << "\nit_max = " << it_max << std::endl;

        // START TIMER //
        begin = std::chrono::high_resolution_clock::now();

        // prioritization queue of logical qubits
        priority = Prioritization(F, n, m);

        // greedy heuristic allocation
        vector<int> map0;
        min_cost = GreedyAllocation(D, F, priority, n, m, map0);
    }

    mpi::broadcast(world, m, 0);
    mpi::broadcast(world, n, 0);
    mpi::broadcast(world, priority, 0);
    mpi::broadcast(world, min_cost, 0);
    mpi::broadcast(world, D, 0);
    mpi::broadcast(world, F, 0);

    // tags
    const int TAG_WORK_SHARING = 10;
    const int TAG_SEND_SOLUTION = 20;


    //----------------------------------- Initial task distribution -----------------------------------//

    if (rank == 0)
    {
        std::cout << "\n...exploration\n" << std::endl;

        Node root = Node::Root(D, F, n, m);

        lb = root.bound_OMP(it_max, min_cost, it, true, rt_bound);

        initial_tasks = root.decompose(priority, n, m, min_cost);

        nb_init_task = initial_tasks.size();

    }

    mpi::broadcast(world, nb_init_task, 0);

    int nb_init_task_loc = nb_init_task / nb_proc + (rank < (nb_init_task % nb_proc));

    if (rank == 0)
    {
        for (int i = 0; i < nb_init_task; ++i)
        {
            int rank_dest = i % nb_proc;

            if (rank_dest == 0)
                Pool.push_back(initial_tasks[i]);
            else
                world.send(rank_dest, TAG_WORK_SHARING, initial_tasks[i]);
        }
    }
    else
    {
        Node task;

        for (int i = 0; i < nb_init_task_loc; ++i)
        {
            world.recv(0, TAG_WORK_SHARING, task);
            Pool.push_back(task);
        }
    }

    //----------------------------------- B & B tree exploration -----------------------------------//

    while (true)
    {
        //world.barrier();

        bool empty = Pool.empty();

        //----- extract next node -----//
        bool extracted_leaf = false;

        if (!empty)
        {
            node = Pool.back();
            Pool.pop_back();

            ++ nb_nodes_visited_loc;

            // evaluate leaf node
            if (node.isLeaf(n))
            {
                sol = node.get_solution();
                sol.cost = ObjectiveFunction(sol.mapping, D, F, n);

                extracted_leaf = true;
            }
        }

        //----- manage new solutions -----//
        char will_send = (extracted_leaf && sol.cost <= min_cost) ? 1 : 0;
        mpi::gather(world, will_send, send_flags, 0);

        // master receives solutions
        if (rank == 0)
        {
            for (int src = 1; src < nb_proc; ++src)
            {
                if (send_flags[src])
                {
                    Solution sol_recv;
                    world.recv(src, TAG_SEND_SOLUTION, sol_recv);

                    if (sol_recv.cost < min_cost)
                    {
                        min_cost = sol_recv.cost;
                        optimal_solutions.clear();
                        optimal_solutions.push_back(sol_recv.mapping);
                    }
                    else if (sol_recv.cost == min_cost)
                    {
                        optimal_solutions.push_back(sol_recv.mapping);
                    }
                }
            }

            // if master itself has a solution to add
            if (send_flags[0])
            {
                if (sol.cost < min_cost)
                {
                    min_cost = sol.cost;
                    optimal_solutions.clear();

                    optimal_solutions.push_back(sol.mapping);
                }
                else if (sol.cost == min_cost)
                {
                    optimal_solutions.push_back(sol.mapping);
                }
            }
        }
        // worker sends solution
        else
        {
            if (will_send)
            {
                world.send(0, TAG_SEND_SOLUTION, sol);
            }
        }


        /*
        bool will_send = extracted_leaf && sol.cost <= min_cost;

        if (rank != 0)
        {
            if (will_send)
            {
                // Worker sends its solution to master
                world.send(0, TAG_SEND_SOLUTION, sol);
            }
        }
        else
        {
            // Master processes its own solution if present
            if (will_send)
            {
                if (sol.cost < min_cost) {
                    min_cost = sol.cost;
                    optimal_solutions.clear();
                    optimal_solutions.push_back(sol.mapping);
                } else if (sol.cost == min_cost) {
                    optimal_solutions.push_back(sol.mapping);
                }
            }

            // Poll for incoming solutions
            int flag;
            MPI_Status status;
            do {

                MPI_Iprobe(MPI_ANY_SOURCE, TAG_SEND_SOLUTION, raw_comm, &flag, &status);

                if (flag)
                {
                    Solution sol_recv;
                    // Use Boost.MPI recv to deserialize the Solution
                    world.recv(status.MPI_SOURCE, TAG_SEND_SOLUTION, sol_recv);

                    if (sol_recv.cost < min_cost) {
                        min_cost = sol_recv.cost;
                        optimal_solutions.clear();
                        optimal_solutions.push_back(sol_recv.mapping);
                    } else if (sol_recv.cost == min_cost) {
                        optimal_solutions.push_back(sol_recv.mapping);
                    }
                }
            } while (flag); // process all messages currently in queue
        }*/

        // broadcast updated min_cost
        mpi::broadcast(world, min_cost, 0);


        //----- bounding & pruning -----//
        bool skip = empty || extracted_leaf;

        if (!skip)
        {
            // bounding
            lb = node.bound_OMP(it_max, min_cost, it, true, rt_bound);

            // bounding
            if (lb > min_cost)
            {
                skip = true;
            }
        }


        //----- decomposition -----//
        if (!skip)
        {
            vector<Node> children = node.decompose(priority, n, m, min_cost);

            // append in Pool
            for (Node node : children)
                Pool.push_back(node);
        }


        //----- work sharing -----//
        struct {
            int value;
            int rank;
        } local_minloc, global_minloc, local_maxloc, global_maxloc;

        int pool_size = Pool.size();

        // get lowest and highest local pool sizes
        local_minloc.value = pool_size;
        local_minloc.rank = rank;
        local_maxloc.value = pool_size;
        local_maxloc.rank = rank;

        MPI_Allreduce(&local_minloc, &global_minloc, 1, MPI_2INT, MPI_MINLOC, raw_comm);
        MPI_Allreduce(&local_maxloc, &global_maxloc, 1, MPI_2INT, MPI_MAXLOC, raw_comm);

        int min_pool_size = global_minloc.value;
        int min_pool_rank = global_minloc.rank;
        int max_pool_size = global_maxloc.value;
        int max_pool_rank = global_maxloc.rank;

        if (max_pool_size == 0)
        {
            if (rank == 0)
                std::cout << "terminated\n" << std::endl;
            
            break;
        }

        while (min_pool_size == 0 && max_pool_size > 1) // at least one pool empty and one pool able to share
        {
            if (rank == max_pool_rank)
            {
                auto begin = Pool.begin();
                auto mid   = Pool.begin() + pool_size / 2;

                // move half of Pool into shared
                shared.clear();
                shared.reserve(std::distance(begin, mid));
                std::move(begin, mid, std::back_inserter(shared));

                // send 'shared' to the empty pool rank
                world.send(min_pool_rank, TAG_WORK_SHARING, shared);

                // remove elements from Pool
                Pool.erase(begin, mid);

                pool_size = Pool.size();
            }

            if (rank == min_pool_rank)
            {
                // receive new tasks
                world.recv(max_pool_rank, TAG_WORK_SHARING, shared);

                // move received nodes into pool (avoiding copies)
                Pool.reserve(Pool.size() + shared.size());
                std::move(shared.begin(), shared.end(), std::back_inserter(Pool));
                shared.clear(); // optional

                pool_size = Pool.size();
            }

            pool_size = Pool.size();

            // get lowest and highest local pool sizes
            local_minloc.value = pool_size;
            local_minloc.rank  = rank;
            local_maxloc.value = pool_size;
            local_maxloc.rank  = rank;

            MPI_Allreduce(&local_minloc, &global_minloc, 1, MPI_2INT, MPI_MINLOC, raw_comm);
            MPI_Allreduce(&local_maxloc, &global_maxloc, 1, MPI_2INT, MPI_MAXLOC, raw_comm);

            min_pool_size = global_minloc.value;
            min_pool_rank = global_minloc.rank;
            max_pool_size = global_maxloc.value;
            max_pool_rank = global_maxloc.rank;
        }
    }


    //----------------------------------- Final displays (master) -----------------------------------//

    world.barrier();

    if (rank == 0)
    {
        // STOP TIMER //
        end = std::chrono::high_resolution_clock::now();
        duration = end - begin;
        rt = duration.count();
    }

    // master sums visited nodes
    mpi::reduce(world, nb_nodes_visited_loc, nb_nodes_visited, std::plus<double>(), 0);

    if (rank == 0)
    {
        // results
        std::cout << "number of solutions = " << optimal_solutions.size() << "\n";
        assert(ValidSolutions(optimal_solutions, D, F, n, min_cost) && "Error: Invalid set of optimal solutions");
        std::cout << "cost = " << min_cost << std::endl;

        // visited nodes
        std::cout << "\nnumber of visited nodes = " << nb_nodes_visited + 1 << "\n";

        // runtime
        std::cout << "\nruntime = " << rt << " s\n" << std::endl;
    }


    return 0;
}



// DUMP //
/*
while (min_pool_size == 0 && max_pool_size > 1) // at least one pool empty and one pool able to share
{
    if (rank == max_pool_rank)
    {
        auto begin = Pool.begin();
        auto mid = Pool.begin() + pool_size / 2;

        shared = vector<Node>(begin, mid);

        world.send(min_pool_rank, TAG_WORK_SHARING, shared);

        Pool.erase(begin, mid);

        pool_size = Pool.size();
    }

    if (rank == min_pool_rank)
    {
        world.recv(max_pool_rank, TAG_WORK_SHARING, shared);

        Pool.reserve(shared.size());
        Pool.insert(Pool.end(), shared.begin(), shared.end());
        pool_size = Pool.size();
    }

    pool_size = Pool.size();

    // get lowest and highest local pool sizes
    local_minloc.value = pool_size;
    local_minloc.rank = rank;
    local_maxloc.value = pool_size;
    local_maxloc.rank = rank;

    MPI_Allreduce(&local_minloc, &global_minloc, 1, MPI_2INT, MPI_MINLOC, raw_comm);
    MPI_Allreduce(&local_maxloc, &global_maxloc, 1, MPI_2INT, MPI_MAXLOC, raw_comm);
    
    min_pool_size = global_minloc.value;
    min_pool_rank = global_minloc.rank;
    max_pool_size = global_maxloc.value;
    max_pool_rank = global_maxloc.rank;
}*/
