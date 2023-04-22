import os, sys
from kaki.app import App 
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.resources import resource_add_path, resource_find
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.properties import NumericProperty
    
class MainLayout(MDBoxLayout):
    
    def function_name(self,app):
        if app.theme_cls.theme_style== 'Dark':
           app.theme_cls.theme_style= 'Light'
           app.theme_cls.primary_palette= "Yellow"
        else:
            app.theme_cls.theme_style= 'Dark'
            app.theme_cls.primary_palette= "Purple"
    dialog = None
    def show_alert_dialog(self):
        self.dialog= None
        if not self.dialog:
            self.dialog = MDDialog(
            title= "Exit?",
                text= "Confirm Logout?",
                buttons=[
                MDFlatButton(
                    text="CANCEL",
                    font_size= '18sp',
                    on_release=self.close_dialog
                ),
                MDRaisedButton(
                    text= "LOGOUT",
                    text_color= "white",
                    font_size= '18sp',
                    on_release=self.close_dialog
                    
                ),
                ],  
                )   
            self.dialog.open()
    def close_dialog(self,obj):
        self.dialog.dismiss()
    
    notif = NumericProperty(0)
    def spam(self):
        self.notif+=1
        if self.notif <=10:
            self.ids.screen5.badge_icon=f'numeric-{self.notif}'
        
    
    def clear(app):
        app.notif = 0
        app.ids.screen5.badge_icon = ""
class mdAppComponents(MDApp):
    def build(self):
        
        return MainLayout()  

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()      
      
if __name__ == '__mainnn__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    mdAppComponents().run()