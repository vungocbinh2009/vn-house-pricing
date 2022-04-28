# Đây là script để chạy d-tale: Đây là phần mềm giúp việc eda dữ liệu đơn giản hơn
# Trước khi chạy, anh cần cài dtale
# Sau đó anh copy đoạn code trong file này để dùng dtale để EDA - Sẽ dễ hơn.

import pandas
import dtale
df = pandas.read_csv("VN_housing_dataset.csv")
d = dtale.show(df)
d.open_browser()


