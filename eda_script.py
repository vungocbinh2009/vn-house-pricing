# Đây là script để chạy d-tale: Đây là phần mềm giúp việc eda dữ liệu đơn giản hơn
# Trước khi chạy, anh cần cài dtale
import pandas
import dtale
import pprint

df = pandas.read_csv("VN_housing_dataset.csv")
unique_districts = df["Quận"].unique()
ward_by_district = {}
for district in unique_districts:
    district_data = df[df["Quận"] == district]
    ward_by_district[district] = district_data["Huyện"].unique()
pprint.pprint(ward_by_district)
d = dtale.show(df)
d.open_browser()


