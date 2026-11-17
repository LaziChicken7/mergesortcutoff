# MergeSort CUTOFF — Experimental Benchmark & Analysis

Nghiên cứu thực nghiệm tìm giá trị `CUTOFF` tối ưu (chuyển sang Insertion Sort cho mảng con nhỏ) trong thuật toán MergeSort dựa trên giáo trình *Algorithms, 4th Edition* (`Tuan 5 Merge Sort.pdf`, trang 7, 8, 18, 22).

## Cấu trúc thư mục

- `src/mergesort_user.cpp`: Cài đặt MergeSort + CUTOFF của sinh viên.
- `src/benchmark.cpp`: Chương trình benchmark C++ (warm-up, xáo trộn thứ tự CUTOFF, đo bằng `steady_clock`, kiểm tra `is_sorted`).
- `src/test.cpp`: Chương trình kiểm thử đơn giản qua stdin/stdout.
- `scripts/generate_data.py`: Sinh 16 bộ dữ liệu (`random`, `ascending`, `descending`, `duplicates` với $N \in \{1000, 10000, 100000, 500000\}$, seed cố định `20261117 + n`).
- `scripts/run_experiments.py`: Chạy benchmark qua tất cả bộ dữ liệu và gom kết quả vào `results/all_runs.csv`.
- `scripts/analyze.py` & `scripts/full_analysis.py`: Thống kê (`mean`, `median`, `stdev`, `min`, `max`, `speedup`, `geometric mean`) và vẽ biểu đồ.
- `results/`: Chứa `machine.txt`, `all_runs.csv`, `summary.csv`, `detailed_summary.csv`, `ranking.csv`, `detailed_ranking.csv` và `results/charts/*.png`.
- `report/report.md`: Báo cáo thí nghiệm hoàn chỉnh bằng tiếng Việt.
- `docs/ai_chat_log.md` & `chatlog/AI_USAGE.md`: Nhật ký sử dụng AI.

## Hướng dẫn tái lập thí nghiệm (Windows PowerShell)

### 1. Cài đặt môi trường
Yêu cầu `g++` (C++17) và Python 3.10+. Cài đặt các thư viện Python:
```powershell
python -m pip install -r requirements.txt
```

### 2. Biên dịch C++
```powershell
g++ -std=c++17 -O2 -DNDEBUG src/benchmark.cpp src/mergesort_user.cpp -o benchmark.exe
```

### 3. Tạo bộ dữ liệu
```powershell
python scripts/generate_data.py
```

### 4. Chạy benchmark (15 lần lặp mỗi cấu hình + warm-up)
```powershell
python scripts/run_experiments.py --exe ./benchmark.exe --trials 15
```

### 5. Sinh bảng thống kê và biểu đồ
```powershell
python scripts/analyze.py
python scripts/full_analysis.py
```

### 6. Đọc kết quả
- Cấu hình máy: `results/machine.txt`
- Dữ liệu đo thô (4,080 lượt): `results/all_runs.csv`
- Bảng thống kê & xếp hạng: `results/detailed_summary.csv`, `results/detailed_ranking.csv`
- Biểu đồ: `results/charts/chart1_cutoff_vs_mean_time.png` đến `chart5_variability_boxplot.png`
- Báo cáo đầy đủ: `report/report.md`

## Tóm tắt kết quả chính (trên Intel Core Ultra 9 185H, Win11, g++ 15.2.0 `-O2`)
- **CUTOFF = 16** đạt speedup trung bình nhân cao nhất (**1.467x** so với `CUTOFF = 0`), theo sát là **CUTOFF = 12** (**1.453x**, độ ổn định cao hơn với CV 11.41%).
- **CUTOFF = 10** (**1.424x**) nhanh hơn **CUTOFF = 7** (**1.361x**) khoảng 4.6% trên tổng thể, nhưng trên mảng lớn ngẫu nhiên/giảm dần ($N = 500,000$) mức chênh lệch nhỏ hơn độ biến động đo.
