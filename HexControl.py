import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class HexControl(Gtk.Window):
    def __init__(self, main_window):
        Gtk.Window.__init__(self, title="Control")
        self.add_events(Gdk.EventMask.SCROLL_MASK)
        self.connect("scroll-event", self.on_scroll)

        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.main_window = main_window

        self.last_button = None
        self.button_key_mapping = {}
        self.grid = Gtk.Grid()
        self.add(self.grid)
        
        self.make_key_button("_ESC", "Escape")
        self.make_key_button("Zoom-in", "plus")
        self.make_key_button("Zoom-out", "minus")
        self.make_key_button("Left", "Left")
        self.make_key_button("Up", "Up")
        self.make_key_button("Down", "Down")
        self.make_key_button("Right", "Right")
        
        self.make_key_button("_Save", "s", (0, 1, 1, 1))
        self.show_all()

    def on_scroll(self, widget, event):
        self.main_window.on_scroll(widget, event)
        
    def make_key_button(self, label, key, coor=None):
        button = Gtk.Button.new_with_mnemonic(label)
        button.connect("clicked", self.on_click_button)
        self.button_key_mapping[label] = key
        if coor is None and self.last_button is None: self.grid.add(button)
        elif coor is None: self.grid.attach_next_to(button, self.last_button, Gtk.PositionType.RIGHT, 1, 1)
        else: self.grid.attach(button, *coor)
        self.last_button = button

    def on_click_button(self, button):
        label = button.get_label()
        key = self.button_key_mapping[label]
        self.main_window.on_press(None, key)
