import os
import sys

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.resources import resource_add_path, resource_find

Builder.load_file("predictscreen.kv")


class PredictScreen(BoxLayout):
    def predict_house_price(self):
        self.ids["predict_button"].text = "Dự đoán giá nhà là 1 triệu đồng"
        self.ids["predict_button"].background_color = "green"

    def clear_data(self):
        input_list = ["floor_input", "bedroom_input", "area_input", "length_input", "width_input"]
        for text_input in input_list:
            self.ids[text_input].text = ""

    def display_about_dialog(self):
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
