import os, sys
from datetime import datetime, timedelta #FOR date saving of current date

import base64       #FOR password encoding
import sqlite3      #FOR sqlite3 connection

from kivymd.app           import MDApp
from kivy.lang            import Builder
from kivy.config          import Config
Config.set('graphics', 'width', '600')   #change screen width
Config.set('graphics', 'height', '800')  #change screen height

from kivy.uix.boxlayout   import BoxLayout
from kivy.core.window     import Window
from kivy.metrics         import dp
from kivy.properties      import StringProperty,NumericProperty,ObjectProperty
from kivy.resources       import resource_add_path, resource_find
from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore

from kivymd.uix.dialog         import MDDialog
from kivymd.uix.boxlayout      import MDBoxLayout
from kivymd.uix.button         import MDRaisedButton,MDFillRoundFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.snackbar       import Snackbar
from kivymd.uix.list           import ThreeLineListItem
from kivymd.uix.card           import MDCardSwipe
from kivymd.uix.pickers        import MDDatePicker
from kivymd.uix.menu           import MDDropdownMenu
from kivymd.toast              import toast

#Builder.load_file('./mdAppComponents.kv')    
class MainLayout(BoxLayout):
    screen_manager = ObjectProperty(None)
    bottom_navigation =  ObjectProperty(None)
    dbconn    = None
    dialogbox = None
    active_tab = StringProperty() #current active tab name
    menu        = None #Menu
    date_dialog = None
    has_focus   = False
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        Create a loggedUser.json file. If firstname key exist, automatically redirects
        to dashboard_screen. If no firstname exist(not logged in yet), redirects to login screen
        """
        self.store = JsonStore("loggedUser.json")
        try:
            if self.store.get('UserInfo')['firstname'] != "":
                self.screen_manager.current = 'dashboard_screen'
        except KeyError:
            self.screen_manager.current = 'login_screen'
    
    
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
    
    def assign_active_tab(self,*args): 
        """
        Use to assign the current active tab of Bottom nav, for validation in touch event of
        view_post method.
            Arguments:
                *args(tuple): consist of [0]button Nav object code, [1]button Nav item properties, [2]button Nav Item screen name
        """
        #print(*args)
        self.active_tab = args[2]
    
    
    
    
    ###################################################
    #                                                 #      
    #              VALIDATION METHODS                 #  
    #                                                 #
    ###################################################       
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
    
    def post_validate(self,title,body):
        """
        Validate user input in post screen. Return a python dictionary
        with key value pair for post_record conditioning
        
            Returns:
                status (dictionary): consist of success key and remarks key
        """
        status = {"success": False, "remarks": ""}
        
        if not title: 
            status["remarks"] = "Title field is required" 
            return status    
        if not body: 
            status["remarks"] = "Body field is required"
            return status  

        status["success"] = True
        return status
            
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
    ###################################################
    
    
    
    
    ###################################################
    #                                                 #      
    #              SCREEN BEHAVIOR METHODS            #  
    #                                                 #
    ################################################### 
    def image_click(self):
        print('click image')    
    
    def return_to_dashboard(self,screen_name):
        """
        Return function to dashboard
            Arguments:
                screen_name {str} -- screen name to switch when return to dashboard
        """
        self.bottom_navigation.switch_tab(screen_name) #automatically switch
        self.screen_manager.current = 'dashboard_screen'
        self.screen_manager.transition.direction = "right"
    
    def datetime_difference(self,from_date):
        """
        Returns the number of date or time passed since the date of posting
            Returns:
                difference (str): difference of date posted vs today in minutes/hours/days or months
        """
        #Removes the stored decimal in created_at field
        decimal_index = from_date.find('.')
        if decimal_index != -1:
            from_date = from_date[:decimal_index]
        
        now = datefunct.now()
        try:
            record_date = datefunct.strptime(from_date, "%Y-%m-%d %H:%M:%S")
        except:
            print(f'error from date {from_date}')
            
        diff = now - record_date
        if diff < timedelta(minutes=60):
            return f"{int(diff.seconds / 60)}m"
        elif diff < timedelta(days=1):
            return f"{int(diff.seconds / 3600)}h"
        elif diff < timedelta(days=30):
            return f"{diff.days}d"
        else:
            return f"{int(diff.days / 30)}mo"
    
    def view_post(self,instance,touch):
        """
        Method called when pressing the post list. Use to open the viewpost_screen.
        There is a validation where only 'screen 4' tab is allowed to respond to touch event.
        MDList has no on_press/on_release event, so this function uses touch instead
        
            Arguments:
                instance(object) -- default parameter of on_touch_down event from mdlist
                touch(object) -- default parameter of on_touch_down event from mdlist
        """
        
        if instance.collide_point(*touch.pos) and self.active_tab == 'screen 4':
            #using instance param, you may determine the property associated to the selected MDList.
            #In this example, using instance.rec_id will send the rec_id of the specific selected MDList
            #that will be use to view the actual post.
            self.screen_manager.get_screen("viewpost_screen").assign_post_id(instance.rec_id,'screen 4')
            self.screen_manager.current = "viewpost_screen"
            self.screen_manager.transition.direction = "up"
            
    def date_open(self):
        """
        Opens DatePicker widget
        """
        import datetime
        minimum_date = datetime.date.today()
        # date_dialog = MDDatePicker(
        #     min_year=2024,
        #     mode="picker",
        # )
        print("onfocus")
        if not self.has_focus:
            self.date_dialog = MDDatePicker(
                mode="picker",
                min_date=datetime.date.today(),
                max_date=datetime.date(
                    datetime.date.today().year,
                    datetime.date.today().month,
                    datetime.date.today().day + 2,
                ),
            )
            self.date_dialog.bind(on_save=self.assign_date) #Does not work if you try to initialize on_save on MDDatePicker, so you bind it separately
            self.date_dialog.open()  
            self.has_focus = True
        else:
            self.has_focus = False
            
    def get_default_date(self):
        """
        Get the current date and assign it to default_date MDTextInput
        """
        import datetime
        date_today = datetime.date.today()
        date_today = date_today.strftime('%m/%d/%Y')
        self.ids.default_date.text=date_today 
    
    def assign_date(self, instance, value, date_range):
        self.ids.default_date.text = value.strftime('%m/%d/%Y')
        
    def open_logout_menu(self,button_caller):
        """
        Opens the logout menu from dots-vertical icon in MDTopAppBar
            Arguments:
                button_caller(object): the "x" passed from root.open_logout_menu(x)
        """
        
        #Creates Menu Items to show
        menu_items = [{
            "text": f"Logout",
            "viewclass": "OneLineListItem",
            "on_release": 
                lambda x=f"Logout": self.logout(),
        }]
        
        #Initialize the DropdownMenu using the menu_items as content, 
        # and button_caller as position from which the menu will open.
        self.menu = MDDropdownMenu(
            caller=button_caller,  #
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()
        
    def logout(self):
        """
        Actual logout method. Removes the content of LoggedUser.json and switches batch to login screen
        """
        self.menu.dismiss()
        self.store.delete('UserInfo')
        self.screen_manager.transition=NoTransition()
        self.screen_manager.current = 'login_screen'
    ####################################################
    
    
    
    
    ###################################################
    #                                                 #      
    #              DATABASE METHODS                   #  
    #                                                 #
    ###################################################
    def login_account(self):
        """
        Validate username and password from user input. If the value of login_complete
        is true, generate a Login Success dialogbox, otherwise, prompt that username and password 
        not found.
        """
        
        input_username = self.ids.log_username.text.strip()
        input_password = self.ids.log_password.pass_text.text.strip()
        
        login_complete = self.check_user(input_username,input_password)
        if login_complete: 
            self.display_dialog("Login Success!")
            self.screen_manager.current = "dashboard_screen" 
            self.screen_manager.transition.direction = "up" 
        else:
            self.display_dialog("Username & password not found")
        
    def register_account(self,app):
        """
        Validate registration fields using input_validate function. If the value of reg_complete
        is true, generate a Registration Success dialogbox, otherwise, prompt that an error message.
        """
        
        if self.input_validate():
            reg_complete = self.add_user() #insert record to database
            if reg_complete: 
                self.display_dialog("", True)
            else:
                self.display_dialog("Error inserting records")
    
    def add_user(self):
        """
            Insert new user information to database
        """
        self.dbconn = sqlite3.connect('kivysql.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = self.dbconn.cursor()
        
        database_params = {
				'var_username'  : self.ids.username.text.strip(),
                'var_firstname' : self.ids.firstname.text.strip(),
                'var_lastname'  : self.ids.lastname.text.strip(),
                'var_email'     : self.ids.email.text.strip(),
                'var_password'  : self.password_encode(self.ids.password.pass_text.text.strip()),
                'var_created_at': datetime.now(),
                'var_updated_at': datetime.now(),
			}
        dbcursor.execute("INSERT INTO mstuser (username,first_name,last_name,email,password,created_at,updated_at) VALUES (:var_username,:var_firstname,:var_lastname,:var_email,:var_password,:var_created_at,:var_updated_at)",database_params)
        #check if NO RECORD is created, return False(ERROR)
        if(dbcursor.rowcount < 1):
            print("No record created")
            return False
        else:
            #print("Commit " + dbcursor.rowcount )
            self.dbconn.commit()
            self.dbconn.close()
            return True    
    
    def check_user(self,input_username,input_password):
        """
            Verify username and password if record in database
        """
        self.dbconn = sqlite3.connect('kivysql.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = self.dbconn.cursor()
        
        sql_query = """SELECT * FROM mstuser WHERE username = :var_username AND password = :var_password"""
        parameter = {'var_username': input_username,'var_password':self.password_encode(input_password)}
        dbcursor.execute(sql_query,parameter)
        
        records = dbcursor.fetchall()
        #check if NO RECORD is created, return False(ERROR)
        
        if not records: #if no record exist
            print("No record created")
            return False
        else:
            for user in records:
                
                """
                Save login user code, firstname,lastname and username to a json file
                """
                self.store.put('UserInfo',code=user[0],firstname=user[2],lastname=user[3],username=user[1])
                
            self.dbconn.commit()
            self.dbconn.close()
            return True
    
    def load_posts(self,widget_type = None):
        """
        Load all Posts record created by the logged-in user. Receives widget_type that is either null 
        or default to "swipe" for swipe cards
        """
        self.dbconn = sqlite3.connect('kivysql.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = self.dbconn.cursor()
        
        
        if widget_type == "swipe":
            user_code = self.store.get('UserInfo')['code'] 
            sql_query = """SELECT * FROM trnpost WHERE user_mst_code = :var_user_code ORDER BY trnpost.created_at DESC """
            parameter = {'var_user_code': user_code}
            dbcursor.execute(sql_query,parameter)
         
        else:
            sql_query = """SELECT * FROM trnpost  ORDER BY trnpost.created_at DESC """
            dbcursor.execute(sql_query)
            
        records = dbcursor.fetchall()
        if not records: #if no record exist
            print("No record created")
        else:
            self.ids.screen4_boxlayout.clear_widgets()
            self.ids.screen5_boxlayout.clear_widgets()
            for post in records:
                if widget_type == "swipe":
                    #Display a Swipe to delete List with rec_id(primary of post record),Post title, user and date posted, and post content
                    self.ids.screen5_boxlayout.add_widget(SwipeToDeleteItem(rec_id=post[0],
                                                                    text=post[2],
                                                                    secondary_text=f'[size=12sp]posted by: {post[5]} · {self.datetime_difference(post[7])}[/size]', 
                                                                    tertiary_text=post[3],
                                                                    on_touch_down=self.view_post))
                elif widget_type is None:
                    #Display a 3 line list item: Post title, user and date posted, and post content
                    self.ids.screen4_boxlayout.add_widget(CustomThreeLineListItem(
                                    rec_id=post[0],
                                    text=f'[size=18sp][b]{post[2]}[/b][/size]',
                                    secondary_text=f'[size=12sp]posted by: {post[5]} · {self.datetime_difference(post[7])}[/size]',                                        
                                    tertiary_text=post[3],
                                    on_touch_down=self.view_post
                                    ))
        self.dbconn.commit()
        self.dbconn.close()
    
    def insert_post(self,app):
        """
        Post a record to database. Then return to dashboard screen with
        toast.
        """
        title = self.ids.p_title.text.strip()       
        body = self.ids.p_body.text.strip()
        
        post_status = self.post_validate(title,body)
        if post_status["success"]: #if the return dictionary success key is TRUE
            self.dbconn = sqlite3.connect('kivysql.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            dbcursor = self.dbconn.cursor()
            
            database_params = {
                    'var_user_code': self.store.get('UserInfo')['code'],
                    'var_title'  : title,
                    'var_body' : body,
                    'var_created_by': self.store.get('UserInfo')['firstname']+ " " +self.store.get('UserInfo')['lastname'],
                    'var_updated_by': self.store.get('UserInfo')['firstname']+ " " +self.store.get('UserInfo')['lastname'],
                    'var_created_at': datetime.now(),
                    'var_updated_at': datetime.now(),
                }
            dbcursor.execute("INSERT INTO trnpost (user_mst_code,title,body,created_by,updated_by,created_at,updated_at) VALUES (:var_user_code,:var_title,:var_body,:var_created_by,:var_updated_by,:var_created_at,:var_updated_at)",database_params)
            #check if NO RECORD is created, return False(ERROR)
            if(dbcursor.rowcount < 1):
                print("No record created")
                self.dbconn.close()
            else:
                #print("Commit " + dbcursor.rowcount )
                self.dbconn.commit()
                self.dbconn.close()
                self.screen_manager.current = 'dashboard_screen'
                self.screen_manager.transition.direction = "right" 
                self.bottom_navigation.switch_tab('screen 1') 
                
                #Snackbar - create popup message after successful posting
                Snackbar(
                    text="Successfully posted a record!",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                    bg_color=app.theme_cls.accent_color
                ).open()
        
            
        else:
            self.display_dialog(post_status["remarks"]) #display the remarks message in post_validate() status return
    
    def load_selected_post(self):
        """
        Load selected post. This function is called by on_enter: root.load_selected_post() in .kv file 
        Assign the title and body to MDLabels for viewing
        """
        
        self.dbconn = sqlite3.connect('kivysql.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = self.dbconn.cursor()
        post_id = self.ids.viewpost_screen.rec_id
        
        
        #user_code = self.store.get('UserInfo')['code'] 
        sql_query = """SELECT title, body,created_by,created_at FROM trnpost WHERE code = :post_id """
        parameter = {'post_id': post_id}
        dbcursor.execute(sql_query,parameter)
        records = dbcursor.fetchall()
        if not records: #if no record exist
            print("No record created")
        else:
            self.ids.title_post.text = ''
            self.ids.body_post.text = ''   
            for post in records:
                self.ids.title_post.text = post[0]
                self.ids.body_post.text = post[1]  
                self.ids.postby_post.text = f'Posted by {post[2]} · {self.datetime_difference(post[3])}'   
    ####################################################       
      
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

class CustomThreeLineListItem(ThreeLineListItem):
    rec_id = NumericProperty()
    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text=StringProperty()
    
class SwipeToDeleteItem(MDCardSwipe):
    rec_id = NumericProperty()
    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text=StringProperty()
    
    dbconn    = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.store = JsonStore("loggedUser.json")
        
    def remove_item(self,record_id):
        """
        Remove SwipeToDeleteItem in screen
        """
        widgetToRemove = list(filter(lambda child: child.rec_id == record_id, self.parent.children))
        for child_widget in widgetToRemove:
            self.delete_record(record_id)
            self.parent.remove_widget(child_widget)
            
    def delete_record(self,record_id):
        """
        Remove the actual record in the database base from record_id parameter
        """
        self.dbconn = sqlite3.connect('kivysql.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = self.dbconn.cursor()
        
        sql_query = """DELETE FROM trnpost WHERE code = :rec_id AND user_mst_code = :var_user_code """
        parameter = {'rec_id': record_id,'var_user_code': self.store.get('UserInfo')['code']}
        dbcursor.execute(sql_query,parameter)
        #check if NO RECORD is created, return False(ERROR)
        if(dbcursor.rowcount == 1):
            toast("Post has been deleted")
        else:
            toast("Post does not exist. Please reload the screen")
            #print("Commit " + dbcursor.rowcount 
        self.dbconn.commit()
        self.dbconn.close()


class ViewPostScreen(Screen):
    post_id = None
    caller_screen = None
    rec_id = NumericProperty()
    def assign_post_id(self,param_post_id,screen_name):
        """
        Called by view_post method in MainLayout Class to receive post_id 
        when viewing post
            Arguments:
                param_post_id(int): post id to view
                screen_name(str)  : fall back screen when closing the view post screen
        """
        self.post_id = param_post_id
        self.caller_screen = screen_name
        self.rec_id = param_post_id
         
    
    
class mdScrollViewApp(MDApp):

    def build(self):
            self.theme_cls.material_style = "M3"    
            self.theme_cls.theme_style    = "Light"
            self.theme_cls.primary_palette= "Blue"
            self.theme_cls.accent_palette = "Teal"
            return MainLayout()  
        
        
    
      
if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    mdScrollViewApp().run()