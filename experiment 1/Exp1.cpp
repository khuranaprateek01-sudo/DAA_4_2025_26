#include <iostream>
#include <chrono>
using namespace std;
using namespace chrono;

long long opCount = 0;
int maxDepth = 0;

void complexRec(int n, int depth) {
    maxDepth = max(maxDepth, depth);

    if (n <= 2) {
        return;
    }

    int p = n;
    while (p > 0) {
        vector<int> temp(n);
        for (int i = 0; i < n; i++) {
            temp[i] = i ^ p;
            opCount++;
        }
        p >>= 1;
        opCount++;
    }

    vector<int> small(n);
    for (int i = 0; i < n; i++) {
        small[i] = i * i;
        opCount++;
    }

    reverse(small.begin(), small.end());
    opCount += n;

    complexRec(n / 2, depth + 1);
    complexRec(n / 2, depth + 1);
    complexRec(n / 2, depth + 1);
}

int main() {
    vector<int> inputs = {100, 200, 400, 800};

    for (int n : inputs) {
        opCount = 0;
        maxDepth = 0;

        auto start = high_resolution_clock::now();
        complexRec(n, 1);
        auto end = high_resolution_clock::now();

        auto duration = duration_cast<milliseconds>(end - start);

        cout << "Input size: " << n << endl;
        cout << "Operations: " << opCount << endl;
        cout << "Recursion depth: " << maxDepth << endl;
        cout << "Time (ms): " << duration.count() << endl;
        cout << "--------------------------" << endl;
    }
    return 0;
}
/* Recurrence: T(n) = 3T(n/2) + O(n log n)
   By Master Theorem:
   T(n) = Θ(n^(log2 3)) ≈ Θ(n^1.585) */

