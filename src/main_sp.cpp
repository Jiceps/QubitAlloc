#include "../include/node.hpp"
#include "../include/heuristics.hpp"
#include "../include/objective.hpp"

#include <boost/mpi.hpp>
#include <boost/serialization/vector.hpp>

namespace mpi = boost::mpi;


// ARGUMENTS:
// argv[1] = interaction matrix path
// argv[2] = distance matrix path
// argv[3] = it_max                     (optional, default: 10)


int main (int argc, char** argv)
{

    //----------------------------------- MPI initialization -----------------------------------//

    mpi::environment env;
    mpi::communicator world;
    int rank = world.rank();
    int nb_proc = world.size();

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
    int it_max = 10;

    // initialization variables
    vector<vector<int>> D, F;
    vector<int> priority;
    int n, m, min_cost;

    // tree exploration variables
    vector<vector<int>> optimal_solutions;
    Solution sol;
    vector<Node> Pool, children, shared_nodes, received_nodes;
    Node node;
    std::vector<char> work_flags(nb_proc), children_flags(nb_proc);
    char has_work, has_children;
    bool pruned, termination{false};
    int nb_nodes_to_share, lb, it;
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

    // tags
    const int TAG_SHARE_NODE = 10;


    //----------------------------------- Pool initialization (master) -----------------------------------//

    if (rank == 0)
    {
        std::cout << "\n...exploration\n" << std::endl;

        Node root = Node::Root(D, F, n, m);

        lb = root.bound_OMP(it_max, min_cost, it, true, rt_bound);

        children = root.decompose(priority, n, m, min_cost);

        for (Node node : children)
            Pool.push_back(node);
    }


    //----------------------------------- B & B tree exploration -----------------------------------//

    while (true)
    {
        //----- master checks for new solutions and prepares tasks to share -----//
        if (rank == 0)
        {
            nb_nodes_to_share = 0;

            work_flags.assign(nb_proc, 1);

            shared_nodes.clear();
            shared_nodes.reserve(nb_proc);

            while (!Pool.empty() && nb_nodes_to_share < nb_proc)
            {
                node = Pool.back();
                Pool.pop_back();

                ++ nb_nodes_visited;

                // manage leaf node
                if (node.isLeaf(n))
                {
                    const vector<int>& map = node.get_solution().mapping;
                    int cost = ObjectiveFunction(map, D, F, n);

                    if (cost < min_cost)
                    {
                        optimal_solutions = {map};
                        min_cost = cost;
                    }
                    else if (cost == min_cost)
                    {
                        optimal_solutions.push_back(map);
                    }
                }
                // prepare to send
                else
                {
                    ++ nb_nodes_to_share;

                    shared_nodes.push_back(node);
                }
            }

            // pad with dummy nodes if there is not enough work to send
            for (int i = nb_nodes_to_share; i < nb_proc; ++i)
            {
                work_flags[i] = 0;

                Node dummy;
                shared_nodes.push_back(dummy);
            }

            if (nb_nodes_to_share == 0)
            {
                termination = true;
            }
        }


        //----- check termination -----//
        mpi::broadcast(world, termination, 0);

        if (termination)
        {
            break;
        }


        //----- distribute tasks & minimal cost -----//
        mpi::scatter(world, work_flags, has_work, 0);
        mpi::scatter(world, shared_nodes, node, 0);
        mpi::broadcast(world, min_cost, 0);


        //----- bounding & pruning -----//
        pruned = false;

        if (has_work)
        {
            // bounding
            lb = node.bound_OMP(it_max, min_cost, it, true, rt_bound);

            // pruning
            if (lb > min_cost)
            {
                pruned = true;
            }
        }

        
        //----- decomposition -----//
        children.clear();

        if (has_work && !pruned)
        {
            children = node.decompose(priority, n, m, min_cost);
        }

        
        //----- send children to master & add them in the pool -----//
        has_children = has_work && !pruned && children.size() > 0;

        mpi::gather(world, has_children, children_flags, 0);

        if (rank == 0)
        {
            // receive worker's children
            for (int p = nb_proc - 1; p > 0; --p)
            {
                if (children_flags[p])
                {
                    world.recv(p, TAG_SHARE_NODE, received_nodes);

                    for (Node node : received_nodes)
                        Pool.push_back(node);
                }
            }

            // append master's children at the end
            for (Node node : children)
                Pool.push_back(node);
        }
        else
        {
            // send children to master
            if (has_children)
            {
                world.send(0, TAG_SHARE_NODE, children);
            }
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

        // results
        std::cout << "number of solutions = " << optimal_solutions.size() << "\n";
        assert(ValidSolutions(optimal_solutions, D, F, n, min_cost) && "Error: Invalid set of optimal solutions");
        std::cout << "cost = " << min_cost << "\n";

        // visited nodes
        std::cout << "\nnumber of visited nodes = " << nb_nodes_visited + 1 << "\n";
    
        // runtime
        std::cout << "\nruntime = " << rt << " s\n" << std::endl;
    }


    return 0;
}
