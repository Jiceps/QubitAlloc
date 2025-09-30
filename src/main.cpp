#include "../include/node.hpp"
#include "../include/objective.hpp"


// ARGUMENTS:
// argv[1] = interaction matrix path
// argv[2] = distance matrix path


int main (int argc, char** argv)
{
    
    //----------------------------------- Parameterization -----------------------------------//

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
    vector<vector<int>> D;
    int m = Load_distanceMatrix(D, distance_matrix_path);

    // interaction matrix & logical qubits
    string interaction_matrix_path = argv[1];
    vector<vector<int>> F;
    int n = Load_interactionMatrix(F, interaction_matrix_path, m);

    // displays
    std::cout << "\nnumber of physical qubits = " << m << "\n";
    std::cout << "number of logical qubits = " << n << std::endl;


    //----------------------------------- Initialization -----------------------------------//

    // START TIMER //
    auto begin = std::chrono::high_resolution_clock::now();
    
    // prioritization queue of logical qubits
    vector<int> priority = Prioritization(F, n, m);

    // greedy heuristic allocation
    vector<int> map0;
    int min_cost = GreedyAllocation(D, F, priority, n, m, map0);

    // TEST //
    //std::cout << "\ngreedy = " << map0 << std::endl;
    //std::cout << "cost = " << min_cost << std::endl;
    //////////

    // variables
    vector<vector<int>> optimal_solutions;
    int num_visited = 0;



    //----------------------------------- B&B tree exploration -----------------------------------//

    std::cout << "\n...exploration\n" << std::endl;

    stack<Node> Pool;
    Pool.push(Node::Root(n, m));

    while (!Pool.empty())
    {
        // extract next node
        Node node = Pool.top();
        Pool.pop();

        ++ num_visited;

        // leaf node    
        if (node.isLeaf(n))
        {
            const vector<int>& map = node.get_mapping();
            int cost = Objective(map, D, F, n);

            if (cost < min_cost)
            {
                optimal_solutions = {map};
                min_cost = cost;
            }
            else if (cost == min_cost)
            {
                optimal_solutions.push_back(map);
            }

            continue;
        }
        
        // bounding
        int lb = node.bound_GLB(D, F, n, m);

        // pruning
        if (lb > min_cost)
        {
            continue;
        }

        // decomposition
        vector<Node> children = node.decompose(priority, n, m);

        // append in Pool
        for (Node node : children)
            Pool.push(node);
    }


    //----------------------------------- Termination -----------------------------------//

    // STOP TIMER //
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - begin;
    double rt = duration.count();

    // results display
    std::cout << "number of solutions = " << optimal_solutions.size() << "\n";

    assert(ValidSolutions(optimal_solutions, D, F, n, min_cost) && "Error: Invalid set of optimal solutions");
    std::cout << "cost = " << min_cost << std::endl;

    // visited nodes
    std::cout << "\nvisted nodes = " << num_visited << std::endl;

    // runtime 
    std::cout << "\nruntime = " << rt << " s\n" << std::endl;


    return 0;
}
