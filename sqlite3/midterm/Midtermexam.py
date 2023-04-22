import os, sys
from kaki.app import App 
from kivy.factory import Factory
from kivy.config import Config
from kivy.resources import resource_add_path, resource_find


#from kivy.core.window import Window
Config.set('graphics', 'width', '414')
#Config.set('graphics', 'height', '896')
#Config.set('graphics','resizable',0)
from kivymd.app import MDApp

class Midterm(App,MDApp):    
    DEBUG = True
    
    KV_FILES = {
        os.path.join('.', 'MT.kv')
    }

    CLASSES = {
        "MainLayout": "MIDTERM"
    }

    AUTORELOADER_PATHS = [('.', {"recursive": True})]
    
    def build_app(self):
        self.theme_cls.matepythorial_style = "M3"    
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette= "Pink"
        self.theme_cls.accent_palette= "Purple"
            
        return Factory.MainLayout()


if hasattr(sys, '_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS))
Midterm().run()