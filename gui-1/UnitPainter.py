from ObjPainter import AbstractPainter


class UnitPainter(AbstractPainter):        
    def draw(self, context):
        for vex, units in self.saver.units.items():
            own, symbol, size = self.estimate_unit(*units)
            if symbol == "infantry": self.draw_unit_infantry(context, vex, own, size)
            else: raise ValueError(f"Not supported unit type: {unit['type']}")

    def estimate_unit(self, *units):
        return units[0]["own"], units[0]["type"], 1

    def draw_unit_size(self, context, vex, size):
        r = self.saver.settings.get("hex-radius", 1.0)
        zoom = self.saver.settings["window-zoom"]
        loc = AbstractPainter.vex_to_loc(vex, r)                
        xo, yo = self.translate_xy(*loc)

    def draw_unit_infantry(self, context, vex, own, size):
        r = self.saver.settings.get("hex-radius", 1.0)
        zoom = self.saver.settings["window-zoom"]
        color = self.saver.controls[own]["unit-color"]
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

        self.draw_unit_size(context, vex, size)
