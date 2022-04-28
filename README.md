# vn-house-pricing

# Cấu trúc của dự án
- build_linux: Kết quả build app trên linux
- build_windows: Kết quả build app trên Windows
- Các file khác: Là source code của dự án

# Cách build ứng dụng này
1. Cài đặt Kivy và PyInstaller
2. Build trên linux
    - Tạo folder build_linux
    - Chạy script deploy.sh
3. Build trên Windows
    - Tạo folder build_windows
    - Chạy script deploy.bat

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