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
1. Xây dựng mô hình bằng autosklearn và autokeras
   - Nhập dữ liệu từ file
   - Xử lý dữ liệu
     + Đặt lại tên các cột
     + Xóa bỏ các hàng không phù hợp
     + Chuyển một số cột về dạng numeric
   - Đánh số ngẫu nhiên số tầng và tính chiều dài, chiều rộng của ngôi nhà
   - Xóa bỏ các giá trị bất thường
     + Xóa bỏ các hàng có giá nhà quá cao hoặc quá thấp
     + Xóa bỏ các hàng có diện tích nhà khác xa với tích giữa chiều dài và chiều rộng.
     + Xóa bỏ các hàng không có thông tin về giấy tờ pháp lý
   - Chọn các cột thích hợp để xây dựng mô hình
   - Xóa bỏ các hàng có dữ liệu trống
   - Chia dataset thành tập train và test
   - One hot encode các cột dữ liệu định tính ở tập train (đối với autosklearn)
   - Sử dụng auto-sklearn và autokeras để xây dựng model
   - Kiểm tra mô hình bằng test data
3. Xây dựng ứng dụng.
   - Thư viện GUI sử dụng: Kivy
   - Giao diện của ứng dụng.
   - Đóng gói ứng dụng bằng PyInstaller
