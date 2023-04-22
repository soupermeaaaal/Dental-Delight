import os, sys
import datetime     #FOR date saving of current date
import base64       #FOR password encoding

from kivy.lang import Builder
from kivy.config import Config
Config.set('graphics', 'width', '600')   #change screen width
Config.set('graphics', 'height', '800')  #change screen height

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton,MDFillRoundFlatButton
from kivymd.uix.screenmanager import MDScreenManager
from kivy.metrics import dp
from kivy.properties import StringProperty,NumericProperty,ObjectProperty
from kivy.resources import resource_add_path, resource_find
from kivymd.uix.dialog import MDDialog

#Builder.load_file('./mdAppComponents.kv')    
class MainLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    screen_manager = ObjectProperty(None)
    dbconn    = None
    dialogbox = None
    
    
    def login_account(self):
        """
        Validate username and password from user input. If the value of login_complete
        is true, generate a Login Success dialogbox, otherwise, prompt that username and password 
        not found.
        """
        
        input_username = self.ids.log_username.text.strip()
        input_password = self.ids.log_password.pass_text.text.strip()
        login_complete = False  
        if login_complete: 
            self.display_dialog("Login Success!")
        else:
            self.display_dialog("Username & password not found")
    
    
        
    def register_account(self,app):
        """
        Validate registration fields using input_validate function. If the value of reg_complete
        is true, generate a Registration Success dialogbox, otherwise, prompt that an error message.
        """
        
        if self.input_validate():
            reg_complete = True #self.add_user() #insert record to database
            if reg_complete: 
                self.display_dialog("", True)
            else:
                self.display_dialog("Error inserting records")
           
            
            
    def display_dialog(self, text_msg,is_success=False):
        """
        Use to generate dialog box with parameter-based text property. If is_success is true,
        generate a customize dialog box for registration success prompt

            Parameter:
                text_msg(str)   : Message to display in dialog box
                is_success(bool): Default to False, if this is true, display a custom success
                                  dialogbox 
        """
        
        if is_success :
            self.dialogbox = None
            if not self.dialogbox:
                self.clear_registration()
                self.dialogbox = MDDialog(
                    type="custom",
                    content_cls=RegDialogContent(),
                    buttons = [MDFillRoundFlatButton(
                                    text='Return to Login',  #pad blank spaces left and right
                                    font_size="20sp",
                                    md_bg_color="orange",
                                    pos_hint={'center_x': 0.5},
                                    on_release=self.reg_success_button
                                )],
                )
            self.dialogbox.open()  
        else:
            self.dialogbox = None
            if not self.dialogbox:
                self.dialogbox = MDDialog(
                    text=f"[color=#263238]{text_msg}[/color]",
                    buttons = [MDRaisedButton(
                            text="Ok",
                            md_bg_color="orange",
                            pos_hint={'center_x': 0.5},
                            on_press=self.dismiss_dialog)],
                )
            self.dialogbox.open()  
        
    
        
    def dismiss_dialog(self,*args):
        """
        Function to close/dismiss the current dialogbox
        """
        
        if self.dialogbox: #requires to have an existing dialogbox open
            self.dialogbox.dismiss()
    
    
    
    def reg_success_ok_button(self,*args):
        """
        A dismiss_dialog() copy, specific to registration success dialog box.
        Dismiss the dialog box and return to login screen after pressing the
        'Return to Login' button
        """
        
        if self.dialogbox: #requires to have an existing dialogbox open
            self.dismiss_dialog()
            self.screen_manager.current = "login_screen" 
            self.screen_manager.transition.direction = "right"     
        
    
           
    def input_validate(self):
        """
        Validate user input in registration screen. Returns True if all validations are passed.
        
            Returns:
                True/False(bool): 
        """
        
        #strip removes any extra spaces
        username    = self.ids.username.text.strip()  
        firstname   = self.ids.firstname.text.strip()  
        lastname    = self.ids.lastname.text.strip()  
        email       = self.ids.email.text.strip()  
        password    = self.ids.password.pass_text.text.strip()
        cbTerms     = self.ids.checkBox.active
        
        #check if any one of the fields is empty
        if not username or not firstname or not lastname or not email or not password: 
            self.display_dialog("Please fill up all required fields") 
            return False    
        #check if checkbox is not checked   
        elif not cbTerms:
            self.display_dialog("You must agree to terms and condition")
            return False
        else:
            return True   
            
    
            
    def password_encode(self,password_string):
        """
        Encode password into b64 encryption for database storage.
        
            Returns:
                password(string): encoded password in b64encoding 
        """
        
        ascii_pass  = password_string.encode("ascii")
        b64_pass    = base64.b64encode(ascii_pass)
        return b64_pass.decode("ascii")
    
    
    
    def password_decode(self,password_string):
        """
        Decode password into b64 decryption for password viewing(not in use in this app).
        
            Returns:
                password(string): decoded password
        """
        
        ascii_pass  = password_string.encode("ascii")
        b64_pass    = base64.b64decode(ascii_pass)
        return b64_pass.decode("ascii")
    
    
    
    def clear_registration(self):
        """
        Clear input fields in registration screen.
        """
        self.ids.username.text  = ''
        self.ids.firstname.text = ''
        self.ids.lastname.text  = ''
        self.ids.email.text     = ''
        self.ids.password.pass_text.text = ''
        self.ids.checkBox.active = False

        
class CustomPasswordField(MDRelativeLayout):
    text      = StringProperty()
    hint_text = StringProperty()
    pass_text = ObjectProperty(None)

class CustomPasswordRegField(MDRelativeLayout):
    text      = StringProperty()
    hint_text = StringProperty()      
    pass_text = ObjectProperty(None)

class RegDialogContent(MDBoxLayout):
    pass      

class mdAppComponentsApp(MDApp):
    def build(self):
            self.theme_cls.material_style = "M3"    
            self.theme_cls.theme_style    = "Light"
            self.theme_cls.primary_palette= "Blue"
            self.theme_cls.accent_palette = "Teal"
            return MainLayout()  
      
      
if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    mdAppComponentsApp().run()