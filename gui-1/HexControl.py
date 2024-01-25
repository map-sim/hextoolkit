import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class HexControl(Gtk.Window):
    def on_press(self, widget, event):
        self.main_window.on_press(widget, event)
    def on_scroll(self, widget, event):
        self.main_window.on_scroll(widget, event)
    def on_clicked(self, widget):
        value = self.button_mapping[widget.get_label()]
        self.main_window.on_press(widget, value)
    def make_button(self, vbox, label, value):
        button = Gtk.Button(label=label)
        button.connect("clicked", self.on_clicked)
        self.button_mapping[button.get_label()] = value
        vbox.pack_start(button, False, True, 0)

    
        
    def __init__(self, main_window):
        Gtk.Window.__init__(self, title="Control")
        self.add_events(Gdk.EventMask.SCROLL_MASK)
        self.connect("scroll-event", self.on_scroll)
        self.connect("key-press-event",self.on_press)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.main_window = main_window
        self.button_mapping = {}        
        self.box = Gtk.Box(spacing=3)
        self.add(self.box)

        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)
        
        self.make_button(vbox, "Reset (ESC)", "Escape")
        self.make_button(vbox, "ZOOM in", "plus")
        self.make_button(vbox, "ZOOM out", "minus")
        self.make_button(vbox, "Move Up", "Up")
        self.make_button(vbox, "Move Down", "Down")
        self.make_button(vbox, "Move --->", "Right")
        self.make_button(vbox, "Move <---", "Left")
        
        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)

        self.make_button(vbox, "Un-Select (q)", "q")
        self.make_button(vbox, "Save (s)", "s")

        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)
        self.info = Gtk.Label(label="???")
        self.info.set_line_wrap(True)
        self.info.set_max_width_chars(32)
        self.info.set_selectable(True)
        vbox.pack_start(self.info, True, True, 0)
        
        self.show_all()

