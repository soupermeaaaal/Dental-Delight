import os, sys
from kivy.config import Config
#Config.set('graphics', 'width', '730')
#Config.set('graphics', 'height', '980')
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
import sqlite3
import datetime
from kivy.resources import resource_add_path, resource_find
import base64
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.snackbar import BaseSnackbar
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivymd.uix.card import MDCard

#Builder.load_file('MIDTERM.kv')
#Define our different screens
class CustomSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")
    
    
class CCARD(MDCard):
    id      = StringProperty(None)
    title   = StringProperty(None)
    source  = StringProperty(None)
    group   = StringProperty(None)
    def assign_texture_from_database(self,dbTexture):
        self.ids.display_image.texture = dbTexture
        

class MainLayout(FloatLayout):
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)
        self.load_cards()
    def load_cards(self):
        # self.ids.scrn2.clear_widgets()
        # mdCard = CCARD(id="1", title="Test",source=f"",group="group")
        # self.ids.scrn2.add_widget(mdCard)
    def LS(self,login_screen, left):
        self.ids.screen_manager1.current = login_screen
        self.ids.screen_manager1.transition.direction = left
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)
        self.store = JsonStore("loggedUser.json")
        try:
            if self.store.get('UserInfo')['firstname'] != "":
                self.ids.screen_manager1.current = "dashboard_screen"    
        except KeyError:
            self.ids.screen_manager1.current = "login_screen"
    
    def open_icon_snackbar(self):
        snackbar = CustomSnackbar(
            text="This is a sample snackbar error!",
            icon= "close-circle",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x= (Window.width - (dp(10) * 2)) / Window.width,
            bg_color="#B71C1C"
        )
        snackbar.open()

    def open_custom_snackbar(self):
        snackbar = Snackbar(text="Yo! this is a custom snackbar!", snackbar_x="10dp", snackbar_y="10dp",size_hint_x= (Window.width - (dp(10) * 2)) / Window.width,bg_color= "orange")
        snackbar.open()
    
    def RS(self):
        inp_uname = self.ids.uname.text
        inp_fname= self.ids.fname.text
        inp_lname = self.ids.lname.text
        inp_email = self.ids.email.text
        inp_lpass = self.ids.lpass.text
        print("before:" + inp_lpass)
        print("after:" + self.passenc(inp_lpass))
        dbconn = sqlite3.connect("kivysql.db",detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = dbconn.cursor()
        database_params ={
                'var_username' : inp_uname,
                'var_firstname' : inp_fname,
                'var_lastname' : inp_lname,
                'var_email' : inp_email,
                'var_password' : self.passenc(inp_lpass),
                'var_created_at' : datetime.datetime.now(),
                'var_updated_at' : datetime.datetime.now()
                
            }
        dbcursor.execute("INSERT INTO mstuser(username, first_name, last_name, email, password, created_at, updated_at)VALUES(:var_username, :var_firstname, :var_lastname, :var_email, :var_password, :var_created_at, :var_updated_at)" , database_params )
        dbconn.commit()
        dbconn.close()
        self.ids.screen_manager1.current = "login_screen"
        self.ids.screen_manager1.transition.direction = "left"
    
    def Login(self):
        inp_username = self.ids.unname.text
        inp_password = self.ids.lpasss.text
        dbconn = sqlite3.connect("kivysql.db",detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = dbconn.cursor()
        dbcursor.execute("SELECT * FROM mstuser WHERE mstuser.username = :var_username AND password = :var_password", {'var_username' : inp_username, 'var_password' : self.passenc(inp_password) })
        records = dbcursor.fetchall()
        
        if not records:
            print("No records created")
        else:
            for user in records: 
                print(f"Username:{user[1]}\nFirstName:{user[2]}\nLastName:{user[3]}")
                self.store.put('UserInfo', code= user[0], firstname=user[2], lastname=user[3], username=user[1])
            print("Record Exist")
            dbconn.commit()
            dbconn.close()
            self.ids.screen_manager1.current = "dashboard_screen"
            self.ids.screen_manager1.transition.direction = "left"
        
    def passenc(self, password_string):
        asci_pass = password_string.encode("ascii") 
        b64_pass = base64.b64encode(asci_pass)
        return b64_pass.decode("ascii")
    
    def passdec(self, password_string):
        asci_pass = password_string.encode("ascii") 
        b64_pass = base64.b64encode(asci_pass)
        return b64_pass.decode("ascii")

class screenManagerApp(MDApp):
    def build(self):
            self.theme_cls.material_style = "M3"    
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette= "Purple"
            self.theme_cls.accent_palette= "Teal"
            return MainLayout()  

    
if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    screenManagerApp().run()
