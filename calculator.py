from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.config import Config
from kivy.clock import Clock
import sympy as sp

Config.set('graphics', 'width', '440')
Config.set('graphics', 'height', '770')
Config.set('graphics', 'resizable', False)



class MainApp(App):
    def build(self):
        self.icon = "calculator.png"
        self.operators = ["/", "*", "+", "-"]
        self.expression = ""
        self.memory_value = 0
        self.previous_result = None
        self.enabled = False

        main_layout = BoxLayout(orientation="vertical")

        # On and Off buttons layout
        on_off_layout = BoxLayout(size_hint=(1, 0.1), padding=[10, 10, 10, 0])
        on_button = Button(text="On", font_size=20, size_hint=(None, None), size=(100, 50), color="blue")
        on_button.bind(on_press=self.turn_on)
        off_button = Button(text="Off", font_size=20, size_hint=(None, None), size=(100, 50), color="blue")
        off_button.bind(on_press=self.turn_off)
        on_off_layout.add_widget(on_button)
        on_off_layout.add_widget(off_button)

        # Equation and solution layout
        equation_solution_layout = BoxLayout(orientation="vertical", size_hint=(1, 0.2), padding=[10, 10, 10, 10])
        self.display = Label(text="", color="grey", font_size=40, halign="right")
        self.solution_label = Label(text="", color="red", font_size=20, halign="right")
        equation_solution_layout.add_widget(self.display)
        equation_solution_layout.add_widget(self.solution_label)

        # Buttons layout
        buttons_layout = GridLayout(cols=4, spacing=10)
        buttons_layout.bind(minimum_height=buttons_layout.setter('height'))
        buttons = [
            ('7', self.append_to_display), ('8', self.append_to_display), ('9', self.append_to_display),
            ('/', self.append_to_display),
            ('4', self.append_to_display), ('5', self.append_to_display), ('6', self.append_to_display),
            ('*', self.append_to_display),
            ('1', self.append_to_display), ('2', self.append_to_display), ('3', self.append_to_display),
            ('+', self.append_to_display),
            ('.', self.append_to_display), ('0', self.append_to_display), ('CE', self.clear_last_character),
            ('-', self.append_to_display),
            ('=', self.evaluate_expression),
            ('(', self.append_to_display), (')', self.append_to_display), ('log', self.append_to_display),
            ('exp', self.append_to_display),
            ('x^2', self.append_to_display), ('1/x', self.append_to_display), #('+/-', self.append_to_display)#,
            ('^', self.append_to_display),
            ('C', self.clear_display), ('MC', self.memory_clear), ('MR', self.memory_recall),
            ('M+', self.memory_add), ('M-', self.memory_subtract), ('MS', self.memory_store), ('%', self.percent),
            ('π', self.append_to_display), ('.00', self.append_to_display), ('00', self.append_to_display),
            ('sin', self.append_to_display),
            ('√', self.append_to_display)
        ]

        for text, callback in buttons:
            button = Button(text=text,
                            font_size=20,
                            size_hint=(None, None),
                            size=(100, 50),
                            background_color="blue",
                            color="pink",
                            )
            button.bind(on_press=callback)
            buttons_layout.add_widget(button)

        # Make the buttons layout scrollable
        buttons_scroll_view = ScrollView(size_hint=(1, 0.7))
        buttons_scroll_view.add_widget(buttons_layout)

        main_layout.add_widget(on_off_layout)
        main_layout.add_widget(equation_solution_layout)
        main_layout.add_widget(buttons_scroll_view)

        return main_layout

    def append_to_display(self, instance):
        if self.enabled:
            if self.display.text == 'Syntax Error':
                self.display.text = ''

            if instance.text == '=':
                self.evaluate_expression(instance)
            elif instance.text == 'C':
                self.clear_display()
            elif instance.text == 'CE':
                self.clear_last_character()
            else:
                if self.display.text == '' or (self.previous_result and not self.expression):
                    self.display.text = ''

                if self.previous_result and not self.expression:
                    self.previous_result = None
                    self.display.text = ''

                if instance.text.isdigit() or instance.text == '.':
                    if self.expression and (
                            self.expression[-1].isdigit() or self.expression[-1] == ')' or self.expression[
                        -1] == 'π'):
                        self.expression += '*' + instance.text
                    else:
                        self.expression += instance.text
                    self.display.text += instance.text
                else:
                    if instance.text == 'π':
                        if self.expression and self.expression[-1].isdigit():
                            self.expression += '*' + str(sp.pi)
                        elif self.expression and self.expression[-1] == 'π':
                            self.expression += '*'
                        else:
                            self.expression += str(sp.pi)
                        self.display.text += 'π'
                    elif instance.text == '√':
                        if not self.expression or not self.expression[-1].isdigit():
                            self.expression += 'sqrt('
                            self.display.text += '√('
                        else:
                            self.expression += '*sqrt('
                            self.display.text += '√('
                    elif instance.text == 'sin':
                        if not self.expression or not self.expression[-1].isdigit():
                            self.expression += 'sin('
                            self.display.text += 'sin('
                        else:
                            self.expression += '*sin('
                            self.display.text += 'sin('
                    elif instance.text == 'log':
                        if not self.expression or not self.expression[-1].isdigit():
                            self.expression += 'log('
                            self.display.text += 'log('
                        else:
                            self.expression += '*log('
                            self.display.text += 'log('
                    else:
                        self.expression += instance.text
                        self.display.text += instance.text

    def evaluate_expression(self, instance):
        try:
            # Evaluate the expression
            result = sp.sympify(self.expression).evalf()
            if result is not None:
                self.solution_label.text = str(result)  # Update solution_label.text
                self.previous_result = self.solution_label.text
            else:
                self.solution_label.text = 'Syntax Error'
        except Exception as e:
            print(e)
            self.solution_label.text = 'Syntax Error'
        self.expression = ""

    def clear_display(self, instance=None):
        if self.enabled:
            self.expression = ""
            self.previous_result = None
            self.display.text = ""

    def clear_last_character(self):
        if self.enabled:
            if self.expression:
                if self.expression.endswith('sqrt('):
                    self.expression = self.expression[:-5]
                    self.display.text = self.display.text[:-2] + ' '
                elif self.expression.endswith('√'):
                    self.expression = self.expression[:-1]
                    self.display.text = self.display.text[:-1] + ' '
                else:
                    self.expression = self.expression[:-1]
                    self.display.text = self.display.text[:-1]

    def memory_clear(self, instance):
        if self.enabled:
            self.memory_value = 0

    def memory_recall(self, instance):
        if self.enabled:
            self.display.text += str(self.memory_value)

    def memory_store(self, instance):
        if self.enabled:
            try:
                self.memory_value = float(self.display.text)
            except ValueError:
                self.memory_value = 0

    def memory_add(self, instance):
        if self.enabled:
            try:
                self.memory_value += float(self.display.text)
            except ValueError:
                pass

    def memory_subtract(self, instance):
        if self.enabled:
            try:
                self.memory_value -= float(self.display.text)
            except ValueError:
                pass

    def percent(self, instance):
        if self.enabled:
            try:
                result = eval(self.display.text) / 100
                self.display.text = str(result)
            except Exception as e:
                self.display.text = "Error"

    def on_solution(self):
        text = self.display.text
        if text:
            result = self.evaluate_expression(text)
            if result is not None:
                self.solution_label.text = str(result)
            else:
                self.solution_label.text = "Error"

    def turn_on(self, instance):
        self.enabled = True
        self.display.text = "By Gabriel"
        Clock.schedule_once(self.clear_label, 0.9)

    def turn_off(self, instance):
        self.enabled = False
        self.display.text = "By Gabriel"
        Clock.schedule_once(self.clear_label, 0.9)
        self.solution_label.text = ""

    def clear_label(self, dt):
        self.display.text = ""
        self.solution_label.text = ""


if __name__ == "__main__":
    app = MainApp()
    app.run()
