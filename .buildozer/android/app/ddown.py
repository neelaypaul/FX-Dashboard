from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivymd.uix.textfield import MDTextFieldRound, MDTextField, MDTextFieldRect
import json

Clock.max_iteration = 20

with open('Common-Currency.json', encoding='utf-8') as f:
    countries = json.load(f)

cntry_name_lst = [countries[x]['code'] + '-' + countries[x]['name_plural'] for x in countries]




KV = '''
<MyMDTextField>:
    readonly: True
    font_size:'14sp'
    icon_right: "arrow-down-drop-circle-outline"
    icon_right_color: app.theme_cls.primary_color
    color_mode: 'custom'
    line_color_focus: 0, 0, 0, 1

<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (1, 1, 1, 0)
        Rectangle:
            pos: self.pos
            size: self.size
<Content>

    orientation: "vertical"
    spacing: "8dp"
    size_hint_y: None
    height: "200dp"



    MDBoxLayout:
        adaptive_height: True
        MDIconButton:
            icon: 'magnify'

        MDTextField:
            id: search_field
            hint_text: 'Search'
            on_text: root.set_list_md_icons(self.text, True)

    RecycleView:
        id: rv
        viewclass: 'SelectableLabel'
        key_size: 'height'


        SelectableRecycleBoxLayout:
            padding: dp(10)
            default_size: None, dp(48)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            multiselect: False
            touch_multiselect: False
'''

Builder.load_string(KV)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, MDLabel):
    event = None
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''

        self.selected = is_selected
        if is_selected:

            self.event = Clock.schedule_once(lambda x: x, 0.5)
            if App.get_running_app().dialog != None:
                App.get_running_app().dialog.dismiss()
                App.get_running_app().dialog = None

            getattr(App.get_running_app().root.ids, App.get_running_app().dd.lower()).text = str(
                rv.data[index]['text'])[:3]


class Content(BoxLayout):
    lst = None

    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''

        def add_icon_item(name_icon):
            self.ids.rv.data.append(
                {

                    "text": name_icon
                }
            )

        self.ids.rv.data = []
        for name_icon in self.lst:
            if search:
                if text.lower() in name_icon.lower():
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)


class MyMDTextField(MDTextField):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.icon_right:
                # icon position based on the KV code for MDTextField
                icon_x = (self.width + self.x) - (self._lbl_icon_right.texture_size[1]) - dp(8)
                icon_y = self.center[1] - self._lbl_icon_right.texture_size[1] / 2

                # not a complete bounding box test, but should be sufficient
                if touch.pos[0] > icon_x and touch.pos[1] > icon_y:
                    Clock.schedule_once(lambda x: x)

                    App.get_running_app().show_confirmation_dialog()

        return super(MyMDTextField, self).on_touch_down(touch)

