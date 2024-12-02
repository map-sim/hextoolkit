from ObjPainter import AbstractPainter


class UnitPainter(AbstractPainter):        
    def draw(self, context, own):
        for vex, units in self.saver.units.items():
            color, symbol, size = self.estimate_unit(units, own)
            if size == 0: continue
            self.draw_unit_envelop(context, vex, color)
            self.draw_unit_label(context, vex, symbol, size)
            
    def estimate_unit(self, units, own=None):
        if own:
            fown = lambda unit: unit["own"] == own
            units = list(filter(fown, units))
        size = 0; letters = []; backend = True
        for unit in units:
            size += unit["size"]
            letter = self.saver.xsystem[unit["type"]]["char"]
            letters.extend(unit["size"] * [letter])
            if letter != "S" and letter != "E": backend = False
        if len(set(letters)) == 0: return None, None, 0
        elif len(set(letters)) == 1: letter = letters[0]
        elif backend: letter = "B"
        else: letter = "X"
        own = units[0]["own"]
        color = self.saver.controls[own]["unit-color"] 
        return color, letter, size

    def draw_unit_label(self, context, vex, symbol, size):
        r = self.saver.settings.get("hex-radius", 1.0)
        zoom = self.saver.settings["window-zoom"]
        loc = AbstractPainter.vex_to_loc(vex, r)                
        xo, yo = self.translate_xy(*loc)
        if size < 10: context.move_to(xo-0.45*zoom, yo+0.25*zoom)
        else: context.move_to(xo-0.7*zoom, yo+0.25*zoom)
        context.set_font_size(0.66*zoom)
        context.set_source_rgba(0, 0, 0)
        context.show_text(f"{symbol}{size}")
        context.fill()

    def draw_unit_envelop(self, context, vex, color):
        r = self.saver.settings.get("hex-radius", 1.0)
        zoom = self.saver.settings["window-zoom"]
        loc = AbstractPainter.vex_to_loc(vex, r)                
        xo, yo = self.translate_xy(*loc)

        context.set_source_rgba(1, 1, 1)
        context.move_to(xo - 0.8 * zoom, yo + 0.6 * zoom)
        context.line_to(xo + 0.8 * zoom, yo + 0.6 * zoom)
        context.line_to(xo + 0.8 * zoom, yo - 0.6 * zoom)
        context.line_to(xo - 0.8 * zoom, yo - 0.6 * zoom)
        context.line_to(xo - 0.8 * zoom, yo + 0.6 * zoom)
        context.fill()

        context.set_source_rgba(0, 0, 0)
        context.move_to(xo - 0.77 * zoom, yo + 0.57 * zoom)
        context.line_to(xo + 0.77 * zoom, yo + 0.57 * zoom)
        context.line_to(xo + 0.77 * zoom, yo - 0.57 * zoom)
        context.line_to(xo - 0.77 * zoom, yo - 0.57 * zoom)
        context.line_to(xo - 0.77 * zoom, yo + 0.57 * zoom)
        context.fill()

        context.set_source_rgba(*color)
        context.move_to(xo - 0.74 * zoom, yo + 0.54 * zoom)
        context.line_to(xo + 0.74 * zoom, yo + 0.54 * zoom)
        context.line_to(xo + 0.74 * zoom, yo - 0.54 * zoom)
        context.line_to(xo - 0.74 * zoom, yo - 0.54 * zoom)
        context.line_to(xo - 0.74 * zoom, yo + 0.54 * zoom)
        context.fill()
