# Nhật ký sử dụng AI (AI Chat Log)

- **2026-11-17 (Giai đoạn chuẩn bị ban đầu — xem thêm `chatlog/AI_USAGE.md`):**
  - Sinh viên tự hoàn thiện 3 phần TODO trong `src/mergesort_user.cpp` theo slide `Tuan 5 Merge Sort.pdf` (trang 7, 8, 18).
  - AI hỗ trợ thiết kế khung benchmark (`src/benchmark.cpp`), sinh dữ liệu (`scripts/generate_data.py`), chạy thí nghiệm (`scripts/run_experiments.py`) và phân tích cơ bản (`scripts/analyze.py`).

- **2026-11-17 (Phiên thực nghiệm & báo cáo với Antigravity):**
  - Hỗ trợ viết `src/test.cpp` gọi hàm `merge_sort` từ `src/mergesort_user.cpp`.
  - Kiểm tra cấu hình máy thực tế (`results/machine.txt`) và kiểm thử tính đúng đắn với `-D_GLIBCXX_DEBUG`; phát hiện lỗi biên `j >= l` (truy cập `a[-1]`) ở `insertion_sort` và xung đột `int main()` trong `src/mergesort_user.cpp`. Sau khi sinh viên xác nhận và chỉnh sửa, toàn bộ kiểm thử đã vượt qua (`ALL_TESTS_PASSED`).
  - Biên dịch `benchmark.exe` với `-std=c++17 -O2 -DNDEBUG` và chạy đủ 4,080 lượt đo thực tế trên máy Windows 11 của sinh viên.
  - Bổ sung `scripts/full_analysis.py` để tính đầy đủ `min`, `max`, `stdev`, `CV%`, `Speedup`, `geometric mean` và vẽ 5 biểu đồ báo cáo tại `results/charts/`.
  - Hoàn thiện báo cáo `report/report.md`, `README.md` và `requirements.txt` dựa hoàn toàn trên số liệu thực đo.
