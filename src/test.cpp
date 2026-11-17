
//Sleeping_94 - 2026

#include <bits/stdc++.h>
#include "mergesort_user.cpp"
using namespace std;

//--------------------------------
void merge_sort(vector <int> &a, int cutoff);
//--------------------------------
int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    // Validation
    int n; cin >> n;
    vector <int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    int cutoff; cin >> cutoff;
    merge_sort(a, cutoff);
    for (int i = 0; i < n; i++) {
        cout << a[i] << " ";
    }
}
/*
Note:

*/