# vn-house-pricing

# Cách build ứng dụng này
1. Cài đặt Kivy, scikit-learn và PyInstaller
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
