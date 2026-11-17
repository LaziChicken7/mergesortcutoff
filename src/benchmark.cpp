#include <bits/stdc++.h>
using namespace std;

void merge_sort(vector<int>& a, int cutoff);

int main(int argc, char** argv) {
    if (argc != 5) {
        cerr << "Usage: benchmark INPUT TRIALS OUTPUT SEED\n";
        return 1;
    }

    try {
        ifstream in(argv[1]);
        if (!in) {
            throw runtime_error("missing data");
        }

        int n;
        in >> n;
        if (n < 0) {
            throw runtime_error("bad n");
        }

        vector<int> orig(n);
        for (int& x : orig) {
            if (!(in >> x)) {
                throw runtime_error("bad input");
            }
        }

        ofstream out(argv[3]);
        if (!out) {
            throw runtime_error("cannot open output");
        }

        out << "input,cutoff,trial,time_ns\n";

        int trials = stoi(argv[2]);
        if (trials < 1) {
            throw runtime_error("bad trials");
        }

        vector<int> cutoffs = {0, 2, 4, 6, 7, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40, 48, 64};
        mt19937 rng(stoul(argv[4]));

        for (int c : cutoffs) {
            auto a = orig;
            merge_sort(a, c);
            if (!is_sorted(a.begin(), a.end())) {
                throw runtime_error("bad sort warmup");
            }
        }

        for (int t = 1; t <= trials; t++) {
            shuffle(cutoffs.begin(), cutoffs.end(), rng);

            for (int c : cutoffs) {
                auto a = orig; // Copy ngoai vung do thoi gian

                auto start = chrono::steady_clock::now();
                merge_sort(a, c);
                auto stop = chrono::steady_clock::now();

                if (!is_sorted(a.begin(), a.end())) {
                    throw runtime_error("bad sort cutoff=" + to_string(c));
                }

                auto elapsed = chrono::duration_cast<chrono::nanoseconds>(stop - start).count();
                out << argv[1] << "," << c << "," << t << "," << elapsed << "\n";
            }
        }

        cerr << "Finished " << argv[1] << "\n";
    } catch (exception const& e) {
        cerr << "ERROR: " << e.what() << "\n";
        return 2;
    }
}
