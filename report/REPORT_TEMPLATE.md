# Báo cáo: Tìm CUTOFF cho MergeSort

**Họ tên / MSSV:** [Điền]  
**Cấu hình CPU, RAM, OS:** [Điền]  
**Compiler, phiên bản, flags:** [Điền]

## 1. Mục tiêu
Tìm CUTOFF phù hợp trên máy cá nhân, so sánh giá trị 7 và 10 với MergeSort không có cutoff (0).

## 2. Cài đặt
Mô tả tự cài đặt theo bài giảng trang 7, 8 và 18. Chưa sử dụng các tối ưu khác ở trang 20-21 để cách ly ảnh hưởng cutoff.

## 3. Phương pháp
- Dữ liệu: random, ascending, descending, duplicates, n=1000/10000/100000/500000, seed cố định.
- CUTOFF: 0,2,4,6,7,8,10,12,14,16,20,24,28,32,40,48,64.
- Mỗi ca lặp 15 lần; warmup trước đo; trộn thứ tự cutoff; chỉ tính thời gian sort.
- Thống kê mean, median, standard deviation (ms); vẽ thời gian theo cutoff.

## 4. Kết quả THỰC ĐO
**Chưa có số liệu: chỉ điền sau khi chạy benchmark trên máy của mình.**

Chèn bảng `results/summary.csv`, biểu đồ `results/chart_*.png`, bảng `results/ranking.csv`.

## 5. Phân tích và kết luận
- Cutoff tối ưu theo từng kích thước/dạng dữ liệu?
- Cutoff 7 so với 10 có khác biệt đáng kể so với dao động đo không?
- Chọn cutoff theo median và mức ổn định; nêu rằng kết quả chỉ đúng cho máy/compiler/implementation này.
- Nhiễu: tiến trình nền, nhiệt độ CPU, thay đổi xung, caching.

## 6. Phụ lục
Link GitHub: [Điền]. Log chat AI: `chatlog/AI_USAGE.md`.
