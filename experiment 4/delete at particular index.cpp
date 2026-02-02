#include <bits/stdc++.h>
#define MAX 100
using namespace std;

int heap[MAX];
int heapSize = 0;

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
    if (heapSize == MAX) {
        cout << "heap full\n";
        return;
    }
    heap[heapSize] = val;
    heapSize++;
    heapifyUp(heapSize - 1);
}

void deleteAtIndex(int i) {
    if (i < 0 || i >= heapSize) {
        cout << "invalid index\n";
        return;
    }

    heap[i] = heap[heapSize - 1];
    heapSize--;

    if (i > 0 && heap[i] < heap[(i - 1) / 2])
        heapifyUp(i);
    else
        heapifyDown(i);
}

void printHeap() {
    for (int i = 0; i < heapSize; i++)
        cout << heap[i] << " ";
    cout << endl;
}

int main() {
    insert(2);
    insert(4);
    insert(6);
    insert(1);
    insert(8);

    cout << "Heap before deletion: ";
    printHeap();

    deleteAtIndex(2);

    cout << "Heap after deleting index 2: ";
    printHeap();

    return 0;
}
