# vn-house-pricing

# Cấu trúc của dự án
- build_linux: Kết quả build app trên linux
- build_windows: Kết quả build app trên Windows
- Các file khác: Là source code của dự án

# Cách build ứng dụng này
1. Cài đặt Kivy và PyInstaller
2. Build trên linux
    - Tạo folder build_linux
    - Chạy các câu lệnh sau:
```shell
mkdir dist_linux
cd dist_linux
../venv/bin/python3 -m PyInstaller ../house-pricing.spec
```
3. Build trên Windows
    - Tạo folder build_windows
    - Chạy các câu lệnh sau
```shell
mkdir dist_windows
cd dist_windows
../venv/bin/python3 -m PyInstaller ../house-pricing.spec
```

# EDA Script
```python
# Đây là script để chạy d-tale: Đây là phần mềm giúp việc eda dữ liệu đơn giản hơn
# Trước khi chạy, anh cần cài dtale
# Sau đó anh copy đoạn code trong file này để dùng dtale để EDA - Sẽ dễ hơn.

import pandas
import dtale
df = pandas.read_csv("VN_housing_dataset.csv")
d = dtale.show(df)
d.open_browser()
```

# Slide thuyết trình và tiểu luận báo cáo:

Bao gồm các mục sau:
1. Xây dựng mô hình bằng autosklearn (tham khảo file autosklearn-notebook.ipynb)
   - Nhập dữ liệu từ file
   - Xử lý dữ liệu (Đặt lại tên cột, chuyển các giá trị từ string về float)
   - Đánh số ngẫu nhiên số tầng và tính chiều dài, chiều rộng của ngôi nhà
   - Xóa bỏ các giá trị bất thường
   - Chọn các cột thích hợp
   - Xóa bỏ các hàng có dữ liệu trống
   - Chia dataset thành tập train và test
   - One hot encode các cột dữ liệu định tính ở tập train.
   - Sử dụng auto-sklearn để xây dựng model
   - Sử dụng scikit-learn train lại model tốt nhất của autosklearn để đưa vào app
   - Test model và ghi kết quả
2. Xây dựng mô hình bằng autokeras (tham khảo file autokeras-notebook.ipynb)
   - Xử lý dữ liệu (Gần như trên)
   - Dùng AutoKeras để xây dựng model
3. Xây dựng ứng dụng.
   - Thư viện GUI sử dụng: Kivy
   - Giao diện của ứng dụng.
