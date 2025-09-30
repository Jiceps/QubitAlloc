#include "../include/node.hpp"
#include "../include/hungarian.hpp"


Node Node::Root (int n, int m)
{
    vector<int> mapping(n, -1);
    vector<bool> available(m, true);

    return Node{mapping, available, 0};
}


vector<Node> Node::decompose (const vector<int>& priority, int n, int m)
{
    vector<Node> children;

    vector<int> map = this->mapping;
    vector<bool>& av = this->available;
    const int dp = this->depth;

    // next logical qubit q_i to assign
    int i = priority[dp];

    // iterate over available physical qubits
    for (int j = m - 1; j >= 0; --j)
    {
        if (!av[j])
            continue; // skip if not available

        // assign q_i to P_j
        map[i] = j;
        av[j] = false;

        // insert in children vector
        children.push_back(Node{map, av, dp+1});

        // restore data
        map[i] = -1;
        av[j] = true;
    }

    return children;
}


// partial_mapping: -1 indicates unassigned, otherwise the location assigned (n = facilities, m = locations)
vector<int> Node::Assemble_LAP(const vector<vector<int>>& D, const vector<vector<int>>& F, int n, int m)
{
    vector<int> partial_mapping = this->mapping;
    vector<bool> av = this->available;

    // Identify assigned and unassigned facilities/locations
    vector<int> assigned_fac, unassigned_fac;
    vector<int> assigned_loc, unassigned_loc;

    for (int i = 0; i < n; ++i)
    {
        if (partial_mapping[i] != -1)
        {
            assigned_fac.push_back(i);
            assigned_loc.push_back(partial_mapping[i]);
        }
        else
            unassigned_fac.push_back(i);
    }
    for (int k = 0; k < m; ++k)
    {
        if (av[k])
            unassigned_loc.push_back(k); // true => available
    }

    int u = (int) unassigned_fac.size(); // number of unassigned facilities (rows)
    int r = (int) unassigned_loc.size(); // number available locations (columns)

    assert(u > 0 && r >= u && "Error: Bounding failure.");

    vector<int> L(r*r, 0); // reduced L-matrix (r x r)

    int val, min_val;

    // Build reduced L-matrix
    for (int i_idx = 0; i_idx < u; ++i_idx)
    {
        int i = unassigned_fac[i_idx];

        for (int k_idx = 0; k_idx < r; ++k_idx)
        {
            int k = unassigned_loc[k_idx];
            int cost = 0;

            // Interaction with other unassigned facilities
            for (int j_idx = 0; j_idx < u; ++j_idx)
            {
                int j = unassigned_fac[j_idx];

                if (i == j)
                    continue;

                min_val = INF;
                for (int l_idx = 0; l_idx < r; ++l_idx)
                {
                    if (k_idx == l_idx)
                        continue;

                    int l = unassigned_loc[l_idx];

                    val = F[i][j] * D[k][l];
                    if (val < min_val)
                        min_val = val; 
                }
                cost += min_val;
            }

            // Interaction with assigned facilities
            for (int a_idx = 0; a_idx < (int) assigned_fac.size(); ++a_idx)
            {
                int j = assigned_fac[a_idx];
                int l = partial_mapping[j];

                cost += F[i][j] * D[k][l];
            }

            L[i_idx*r + k_idx] = cost;
        }
    }

    return L;
}


int Node::bound_GLB (const vector<vector<int>>& D, const vector<vector<int>>& F, int n, int m)
{
    vector<int> partial_mapping = this->mapping;

    vector<int> L = Assemble_LAP(D, F, n, m);

    int fixed_cost = Objective(partial_mapping, D, F, n);

    int remaining_lb = Hungarian(L, m - this->depth);

    return fixed_cost + remaining_lb;
}
