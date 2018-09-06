# TODO: Add documentation.

from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView

from kivymd.backgroundcolorbehavior import SpecificBackgroundColorBehavior
from kivymd.button import MDIconButton
from kivymd.theming import ThemableBehavior

Builder.load_string("""
#:import Window kivy.core.window.Window
#:import StiffScrollEffect kivymd.stiffscroll.StiffScrollEffect


<ModifiedToolbar>
    size_hint_y: None
    height: root.theme_cls.standard_increment
    padding: [root.theme_cls.horizontal_margins - dp(12), 0]

    BoxLayout:
        id: left_actions
        orientation: 'horizontal'
        size_hint_x: None
        padding: [0, (self.height - dp(48))/2]

    BoxLayout:
        padding: dp(12), 0
        MDLabel:
            font_style: 'Title'
            opposite_colors: root.opposite_colors
            theme_text_color: 'Custom'
            text_color: root.specific_text_color
            text: root.title
            shorten: True
            shorten_from: 'right'

    BoxLayout:
        id: right_actions
        orientation: 'horizontal'
        size_hint_x: None
        padding: [0, (self.height - dp(48))/2]


<UserAnimationCard>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos

    Image:
        id: image
        source: root.path_to_avatar
        size_hint: 1, None
        height: Window.height * 40 // 100
        y: Window.height - self.height
        allow_stretch: True
        keep_ratio: False

        canvas:
            Color:
                rgba: root._primary_color
            Rectangle:
                size: self.size
                pos: self.pos

    MDLabel:
        id: user_name
        font_style: 'Display1'
        theme_text_color: 'Custom'
        color: 1, 1, 1, 1
        shorten: True
        shorten_from: 'right'
        text: root.user_name
        y: Window.height - image.height
        x: dp(15)
        size_hint_y: None
        height: self.texture_size[1]

    ModifiedToolbar:
        id: toolbar
        md_bg_color: 0, 0, 0, 0
        left_action_items: [['arrow-left', lambda x: root._callback_back()]]
        y: Window.height - self.height

    ScrollView:
        id: scroll
        y: -image.height
        effect_cls: StiffScrollEffect
        scroll_distance: 100
    
        GridLayout:
            id: box_content
            size_hint_y: None
            height: self.minimum_height
            cols: 1
            canvas:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
""")


class MDUserAnimationCard(ThemableBehavior, ModalView):
    user_name = StringProperty()
    path_to_avatar = StringProperty()
    box_content = ObjectProperty()
    callback = ObjectProperty()
    _anim_bottom = True

    def __init__(self, **kwargs):
        super(MDUserAnimationCard, self).__init__(**kwargs)
        self._primary_color = self.theme_cls.primary_color
        self._primary_color[3] = 0
        self.user_animation_card = UserAnimationCard(
            user_name=self.user_name,
            path_to_avatar=self.path_to_avatar,
            _callback_back=self._callback_back,
            _primary_color=self._primary_color)
        self.box_content = self.user_animation_card.ids.box_content
        self.add_widget(self.user_animation_card)

        self._obj_avatar = self.user_animation_card.ids.image
        self._obj_user_name = self.user_animation_card.ids.user_name
        self._obj_toolbar = self.user_animation_card.ids.toolbar
        self._obj_scroll = self.user_animation_card.ids.scroll
        self._set_current_pos_objects()

    def _callback_back(self):
        self.dismiss()
        if self.callback:
            self.callback()

    def on_open(self):
        self._primary_color = self.theme_cls.primary_color
        self._primary_color[3] = 0
        self.user_animation_card._primary_color = self._primary_color

    def _set_current_pos_objects(self):
        self._avatar_y = self._obj_avatar.y
        self._toolbar_y = self._obj_toolbar.y
        self._user_name_y = self._obj_user_name.y
        self._scroll_y = self._obj_scroll.y

    def on_touch_move(self, touch):
        if touch.ud['swipe_begin'] < touch.y:
            if self._anim_bottom:
                self._anim_bottom = False
                self.animation_to_top()
        else:
            if not self._anim_bottom:
                self._anim_bottom = True
                self.animation_to_bottom()

    def on_touch_down(self, touch):
        touch.ud['swipe_begin'] = touch.y
        return super(MDUserAnimationCard, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        touch.ud['swipe_begin'] = 0

    def animation_to_bottom(self):
        Animation(y=self._scroll_y, d=.4, t='in_out_cubic').start(
            self._obj_scroll)
        Animation(y=self._user_name_y, d=.5, x=dp(15), t='in_out_cubic').start(
            self._obj_user_name)
        Animation(font_size=sp(36), d=.3, t='in_out_cubic').start(
            self._obj_user_name)
        Animation(y=self._avatar_y, d=.4, t='in_out_cubic').start(
            self._obj_avatar)
        Animation(a=0, d=.4, t='in_out_cubic').start(
            self._obj_avatar.canvas.children[3])

    def animation_to_top(self):
        user_name_y = Window.height - self._obj_toolbar.height + (
                self.theme_cls.standard_increment // 2 - dp(12))
        user_name_x = self.theme_cls.horizontal_margins + dp(12) * 5

        Animation(y=-self._obj_toolbar.height, d=.4, t='in_out_cubic').start(
            self.user_animation_card.ids.scroll)
        Animation(y=user_name_y, d=.3, x=user_name_x, t='in_out_cubic').start(
            self._obj_user_name)
        Animation(font_size=sp(20), d=.3, t='in_out_cubic').start(
            self._obj_user_name)
        Animation(y=self._obj_avatar.y + 30, d=.4, t='in_out_cubic').start(
            self._obj_avatar)
        Animation(a=1, d=.4, t='in_out_cubic').start(
            self._obj_avatar.canvas.children[3])


class UserAnimationCard(ThemableBehavior, FloatLayout):
    user_name = StringProperty()
    path_to_avatar = StringProperty()
    _callback_back = ObjectProperty()
    _primary_color = ListProperty()


class ModifiedToolbar(ThemableBehavior, SpecificBackgroundColorBehavior,
                      BoxLayout):
    left_action_items = ListProperty()
    title = StringProperty()

    def __init__(self, **kwargs):
        super(ModifiedToolbar, self).__init__(**kwargs)
        self.bind(specific_text_color=self.update_action_bar_text_colors)
        Clock.schedule_once(
            lambda x: self.on_left_action_items(0, self.left_action_items))

    def on_left_action_items(self, instance, value):
        self.update_action_bar(self.ids['left_actions'], value)

    def update_action_bar(self, action_bar, action_bar_items):
        action_bar.clear_widgets()
        new_width = 0
        for item in action_bar_items:
            new_width += dp(48)
            action_bar.add_widget(
                MDIconButton(icon=item[0], on_release=item[1],
                             opposite_colors=True,
                             text_color=self.specific_text_color,
                             theme_text_color='Custom'))
        action_bar.width = new_width

    def update_action_bar_text_colors(self, instance, value):
        for child in self.ids['left_actions'].children:
            child.text_color = self.specific_text_color