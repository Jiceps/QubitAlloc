#include "../include/node.hpp"


int main()
{

    // input size
    int m;
    std::cout << "\nSelect size (> 2): ";
    std::cin >> m;
    while (m < 3)
    {
        std::cout << "Select valid size (> 2): ";
        std::cin >> m;
    }


    // hyperparameter
    const int it_max = 10; //20;


    // linear coupling graph distance matrix
    vector<vector<int>> D = LinearCouplingDistanceMatrix(m);


    // random circuit interaction frequency matrix
    const int max_rd_circuit_size = 27;
    const string circuit_name = "rd_" + std::to_string(std::min(m, max_rd_circuit_size));
    const string interaction_mat_dir = "inter";
    const string interaction_matrix_path = interaction_mat_dir + "/" + circuit_name + ".csv";

    vector<vector<int>> F;
    int n = Load_interactionMatrix(F, interaction_matrix_path, m);
    //assert(n == m && "Error: invalid matrix sizes.");


    // root node initialization
    Solution sol;
    vector<int> map(n, -1);
    sol.mapping = map;
    sol.cost = -1;
    vector<int> available = Arange(m);
    CostMatrix CM = CostMatrix::Assemble(D, F, m);

    Node root_seq = Node{sol, 0, 0, CM, available};
    Node root_omp = Node{sol, 0, 0, CM, available};


    // runtime variables
    std::chrono::high_resolution_clock::time_point t0_seq, t1_seq, t0_omp, t1_omp;
    std::chrono::duration<double> delta_seq, delta_omp;
    double rt_seq, rt_omp, rt_dummy{0};


    //-------------------- bounding --------------------//

    int lb_seq, lb_omp;
    int min_cost = INF;
    int it;

    // sequential
    t0_seq = std::chrono::high_resolution_clock::now();

    lb_seq = root_seq.bound(it_max, min_cost, it, false, rt_dummy);

    t1_seq = std::chrono::high_resolution_clock::now();
    delta_seq = t1_seq - t0_seq;
    rt_seq = delta_seq.count();

    // OpenMP
    t0_omp = std::chrono::high_resolution_clock::now();

    lb_omp = root_omp.bound_OMP(it_max, min_cost, it, false, rt_dummy);

    t1_omp = std::chrono::high_resolution_clock::now();
    delta_omp = t1_omp - t0_omp;
    rt_omp = delta_omp.count();


    //std::cout << "\nlb_seq = " << lb_seq << "\n";
    //std::cout << "lb_omp = " << lb_omp << "\n";
    assert(lb_seq == lb_omp && "Error: Bounding failure.");
    
    
    // display
    std::cout << "\nsize = " << m << "\n";
    std::cout << "it_max = " << it_max << "\n";

    std::cout << "\nruntime seq: \t" << rt_seq << " s\n";
    std::cout << "speedup OMP: \t" << rt_seq / rt_omp << "\n";

    std::cout << std::endl;
    

    return 0;
}
