from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class CalculatorApp(App):
    def build(self):
        self.expression = ""
        self.previous_result = None
        main_layout = BoxLayout(orientation='vertical', spacing=10)
        self.display = Button(text="0", font_size=50, size_hint=(1, 0.75))
        main_layout.add_widget(self.display)

        buttons_layout = GridLayout(cols=4, spacing=10, size_hint=(1, 2))
        buttons = [
            ('7', self.append_to_display), ('8', self.append_to_display), ('9', self.append_to_display), ('/',
                                                                                                             self.append_to_display),
            ('4', self.append_to_display), ('5', self.append_to_display), ('6', self.append_to_display), ('*',
                                                                                                             self.append_to_display),
            ('1', self.append_to_display), ('2', self.append_to_display), ('3', self.append_to_display), ('-',
                                                                                                             self.append_to_display),
            ('C', self.clear_display), ('0', self.append_to_display), ('=', self.calculate_result), ('+',
                                                                                                        self.append_to_display),
        ]
        for text, callback in buttons:
            button = Button(text=text, font_size=40)
            button.bind(on_press=callback)
            buttons_layout.add_widget(button)

        main_layout.add_widget(buttons_layout)
        return main_layout

    def append_to_display(self, instance):
        if self.display.text == 'Error':
            self.display.text = ''
        if instance.text == '=':
            try:
                self.display.text = str(eval(self.expression))
                self.previous_result = self.display.text
            except:
                self.display.text = 'Error'
            self.expression = ""
        elif instance.text == 'C':
            self.expression = ""
            self.display.text = "0"
        else:
            if self.display.text == '0' or (self.previous_result and not self.expression):
                self.display.text = ''
            if self.previous_result and not self.expression:
                self.previous_result = None
                self.display.text = ''
            self.expression += instance.text
            self.display.text += instance.text

    def clear_display(self, instance):
        self.expression = ""
        self.previous_result = None
        self.display.text = "0"

    def calculate_result(self, instance):
        try:
            self.display.text = str(eval(self.expression))
            self.previous_result = self.display.text
        except:
            self.display.text = 'Error'
        self.expression = ""


if __name__ == '__main__':
    CalculatorApp().run()
