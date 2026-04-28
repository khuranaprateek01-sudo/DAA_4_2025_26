#include <iostream>
#include <vector>
#include <climits>
using namespace std;

int n;
vector<vector<int>> cost;
vector<vector<int>> dp;

int solve(int mask, int pos) {
    if (mask == (1 << n) - 1) {
        return cost[pos][0];
    }

    if (dp[mask][pos] != -1) return dp[mask][pos];

    int ans = INT_MAX;

    for (int city = 0; city < n; city++) {
        if ((mask & (1 << city)) == 0) {
            int newCost = cost[pos][city] + solve(mask | (1 << city), city);
            ans = min(ans, newCost);
        }
    }

    return dp[mask][pos] = ans;
}

int main() {
    cin >> n;

    cost.assign(n, vector<int>(n));

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> cost[i][j];
        }
    }

    dp.assign(1 << n, vector<int>(n, -1));

    cout << solve(1, 0);

    return 0;
}