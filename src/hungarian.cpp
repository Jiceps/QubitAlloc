#include "../include/hungarian.hpp"


/**
 * Sets a = min(a, b)
 * @return true if b < a
 */
bool ckmin(int &a, const int &b) 
{ 
    return b < a ? (a = b, true) : false; 
}

/**
 * Hungarian algorithm implementation that modifies the input cost matrix and returns
 * the optimal assignment cost, while modifying the permutation vector.
 *
 * @param L A reference to a matrix of dimensions n×n such that L[w][j] is the cost
 *          of assigning the w-th worker to the j-th job (possibly negative).
 * @param n size of the input cost matrix L
 * @return The minimum assignment cost.
 */
int Hungarian (const vector<int>& L, int n)
{
    int w, j, w_cur, j_cur, j_next;

    const int inf = INF / 2;

    // job[j] = worker assigned to job j, or -1 if unassigned
    vector<int> job(n + 1, -1);

    // yw[w] is the potential for worker w
    // yj[j] is the potential for job j
    vector<int> yw(n, 0), yj(n + 1, 0);

    // main Hungarian algorithm
    for (w_cur = 0; w_cur < n; ++w_cur)
    {
        j_cur = n;
        job[j_cur] = w_cur;

        vector<int> min_to(n + 1, inf);
        vector<int> prv(n + 1, -1);
        vector<bool> in_Z(n + 1, false);

        while (job[j_cur] != -1)
        {
            in_Z[j_cur] = true;
            w = job[j_cur];
            int delta = inf;
            j_next = 0;

            for (j = 0; j < n; ++j)
            {
                if (!in_Z[j])
                {
                    // reduced cost = L[w][j] - yw[w] - yj[j]
                    int cur_cost = L[w*n + j] - yw[w] - yj[j];

                    if (ckmin(min_to[j], cur_cost))
                        prv[j] = j_cur;
                    if (ckmin(delta, min_to[j])) 
                        j_next = j;
                }
            }

            // update potentials
            for (j = 0; j <= n; ++j)
            {
                if (in_Z[j])
                {
                    yw[job[j]] += delta;
                    yj[j] -= delta;
                }
                else
                {
                    min_to[j] -= delta;
                }
            }

            j_cur = j_next;
        }

        // update worker assignment along the found augmenting path
        for (; j_cur != n; j_cur = j)
        {
            j = prv[j_cur];
            job[j_cur] = job[j];
        }
    }

    // compute total cost
    int total_cost = 0;

    // for j in [0..n-1], job[j] is the worker assigned to job j
    for (j = 0; j < n; ++j)
    {
        if (job[j] != -1)
            total_cost += L[job[j]*n + j];
    }

    return total_cost;
}
