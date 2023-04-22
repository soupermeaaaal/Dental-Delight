import os, sys
from kaki.app import App 
from kivy.factory import Factory
from kivy.config import Config
from kivy.resources import resource_add_path, resource_find


#from kivy.core.window import Window
# Config.set('graphics', 'width', '730')
# Config.set('graphics', 'height', '980')
# Config.set('graphics','resizable',0)
from kivymd.app import MDApp


class MainApp(App,MDApp):    
    DEBUG = True
    
    KV_FILES = {
        os.path.join(os.getcwd(), "mdAppComponents.kv")
        #os.path.join('.', 'logic.screen_manager.kv')
    }

    CLASSES = {
        "MainLayout": "kivymd1"
        
    }

    AUTORELOADER_PATHS = [('.', {"recursive": True})]
    
    def build_app(self):
        self.theme_cls.material_style = "M3"    
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette= "Purple"
        self.theme_cls.accent_palette= "Teal"
        return Factory.MainLayout()  


    
if hasattr(sys, '_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS))
MainApp().run()