
//Sleeping_94 - 2026

#include <bits/stdc++.h>
using namespace std;

#define ll long long
#define ld long double
#define pii pair <int, int>
#define pli pair <ll, int>
#define pil pair <int, ll>
#define pll pair <ll, ll>
#define tii tuple <int, int, int>
#define fi first
#define se second
#define inf 0x3f

const ll nx = 1e6+2;
const ll bx = 1e3+2;
const ll mod = 1e9+7;

//--------------------------------
static void insertion_sort(vector <int> &a, int l, int r) {
    // TODO: Insertion sort tren a[l...r]
    for (int i = l + 1; i <= r; i++) {
        for (int j = i; j > l; j--) {
            if (a[j-1] > a[j]) swap(a[j-1], a[j]);
            else break;
        }
    }
}

// Tron hai mang con da sap xep: a[l...mid] va a[mid+1...r]
static void merge_ranges(vector <int> &a, vector <int> &mer, int l, int mid, int r) {
    // TODO: Copy a[l...r] sang mer, merge 2 nua da sap xep
    for (int i = l; i <= r; i++) {
        mer[i] = a[i];
    }

    int i = l, j = mid + 1;
    for (int k = l; k <= r; k++) {
        if (i > mid) a[k] = mer[j++];
        else if (j > r) a[k] = mer[i++];
        else if (mer[i] < mer[j]) a[k] = mer[i++];
        else a[k] = mer[j++];
    }
}

static void sort_rec(vector <int> &a, vector <int> &mer, int l, int r, int cutoff) {
    // TODO: base case, cutoff > 0 && len <= cutoff -> insertion sort
    if (l >= r) return;
    if (cutoff > 0 && r - l + 1 <= cutoff) {
        insertion_sort(a, l, r);
        return;
    }

    int mid = (l + r) >> 1;
    sort_rec(a, mer, l, mid, cutoff);
    sort_rec(a, mer, mid+1, r, cutoff);

    merge_ranges(a, mer, l, mid, r);
} 

void merge_sort(vector <int> &a, int cutoff) {
    if (cutoff < 0) throw invalid_argument("cutoff must be nonnegative");
    if (a.size() < 2) return;
    vector <int> mer(a.size());
    sort_rec(a, mer, 0, (int)(a.size() - 1), cutoff);
}
//--------------------------------
/*
Note:

*/