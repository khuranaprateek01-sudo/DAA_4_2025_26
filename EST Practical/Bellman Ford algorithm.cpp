#include <iostream>
#include <vector>
using namespace std;

int main() {
    int V, E;
    cin >> V >> E;

    vector<vector<int>> edges(E, vector<int>(3));

    for(int i = 0; i < E; i++) {
        cin >> edges[i][0] >> edges[i][1] >> edges[i][2];
    }

    int src;
    cin >> src;

    vector<int> dist(V, 100000000);
    dist[src] = 0;

    for(int i = 0; i < V - 1; i++) {
        for(int j = 0; j < E; j++) {
            int u = edges[j][0];
            int v = edges[j][1];
            int w = edges[j][2];

            if(dist[u] != 100000000 && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }

    for(int j = 0; j < E; j++) {
        int u = edges[j][0];
        int v = edges[j][1];
        int w = edges[j][2];

        if(dist[u] != 100000000 && dist[u] + w < dist[v]) {
            cout << -1;
            return 0;
        }
    }

    for(int i = 0; i < V; i++) {
        cout << dist[i] << " ";
    }

    return 0;
}