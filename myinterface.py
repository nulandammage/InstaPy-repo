import sys
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
#from InstaBot import InstaBot
#from secrets import username


#my_bot = InstaBot(username=username)
#names = my_bot.not_following
names = [str(i) for i in range(10)]

class PopupLayout(FloatLayout):

    def __init__(self, info, right_btn, left_btn, **kwargs):
        super(PopupLayout, self).__init__(**kwargs)
        self.info = Label(text=info, size_hint=(.6, 1), pos_hint={'center_x': .5, 'center_y': .5})
        self.right_button = Button(text=right_btn, size_hint=(.3, .1), pos_hint={'center_x': .8, 'center_y': .2})
        self.left_button = Button(text=left_btn, size_hint=(.3, .1), pos_hint={'center_x': .2, 'center_y': .2})
        self.left_button.bind(on_press=self.close_screen)
        self.add_widget(self.info)
        self.add_widget(self.left_button)
        self.add_widget(self.right_button)

    @staticmethod
    def close_screen(instance):
        sys.exit()


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        self.bad_people = []

        self.scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, pos_hint={'center_x': .5, 'center_y': .5})
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))

        for user in names:
            self.user = Label(text=user, size_hint=(None, None), size=(300, 100))
            self.select_box = CheckBox(size_hint=(None, None), size=(100, 100))
            self.select_box.bind(on_press=self.add_to_list)
            self.name_space = BoxLayout(size_hint=(None, None))
            self.name_space.add_widget(self.user)
            self.name_space.add_widget(self.select_box)
            self.scroll_layout.add_widget(self.name_space)

        self.root = ScrollView(size_hint=(None, None), size=(500, 400))
        self.root.add_widget(self.scroll_layout)

        self.unfollow_button = Button(text='Unfollow Selected users', size_hint=(None, None),
                                      pos_hint={'center_x': .5, 'center_y': .5}, size=(300, 50))
        self.unfollow_button.bind(on_press=self.show_users)
        self.add_widget(self.root)
        self.add_widget(self.unfollow_button)

    def add_to_list(self, instance):
        name = instance.parent.children[1].text
        if instance.active:
            if name not in self.bad_people:
                self.bad_people.append(name)
        else:
            self.bad_people.remove(name)

    def show_users(self, instance):
        content = PopupLayout(info='Are You Sure you want to unfollow the users',
                              right_btn='No', left_btn='Yes')
        popup = Popup(title='Test popup',
                      content=content,
                      size_hint=(None, None), size=(400, 400),
                      auto_dismiss=False)
        for item in content.children:
            if item.text == 'No':
                item.bind(on_press=popup.dismiss)
        popup.open()


class MainApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    MainApp().run()
