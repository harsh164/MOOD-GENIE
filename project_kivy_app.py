from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import urllib
import requests
import urllib.request
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('pis2019-1d8caca8db36.json', scope)

client = gspread.authorize(credentials)

sheet = client.open('Pis').sheet1

data = sheet.get_all_records()


def data_read():
    """
    url1 = urllib.request.urlopen("https://my-json-server.typicode.com/VaibhavGupta-19341/PIS_Major_Project/posts")
    data = json.loads(url1.read())
    print(data[-1])
    new_data = data[-1]
    data = "happy,harsh verma,harsh19164@iiitd.ac.in, 2019164"
    #  data = url.urlllib.read()
    #  data = data.read()
    #  data = str(data)
    """
    scope = ['https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('pis2019-1d8caca8db36.json', scope)

    client = gspread.authorize(credentials)

    sheet = client.open('Pis').sheet1

    data = sheet.get_all_records()
    new_data = data[0]
    first_name = new_data['MOOD']
    last_name = new_data['BPM']
    email = new_data['GSR']
    roll = new_data['TEMP']
    if first_name == "happy":
        play_list = "https://www.youtube.com/playlist?list=PL__XwIMVfN10z_iBPX6_MaLbt17s3ueJF"
    elif first_name == "neutral":
        play_list = "https://www.youtube.com/playlist?list=PL__XwIMVfN13AFnf84dLkQp1vmg3eVKTd"
    else:
        play_list = "https://www.youtube.com/playlist?list=PL__XwIMVfN13OucHm4zCyGWlfBAqP3YQX"

    return (first_name, last_name, email, roll, play_list)


class my_grid(GridLayout):
    def __init__(self, **kwargs):
        super(my_grid, self).__init__(**kwargs)
        data = data_read()
        fst = data[0]
        mid = data[1]
        thr = data[-1]
        self.cols = 1
        self.inside = GridLayout()
        self.inside.cols = 2

        #  self.inside.add_widget(Label(text="first Name = "))
        self.inside.add_widget(Label(text="YOUR MOOD IS"))
        self.first_name = TextInput(multiline=False)
        self.inside.add_widget(self.first_name)

        #  self.inside.add_widget(Label(text="Last Name = "))
        self.inside.add_widget(Label(text="YOUR BPM IS"))
        self.last_name = TextInput(multiline=False)
        self.inside.add_widget(self.last_name)

        #  self.inside.add_widget(Label(text="Email ID = "))
        self.inside.add_widget(Label(text="GRS READING IS"))
        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)

        #  self.inside.add_widget(Label(text="roll = "))
        self.inside.add_widget(Label(text="TEMPERATURE OF YOUR FINGURE IS"))
        self.roll = TextInput(multiline=False)
        self.inside.add_widget(self.roll)

        self.inside.add_widget(Label(text="LINK OF PLAYLIST IS"))
        self.PLAY = TextInput(multiline=False)
        self.inside.add_widget(self.PLAY)

        self.add_widget(self.inside)
        self.sumbit = Button(text="submit", font_size=40)
        self.sumbit.bind(on_press=self.pressed)
        self.add_widget(self.sumbit)

    def pressed(self, instance):
        print("pressed")
        first_name = self.first_name.text
        last_name = self.last_name.text
        email = self.email.text
        print((first_name, last_name, email))
        data = data_read()
        fst = data[0]
        mid = data[1]
        thr = data[2]
        frt = data[3]
        play_list = data[-1]
        self.first_name.text = str(fst)
        self.last_name.text = str(mid)
        self.email.text = str(thr)
        self.roll.text = str(frt)
        self.PLAY.text = str(play_list)


class my_app(App):
    def build(self):
        return my_grid()


if __name__ == "__main__":
    my_app().run()
