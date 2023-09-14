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
        self.connect("key-press-event",self.on_press)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.main_window = main_window

        self.last_button = None
        self.button_key_mapping = {}
        self.grid = Gtk.Grid()
        self.add(self.grid)
        
        self.make_key_button("ESC", "Escape")
        self.make_key_button("Zoom-in", "plus")
        self.make_key_button("Zoom-out", "minus")
        self.make_key_button("Left", "Left")
        self.make_key_button("Up", "Up")
        self.make_key_button("Down", "Down")
        self.make_key_button("Right", "Right")
        
        self.make_key_button("Save", "s", (0, 1, 1, 1))
        self.make_key_button("<", "less")
        self.make_key_button(">", "greater")
        self.make_key_button("Load", "l")
        nargs = Gtk.PositionType.RIGHT, 1, 1
        nargs2 = Gtk.PositionType.RIGHT, 2, 1
        self.snapshot_label = Gtk.Label()
        self.grid.attach_next_to(self.snapshot_label, self.last_button, *nargs)
        self.refresh_snapshot_label()

        self.make_key_button("Unselect", "grave", (0, 2, 1, 1))
        title_vex_label = Gtk.Label()
        self.grid.attach_next_to(title_vex_label, self.last_button, *nargs)
        title_vex_label.set_markup("Selection:")
        self.vex_label = Gtk.Label()
        self.grid.attach_next_to(self.vex_label, title_vex_label, *nargs)
        self.refresh_vex_label()
        self.selected_terr_label = Gtk.Label()
        self.grid.attach_next_to(self.selected_terr_label, self.vex_label, *nargs2)
        self.refresh_selected_terr_label(None)

        self.make_key_button("Terr-toogle", "t", (0, 3, 1, 1))
        self.make_key_button("Terr-set", "T")
        self.terr_label = Gtk.Label()
        self.grid.attach_next_to(self.terr_label, self.last_button, *nargs2)
        self.refresh_terr_label()

        self.make_key_button("Obj-toogle", "o", (0, 4, 1, 1))
        self.make_key_button("Obj-set", "O")
        self.obj_label = Gtk.Label()
        self.grid.attach_next_to(self.obj_label, self.last_button, *nargs)
        self.refresh_obj_label()

        self.show_all()

    def refresh_snapshot_label(self):
        snapshot = self.main_window.state["game-index"]
        if snapshot is None: self.snapshot_label.set_markup("--")
        else: self.snapshot_label.set_markup(str(snapshot))
    def refresh_vex_label(self):
        vex = self.main_window.painter.selected_vex
        if vex is None: self.vex_label.set_markup("--")
        else: self.vex_label.set_markup(f"{vex[0]} : {vex[1]}")
    def refresh_terr_label(self):
        terr = self.main_window.state["selected-terr"]
        if terr is None: self.terr_label.set_markup("--")
        else: self.terr_label.set_markup(str(terr))
    def refresh_selected_terr_label(self, terr):
        if terr is None: self.selected_terr_label.set_markup("--")
        else: self.selected_terr_label.set_markup(str(terr))
    def refresh_obj_label(self):
        obj = self.main_window.state["selected-obj"]
        if obj is None: self.obj_label.set_markup("--")
        else: self.obj_label.set_markup(str(obj))
    
    def on_press(self, widget, event):
        self.main_window.on_press(widget, event)
    def on_scroll(self, widget, event):
        self.main_window.on_scroll(widget, event)
        
    def make_key_button(self, label, key, coor=None):
        button = Gtk.Button.new_with_label(label)
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
