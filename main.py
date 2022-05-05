import os
import sys
import pickle

import pandas as pd
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.resources import resource_add_path
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.svm import SVR

Builder.load_file("predictscreen.kv")


class PredictScreen(BoxLayout):
    districts = [
        "Quận Đống Đa", "Quận Thanh Xuân", "Quận Hoàng Mai", "Quận Hai Bà Trưng",
        "Quận Hà Đông", "Quận Cầu Giấy", "Quận Ba Đình", "Quận Long Biên", "Quận Nam Từ Liêm",
        "Quận Tây Hồ", "Quận Bắc Từ Liêm", "Huyện Thanh Trì", "Quận Hoàn Kiếm",
        "Huyện Hoài Đức", "Huyện Gia Lâm", "Huyện Đông Anh", "Huyện Thanh Oai", "Huyện Sóc Sơn",
        "Huyện Quốc Oai", "Huyện Đan Phượng", "Huyện Chương Mỹ", "Thị xã Sơn Tây", "Huyện Thường Tín",
        "Huyện Thạch Thất", "Huyện Mê Linh", "Huyện Ba Vì", "Huyện Phúc Thọ", "Huyện Mỹ Đức",
        "Huyện Phú Xuyên"
    ]

    ward_by_district = {
        'Huyện Ba Vì': ['Xã Phú Châu', 'Xã Vân Hòa', 'Xã Phú Sơn'],
        'Huyện Chương Mỹ': ['Thị trấn Chúc Sơn', 'Xã Phụng Châu', 'Xã Đại Yên', 'Xã Thủy Xuân Tiên', 'Xã Hoàng Văn Thụ',
                            'Thị trấn Xuân Mai'],
        'Huyện Gia Lâm': ['Xã Cổ Bi', 'Xã Kiêu Kỵ', 'Xã Đặng Xá', 'Xã Đông Dư', 'Thị trấn Trâu Quỳ', 'Xã Yên Thường',
                          'Thị trấn Yên Viên', 'Xã Đa Tốn', 'Xã Dương Quang', 'Xã Bát Tràng', 'Xã Ninh Hiệp',
                          'Xã Kim Sơn', 'Xã Dương Xá', 'Xã Yên Viên', 'Xã Đình Xuyên', 'Xã Phù Đổng'],
        'Huyện Hoài Đức': ['Xã Kim Chung', 'Xã Vân Canh', 'Xã La Phù', 'Thị trấn Trạm Trôi', 'Xã Đông La',
                           'Xã Di Trạch', 'Xã An Thượng', 'Xã An Khánh', 'Xã Lại Yên', 'Xã Vân Côn',
                           'Xã Minh Khai', 'Xã Sơn Đồng', 'Xã Dương Liễu', 'Xã Đức Thượng', 'Xã Đức Giang',
                           'Xã Song Phương'],
        'Huyện Mê Linh': ['Thị trấn Quang Minh', 'Xã Đại Thịnh', 'Xã Tam Đồng', 'Xã Kim Hoa', 'Xã Tiền Phong',
                          'Xã Mê Linh'],
        'Huyện Mỹ Đức': ['Xã Hợp Thanh'],
        'Huyện Phú Xuyên': ['Thị trấn Phú Xuyên'],
        'Huyện Phúc Thọ': ['Xã Võng Xuyên', 'Xã Ngọc Tảo'],
        'Huyện Quốc Oai': ['Thị trấn Quốc Oai', 'Xã Phú Mãn', 'Xã Đông Yên', 'Xã Ngọc Liệp', 'Xã Sài Sơn', 'Xã Phú Cát',
                           'Xã Nghĩa Hương', 'Xã Đồng Quang', 'Xã Đại Thành', 'Xã Hòa Thạch'],
        'Huyện Sóc Sơn': ['Xã Phù Lỗ', 'Xã Phú Cường', 'Xã Minh Phú', 'Xã Xuân Giang', 'Xã Tiên Dược', 'Xã Mai Đình',
                          'Xã Đông Xuân', 'Xã Quang Tiến', 'Xã Phù Linh', 'Xã Phú Minh', 'Xã Minh Trí', 'Xã Thanh Xuân',
                          'Thị trấn Sóc Sơn'],
        'Huyện Thanh Oai': ['Xã Cự Khê', 'Xã Bích Hòa', 'Thị trấn Kim Bài', 'Xã Tam Hưng', 'Xã Phương Trung',
                            'Xã Thanh Cao', 'Xã Đỗ Động'],
        'Huyện Thanh Trì': ['Thị trấn Văn Điển', 'Xã Tả Thanh Oai', 'Xã Tam Hiệp', 'Xã Tứ Hiệp', 'Xã Tân Triều',
                            'Xã Hữu Hoà', 'Xã Ngọc Hồi', 'Xã Thanh Liệt', 'Xã Vĩnh Quỳnh', 'Xã Liên Ninh', 'Xã Đông Mỹ',
                            'Xã Ngũ Hiệp', 'Xã Duyên Hà', 'Xã Vạn Phúc', 'Xã Đại áng'],
        'Huyện Thường Tín': ['Xã Nghiêm Xuyên', 'Xã Khánh Hà', 'Thị trấn Thường Tín', 'Xã Hà Hồi', 'Xã Nhị Khê',
                             'Xã Ninh Sở', 'Xã Duyên Thái', 'Xã Văn Bình', 'Xã Lê Lợi', 'Xã Vân Tảo'],
        'Huyện Thạch Thất': ['Xã Bình Yên', 'Xã Hương Ngải', 'Xã Thạch Hoà', 'Xã Tân Xã', 'Xã Bình Phú', 'Xã Tiến Xuân',
                             'Thị trấn Liên Quan'],
        'Huyện Đan Phượng': ['Thị trấn Phùng', 'Xã Tân Lập', 'Xã Thượng Mỗ', 'Xã Tân Hội', 'Xã Đan Phượng',
                             'Xã Phương Đình'],
        'Huyện Đông Anh': ['Xã Kim Chung', 'Xã Đông Hội', 'Xã Võng La', 'Xã Bắc Hồng', 'Xã Hải Bối', 'Xã Kim Nỗ',
                           'Thị trấn Đông Anh', 'Xã Vân Nội', 'Xã Nam Hồng', 'Xã Nguyên Khê', 'Xã Uy Nỗ',
                           'Xã Vĩnh Ngọc', 'Xã Đại Mạch', 'Xã Xuân Nộn', 'Xã Việt Hùng', 'Xã Mai Lâm', 'Xã Dục Tú',
                           'Xã Tiên Dương'],
        'Quận Ba Đình': ['Phường Ngọc Khánh', 'Phường Cống Vị', 'Phường Vĩnh Phúc', 'Phường Trúc Bạch',
                         'Phường Ngọc Hà', 'Phường Liễu Giai', 'Phường Kim Mã', 'Phường Đội Cấn', 'Phường Thành Công',
                         'Phường Giảng Võ', 'Phường Phúc Xá', 'Phường Quán Thánh', 'Phường Điện Biên',
                         'Phường Nguyễn Trung Trực'],
        'Quận Bắc Từ Liêm': ['Phường Cổ Nhuế 1', 'Phường Xuân Đỉnh', 'Phường Phúc Diễn', 'Phường Minh Khai',
                             'Phường Phú Diễn', 'Phường Đông Ngạc', 'Phường Cổ Nhuế 2', 'Phường Thượng Cát',
                             'Phường Liên Mạc', 'Phường Xuân Tảo', 'Phường Thụy Phương', 'Phường Đức Thắng',
                             'Phường Tây Tựu'],
        'Quận Cầu Giấy': ['Phường Nghĩa Đô', 'Phường Yên Hoà', 'Phường Quan Hoa', 'Phường Mai Dịch', 'Phường Trung Hoà',
                          'Phường Dịch Vọng Hậu', 'Phường Nghĩa Tân', 'Phường Dịch Vọng'],
        'Quận Hai Bà Trưng': ['Phường Minh Khai', 'Phường Đống Mác', 'Phường Thanh Lương', 'Phường Bách Khoa',
                              'Phường Trương Định', 'Phường Cầu Dền', 'Phường Bạch Đằng', 'Phường Thanh Nhàn',
                              'Phường Quỳnh Mai', 'Phường Vĩnh Tuy', 'Phường Bạch Mai', 'Phường Phố Huế',
                              'Phường Đồng Tâm', 'Phường Phạm Đình Hổ', 'Phường Lê Đại Hành', 'Phường Quỳnh Lôi',
                              'Phường Đồng Nhân', 'Phường Ngô Thì Nhậm', 'Phường Bùi Thị Xuân', 'Phường Nguyễn Du'],
        'Quận Hoàn Kiếm': ['Phường Phúc Tân', 'Phường Cửa Đông', 'Phường Chương Dương', 'Phường Hàng Bông',
                           'Phường Phan Chu Trinh', 'Phường Cửa Nam', 'Phường Hàng Bồ', 'Phường Trần Hưng Đạo',
                           'Phường Hàng Bài', 'Phường Tràng Tiền', 'Phường Hàng Bạc', 'Phường Hàng Đào',
                           'Phường Đồng Xuân', 'Phường Lý Thái Tổ', 'Phường Hàng Buồm', 'Phường Hàng Trống',
                           'Phường Hàng Mã', 'Phường Hàng Gai'],
        'Quận Hoàng Mai': ['Phường Định Công', 'Phường Tương Mai', 'Phường Đại Kim', 'Phường Mai Động',
                           'Phường Hoàng Văn Thụ', 'Phường Lĩnh Nam', 'Phường Tân Mai', 'Phường Hoàng Liệt',
                           'Phường Thịnh Liệt', 'Phường Vĩnh Hưng', 'Phường Giáp Bát', 'Phường Thanh Trì',
                           'Phường Trần Phú', 'Phường Yên Sở'],
        'Quận Hà Đông': ['Phường Văn Quán', 'Phường Quang Trung', 'Phường La Khê', 'Phường Kiến Hưng',
                         'Phường Vạn Phúc', 'Phường Phú Lương', 'Phường Phú La', 'Phường Hà Cầu', 'Phường Yên Nghĩa',
                         'Phường Nguyễn Trãi', 'Phường Dương Nội', 'Phường Mộ Lao', 'Phường Phú Lãm',
                         'Phường Biên Giang', 'Phường Yết Kiêu', 'Phường Phúc La', 'Phường Đồng Mai'],
        'Quận Long Biên': ['Phường Bồ Đề', 'Phường Gia Thụy', 'Phường Đức Giang', 'Phường Long Biên',
                           'Phường Thạch Bàn', 'Phường Ngọc Thụy', 'Phường Cự Khối', 'Phường Thượng Thanh',
                           'Phường Ngọc Lâm', 'Phường Việt Hưng', 'Phường Giang Biên', 'Phường Phúc Đồng',
                           'Phường Sài Đồng', 'Phường Phúc Lợi'],
        'Quận Nam Từ Liêm': ['Phường Phương Canh', 'Phường Mễ Trì', 'Phường Tây Mỗ', 'Phường Đại Mỗ',
                             'Phường Mỹ Đình 1', 'Phường Mỹ Đình 2', 'Phường Phú Đô', 'Phường Cầu Diễn',
                             'Phường Trung Văn', 'Phường Xuân Phương'],
        'Quận Thanh Xuân': ['Phường Kim Giang', 'Phường Khương Trung', 'Phường Khương Đình', 'Phường Khương Mai',
                            'Phường Nhân Chính', 'Phường Thượng Đình', 'Phường Phương Liệt', 'Phường Thanh Xuân Bắc',
                            'Phường Hạ Đình', 'Phường Thanh Xuân Nam', 'Phường Thanh Xuân Trung'],
        'Quận Tây Hồ': ['Phường Thụy Khuê', 'Phường Xuân La', 'Phường Bưởi', 'Phường Quảng An', 'Phường Phú Thượng',
                        'Phường Nhật Tân', 'Phường Yên Phụ', 'Phường Tứ Liên'],
        'Quận Đống Đa': ['Phường Trung Liệt', 'Phường Láng Hạ', 'Phường Trung Tự', 'Phường Ô Chợ Dừa',
                         'Phường Kim Liên', 'Phường Trung Phụng', 'Phường Ngã Tư Sở', 'Phường Quốc Tử Giám',
                         'Phường Khâm Thiên', 'Phường Láng Thượng', 'Phường Thịnh Quang', 'Phường Nam Đồng',
                         'Phường Quang Trung', 'Phường Phương Mai', 'Phường Thổ Quan', 'Phường Khương Thượng',
                         'Phường Hàng Bột', 'Phường Cát Linh', 'Phường Văn Chương', 'Phường Phương Liên',
                         'Phường Văn Miếu'],
        'Thị xã Sơn Tây': ['Phường Ngô Quyền', 'Phường Phú Thịnh', 'Xã Cổ Đông', 'Phường Viên Sơn',
                           'Phường Trung Sơn Trầm', 'Xã Sơn Đông', 'Phường Xuân Khanh', 'Xã Kim Sơn']
    }

    def update_ward_list(self, text):
        self.ids["ward_spinner"].values = self.ward_by_district[text]
        self.ids["ward_spinner"].text = self.ward_by_district[text][0]

    def display_predict_value(self):
        predict_value = self.predict_price()
        self.ids["predict_button"].text = f"Dự đoán giá nhà là {predict_value: .2f} triệu đồng"
        self.ids["predict_button"].background_color = "green"

    def predict_price(self) -> float:
        with open('final-model.pickle', 'rb') as f:
            model: SVR = pickle.load(f)
        # predict
        ohe = OneHotEncoder(handle_unknown='ignore')
        df = pd.read_csv("train_data.csv")
        x_train = df.drop(["index", "price"], axis=1)
        # ohe.fit(x_train)
        preprocessor = ColumnTransformer([
            ("ohe", ohe, ["district", "ward", "type_of_housing", "legal_paper"]),
        ])
        preprocessor.fit(x_train)

        pipe = Pipeline([
            ("preprocess", preprocessor)
        ])
        input_df = pd.DataFrame(data={
            "district": self.ids["district_spinner"].text,
            "ward": self.ids["ward_spinner"].text,
            "type_of_housing": self.ids["type_of_housing_spinner"].text,
            "legal_paper": self.ids["legal_paper_spinner"].text
        }, index=[0])
        transform_input_data = pipe.transform(input_df)
        return model.predict(transform_input_data)[0]

    def update_predict_button_state(self):
        self.ids["predict_button"].disabled = False
        self.ids["predict_button"].background_color = "blue"
        self.ids["predict_button"].text = "Dự đoán giá nhà"

    @staticmethod
    def display_about_dialog():
        button = Button(text="Close")
        button.size_hint = [1, 0.1]
        label = Label(text="""
            Tên ứng dụng: Ứng dụng dự đoán giá nhà.
            Phiên bản: 1.0.
            Tác giả: Vũ Ngọc Đại & Vũ Ngọc Bình.
            Bài tập môn: Phát triển phần mềm nâng cao cho tính toán khoa học.
        """)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(label)
        layout.add_widget(button)
        popup = Popup(
            title='Về ứng dụng này',
            content=layout,
        )
        button.bind(on_press=popup.dismiss)
        popup.open()


class MyApp(App):
    def build(self):
        self.title = 'Ứng dụng dự đoán giá nhà'
        return PredictScreen()


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    MyApp().run()
