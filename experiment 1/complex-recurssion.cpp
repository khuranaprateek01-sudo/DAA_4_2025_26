/*Experiment 1:
Do the following:
        1.        Write the recurrence relation for the above function.
        2.        Using the Master Theorem, find the asymptotic time complexity and clearly state which case of the theorem is applied.
        3.        Modify the given code to:
        •        count the number of operations performed, and depth of the recursion tree
        •        measure the execution time (in milliseconds)
Print the number of operations and time taken for different input sizes
*/

#include <iostream>
#include <vector>
#include <chrono>
using namespace std;

long long countOps = 0;
int maxDepth = 0;

void complexRec(int n, int depth) {
    maxDepth = max(maxDepth, depth);

    if (n <= 2)
        return;

    int p = n;
    while (p > 0) {
        vector<int> temp(n);
        for (int i = 0; i < n; i++) {
            temp[i] = i ^ p;
            countOps++;
        }
        p >>= 1;
        countOps++;
    }

    vector<int> small(n);
    for (int i = 0; i < n; i++) {
        small[i] = i * i;
        countOps++;
    }

    for (int i = 0; i < n / 2; i++) {
        int t = small[i];
        small[i] = small[n - i - 1];
        small[n - i - 1] = t;
        countOps++;
    }

    complexRec(n / 2, depth + 1);
    complexRec(n / 2, depth + 1);
    complexRec(n / 2, depth + 1);
}

int main() {

    vector<int> inputs = {200};

    for (int n : inputs) {
        countOps = 0;
        maxDepth = 0;

        auto start = chrono::high_resolution_clock::now();
        complexRec(n, 1);
        auto end = chrono::high_resolution_clock::now();

        cout << "Input size: " << n << endl;
        cout << "Operations: " << countOps << endl;
        cout << "Max Recursion Depth: " << maxDepth << endl;

        auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
        cout << "Time (ms): " << duration.count() << endl;
    }

    return 0;
}

/*Recurrence relation is T(n)=3T(n/2) + (nlogn)*/
/*Complexity = O(n^1.585)*/