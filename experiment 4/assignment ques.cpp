#include <bits/stdc++.h>
#define MAX 100

using namespace std;

int heap[MAX];
int heapSize = 0;
int K;

void heapifyDown(int i) {
    int smallest = i;
    int left = 2*i + 1;
    int right = 2*i + 2;

    if (left < heapSize && heap[left] < heap[smallest])
        smallest = left;

    if (right < heapSize && heap[right] < heap[smallest])
        smallest = right;

    if (smallest != i) {
        swap(heap[smallest], heap[i]);
        heapifyDown(smallest);
    }
}

void heapifyUp(int i) {
    while (i > 0 && heap[(i-1)/2] > heap[i]) {
        swap(heap[i], heap[(i-1)/2]);
        i = (i-1)/2;
    }
}

void insert(int val) {
    heap[heapSize] = val;
    heapSize++;
    heapifyUp(heapSize - 1);
}

void processScore(int score) {
    if (heapSize < K) {
        insert(score);
    }
    else if (score > heap[0]) {
        heap[0] = score;
        heapifyDown(0);
    }

    if (heapSize < K)
        cout << -1 << endl;
    else
        cout << heap[0] << endl;
}

int main() {
    int N, score;

    cout << "K = ";
    cin >> K;

    cout << "N = ";
    cin >> N;

    cout << "Scores:\n";
    for (int i = 0; i < N; i++) {
        cin >> score;
        processScore(score);
    }

    return 0;
}
