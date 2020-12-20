from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton, MDRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

input_one_helper = """
MDTextField:
    hint_text: "Enter Data" 
    pos_hint: {'center_x': 0.5, 'center_y': 0.7}
    size_hint: (0.3, 0.1)
"""

input_two_helper = """
MDTextField:
    hint_text: "Enter Data" 
    pos_hint: {'center_x': 0.5, 'center_y': 0.55}
    size_hint: (0.3, 0.1)
"""

input_three_helper = """
MDTextField:
    hint_text: "Enter Data" 
    pos_hint: {'center_x': 0.5, 'center_y': 0.4}
    size_hint: (0.3, 0.1)
"""

doctor_email_helper = """
MDTextField:
    hint_text: "Enter Doctor Email" 
    pos_hint: {'center_x': 0.5, 'center_y': 0.25}
    size_hint: (0.3, 0.1)
"""


class App(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        screen = Screen()

        title = MDLabel(text="Health Check", halign="center", theme_text_color="Custom", font_style="H3",
                        pos_hint={'center_x': 0.5, 'center_y': 0.85}, text_color=(255 / 256, 165 / 256, 0 / 256, 1))

        submit_button = MDRectangleFlatButton(text="Submit", pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                              on_release=self.show_data)

        self.input_one = Builder.load_string(input_one_helper)
        self.input_two = Builder.load_string(input_two_helper)
        self.input_three = Builder.load_string(input_three_helper)

        self.doctor_email = Builder.load_string(doctor_email_helper)

        screen.add_widget(title)
        screen.add_widget(submit_button)

        screen.add_widget(self.input_one)
        screen.add_widget(self.input_two)
        screen.add_widget(self.input_three)

        screen.add_widget(self.doctor_email)

        return screen

    def show_data(self, obj):
        inp_one = self.input_one.text
        inp_two = self.input_two.text
        inp_three = self.input_three.text

        doc_email = self.doctor_email.text

        sender_email = "health1.check@gmail.com"
        passw = "hack12345"
        subj = "Health Check Patient Report"
        mesg = "Your patient on Health Check has out of bounds results. Please contact them as soon as possible."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = doc_email
        msg['Subject'] = subj

        msg.attach(MIMEText(mesg, 'plain'))

        if inp_one == "" or inp_two == "" or inp_three == "":
            text = "Please enter valid data."
        elif doc_email == "":
            text = "Please enter a valid email."
        else:
            if inp_one.isalpha() or inp_two.isalpha() or inp_three.isalpha():
                text = "Please enter valid data."
            else:
                if float(inp_one) > 10.0 or float(inp_two) > 10.0 or float(inp_three) > 10.0:
                    text = "Your test results are out of bounds. We have notified your doctor at {}".format(doc_email)
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, passw)
                    txt = msg.as_string()
                    server.sendmail(sender_email, doc_email, txt)
                    server.quit()
                else:
                    text = "Your test results are within bounds. No action is needed."

        self.dialog = MDDialog(text=text, size_hint=(0.8, 1),
                               buttons=[MDRoundFlatButton(text="Close", on_release=self.close)])
        self.dialog.open()

    def close(self, obj):
        self.dialog.dismiss()


if __name__ == "__main__":
    App().run()
