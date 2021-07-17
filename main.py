from datetime import datetime
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
import ddown as cust_dd
import json

#import requests

#Window.size = (300,500)



#url = 'http://api.exchangeratesapi.io/v1/latest?access_key=5735b4f3f6a5c3a14b5e711b94391e9c'
#http://data.fixer.io/api/latest?access_key=925533e9fa7fd3e75eb89b2b00278076

# Making our request
#response = requests.get(url)
#data = response.json()

# Your JSON object
#print(data['success'])
#with open("latest.json","w") as f:
#    json.dump(data, f, indent = 6)

with open('latest.json', encoding='utf-8') as f:
    data = json.load(f)

time = datetime.utcfromtimestamp(data['timestamp'])


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

class MainApp(MDApp):
    dd = ''
    dialog = None
    curr = data


    def __init__(self, **kwargs):
        super(MDApp, self).__init__(**kwargs)
        # code goes here and add:
        Window.bind(on_keyboard=self.Android_back_click)

    def Android_back_click(self):
        self.root.ids.sm.current = "sc_main_tp"


    def build(self):
        self.theme_cls.primary_palette = 'Blue'

    def cal(self):
        amt = 0 if self.root.ids.amount.text == '' \
        else float(self.root.ids.amount.text)

        self.root.ids.ans.text = \
            self.root.ids.amount.text + ' ' + \
            self.root.ids.fr.text[:3] + ' = ' + \
            str(truncate(amt * \
            (self.curr['rates'][self.root.ids.to.text[:3]] / \
             self.curr['rates'][self.root.ids.fr.text[:3]]),2)) + ' ' + \
            self.root.ids.to.text[:3]

    def sc_main_tp(self):
        self.root.ids.sm.current = "sc_main_tp"
        self.root.ids.toolbar.left_action_items=[]
        self.root.ids.toolbar.title = "Pay and Transfer"

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                type="custom",
                content_cls=cust_dd.Content(),

            )

        global lst
        #self.dd = self.root.ids.PrsDtl.dd
        dy_lst=['']

        self.dialog.content_cls.lst = \
            cust_dd.cntry_name_lst if self.dd == 'FR' \
            else cust_dd.cntry_name_lst if self.dd == 'TO' \
            else ''

        self.dialog.title = \
            'From' if self.dd == 'FR' \
            else 'To' if self.dd == 'TO' \
            else ''

        self.dialog.content_cls.set_list_md_icons()
        self.dialog.open()


MainApp().run()