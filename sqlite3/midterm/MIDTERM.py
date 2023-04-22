import os, sys
import datetime
from kivy.config import Config
Config.set('graphics', 'width', '414')
Config.set('graphics', 'height', '896')
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
import sqlite3
from kivy.resources import resource_add_path, resource_find
import base64
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout
from kaki.app import App
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton,MDFillRoundFlatButton
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.pickers import MDDatePicker
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.chip import MDChip
from kivymd.uix.screen import MDScreen



LabelBase.register(name="MARY", fn_regular="MARY.ttf")
LabelBase.register(name= "Sniglet", fn_regular= "Sniglet.ttf")
LabelBase.register(name= "Bob", fn_regular= "Bob.ttf")
LabelBase.register(name= "Sugar", fn_regular= "Sugar.ttf")
LabelBase.register(name= "little", fn_regular= "little.ttf")
LabelBase.register(name= "lj", fn_regular= "lj.ttf")




class MyScreen(MDScreen):
    def removes_marks_all_chips(self, selected_instance_chip):
        for instance_chip in self.ids.chip_box.children:
            if instance_chip != selected_instance_chip:
                instance_chip.active = False


        
class IconListItem(OneLineIconListItem):
    icon = StringProperty()

    
class MainLayout(FloatLayout):
    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''

        print(instance, value, date_range)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def date_picker(self):
        date_dialog = MDDatePicker(min_date=datetime.date.today())
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


    def __init__(self, services):
        super().__init__(services)
        services = [
            {
                "viexclass": "IconListItem",
                "icon": "tooth",
                "text": "[color=#B84C65]Tooth Extraction[/color]",
                "height": dp(50),
                "font_name": "midterm/MARY.ttf",
                "on_release":  lambda x ="Tooth Extraction":self.setthat(x),
            },{
                "viewclass": "IconListItem",
                "icon": "tooth",
                "text": "[color=#B84C65]Pasta [/color]",
                "height": dp(50),
                "on_release":  lambda x ="Pasta":self.setthat(x),
                
            },{
                "viewclass": "IconListItem",
                "icon": "tooth",
                "text": "[color=#B84C65]Wisdom Tooth Extraction[/color]",
                "font_name": "midterm/MARY.ttf",
                "height": dp(50),
                "on_release":  lambda x ="Wisdom Tooth Extraction":self.setthat(x),
                
                 
            },{
                "viewclass": "IconListItem",
                "icon": "tooth",
                "text": "[color=#B84C65]Metal Braces[/color]",
                "font_name": "midterm/MARY.ttf",
                "height": dp(50),
                "on_release":  lambda x ="Metal Braces":self.setthat(x),
                
                 
            },{
                "viewclass": "IconListItem",
                "icon": "tooth",
                "text": "[color=#B84C65]Dental Check-up[/color]",
                "font_name": "midterm/MARY.ttf",
                "height": dp(50),
                "on_release":  lambda x ="Dental Check-up":self.setthat(x),
                
                 
            }
        ]
        self.serv = MDDropdownMenu(
            caller=self.ids.lserv,
            items=services,
            position="auto",
            width_mult=3
 
        )
        self.set_it(services)
        self.serv.bind()
    def setthat(self,item):
        self.ids.lserv.text=item
        self.serv.dismiss()
    def set_it(self,text_item):
        self.ids.lserv.set_item=text_item
       
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "doctor",
                "text": "[color=#B84C65]Dr. Michaela Palapar[/color]",
                "height": dp(100),
                "font_name": "midterm/MARY.ttf",
                "on_release":  lambda x ="Dr. Michaela Palapar":self.setthis(x),
            },{
                "viewclass": "IconListItem",
                "icon": "doctor",
                "text": "[color=#B84C65]Dr.Erald Talavera [/color]",
                "height": dp(100),
                "on_release":  lambda x ="Dr. Erald Talavera":self.setthis(x),
                
            },{
                "viewclass": "IconListItem",
                "icon": "doctor",
                "text": "[color=#B84C65]Dr. Alyssa Manuel[/color]",
                "font_name": "midterm/MARY.ttf",
                "height": dp(100),
                "on_release":  lambda x ="Dr. Alyssa Manuel":self.setthis(x),
                
                 
            }
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            position="auto",
            width_mult=3, 
            
            
 
        )
        self.set_item(menu_items)
        self.menu.bind()
    def setthis(self,item):
        self.ids.drop_item.text=item
        self.menu.dismiss()
    def set_item(self,text_item):
        self.ids.drop_item.set_item=text_item
        
    dialog = None
    def LG(self,log_screen, left):
        self.ids.screen_manager2.current = log_screen
        self.ids.screen_manager2.transition.direction = left
    
    def checker(self):
        if self.ids.text_field.text == self.ids.confpass.text:
            self.ids.check.text= ("Password Matched!" )
            
        else:
            self.ids.check.text = ("Your Password did not Match!")
    
    
    
    def add_user(self):
        inp_fullname = self.ids.fullname.text
        inp_email = self.ids.email.text
        inp_add = self.ids.address.text
        inp_pnum = self.ids.pnum.text
        inp_lpassword = self.ids.text_field.text
        inp_confpassword = self.ids.confpass.text
        print("before:" + inp_lpassword)
        print("after:" + self.passenc(inp_lpassword))
        
            
        dbconn = sqlite3.connect("MIDTERM.db",detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = dbconn.cursor()
        database_params ={
                
                'var_email' : inp_email,
                'var_fullname' : inp_fullname,
                'var_address' : inp_add,
                'var_pnumber' :inp_pnum ,
                'var_password': self.passenc(inp_lpassword),
                
                
            }
        dbcursor.execute("INSERT INTO login(email, fullname , address, pnumber, custompass)VALUES(:var_email, :var_fullname,:var_address, :var_pnumber,  :var_password)" , database_params )
        
        print(inp_confpassword)
        
        dbconn.commit()
        dbconn.close()
        if self.verif():
            okay = True #self.add_user() #insert record to database
            if okay: 
                self.incorrectlogdialog("Registration Complete!", True)  
            else:
                self.incorrectlogdialog("Please fill out all the fields to continue ")
        self.ids.screen_manager2.current = "register_screen"
        self.ids.screen_manager2.transition.direction = "left"
    def verif(self):    
        inp_fullname = self.ids.fullname.text
        inp_email = self.ids.email.text
        inp_add = self.ids.address.text
        inp_pnum = self.ids.pnum.text
        inp_lpassword = self.ids.text_field.text
        inp_confpassword = self.ids.confpass.text
        
        if not inp_fullname or not inp_email or not inp_add or not inp_pnum or not inp_lpassword or not inp_confpassword: 
            self.incorrectlogdialog("Please fill up all required fields to continue") 
            return False    
        else: 
            self.incorrectlogdialog("Registration Complete! ")
            
  
        
    def clear(self):
         
        self.ids.fullname.text  = ''
        self.ids.email.text = ''
        self.ids.address.text  = ''
        self.ids.pnum.text     = ''
        self.ids.text_field.text = ''
        self.ids.confpass.text = ''
        
        
    def LOG(self):
        
        inp_email = self.ids.emaill.text
        inp_lpassss = self.ids.Passwd.text
        dbconn = sqlite3.connect("MIDTERM.db",detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = dbconn.cursor()
        dbcursor.execute("SELECT * FROM login  WHERE email = :var_email AND custompass = :var_password", {'var_email' : inp_email, 'var_password' : self.passenc(inp_lpassss) })
        records = dbcursor.fetchall()
        print("email: ", inp_email , "pass: ",inp_lpassss)
        if not records:
            print("No records created")
            self.incorrectlogdialog("Incorrect Email Address and Password!")
        else:
            print("Record Exist")
            dbconn.commit()
            dbconn.close()
            self.ids.screen_manager2.current = "home_screen"
            self.ids.screen_manager2.transition.direction = "left"
            self.incorrectlogdialog("Login Successful!")
            
                
            
    
    def incorrectlogdialog(self, mid):
        if not self.dialog:
            self.clear()
            self.dialog = MDDialog(
                text=f"[color=#B84C65]{mid}[/color]",
                buttons=[
                    MDFillRoundFlatButton(
                        text="EXIT",
                        on_release= self.dialog_close,
                        pos_hint={'center_x': 0.5,'center_y': 0.5},
                        md_bg_color="pink"
                        
                    )
                ],
            ) 
            
        else :
            self.dialog = MDDialog(
                text=f"[color=#B84C65]{mid}[/color]",
                buttons=[
                    MDFillRoundFlatButton(
                        text="EXIT",
                        md_bg_color="pink",
                        pos_hint={'center_x': 0.5},
                        on_release= self.dialog_close
                        
                    )
                ],
            )
            
        self.dialog.open()
        
    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)    
            
    def passenc(self, password_string):
        asci_pass = password_string.encode("ascii") 
        b64_pass = base64.b64encode(asci_pass)
        return b64_pass.decode("ascii")
    
    def passdec(self, password_string):
        asci_pass = password_string.encode("ascii") 
        b64_pass = base64.b64encode(asci_pass)
        return b64_pass.decode("ascii")

 
    
   

class MIDTERMApp(MDApp):
    def build(self):
            self.theme_cls.material_style = "M3"    
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette= "Pink"
            self.theme_cls.accent_palette= "Purple"
            return MainLayout()  
    
if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    MIDTERMApp().run()
