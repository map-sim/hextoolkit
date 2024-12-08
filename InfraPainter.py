from ObjPainter import AbstractPainter
from ObjPainter import TWO_PI


class InfraPainter(AbstractPainter):
    def draw(self, context):
        for vex, infra in self.saver.infra.items():
            for i, item in enumerate(infra):
                if item is None: continue
                if item["type"] == "airhub": self.draw_infra_airhub(context, vex, i, **item)
                elif item["type"] == "seahub": self.draw_infra_port(context, vex, i, **item)
                elif item["type"] == "plant": self.draw_infra_plant(context, vex, i, **item)
                elif item["type"] == "supply": self.draw_infra_tech(context, vex, i, **item)
                elif item["type"] == "fort": self.draw_infra_fort(context, vex, i, **item)
                elif item["type"] == "unit": self.draw_infra_unit(context, vex, i, **item)
                elif item["type"] == "link": self.draw_infra_link(context, vex, i, **item)
                else: raise ValueError(f"Not supported infra type: {item['type']}")

    def __to_slot(self, xo, yo, r, i):
        if i == 0: return xo, yo + 0.74 * r
        elif i == 1: return xo, yo - 0.74 * r
        elif i == 2: return xo + 0.63 * r, yo - 0.37 * r
        elif i == 3: return xo - 0.63 * r, yo - 0.37 * r
        elif i == 4: return xo + 0.63 * r, yo + 0.37 * r
        elif i == 5: return xo - 0.63 * r, yo + 0.37 * r
        
    def draw_infra_fort(self, context, vex, index, own, **item): 
        r = self.saver.settings.get("hex-radius", 1.0)
        zoom = self.saver.settings["window-zoom"]
        color = self.saver.controls[own]["base-color"]
        loc = AbstractPainter.vex_to_loc(vex, r)                
        xo, yo = self.translate_xy(*loc)
        xo, yo = self.__to_slot(xo, yo, zoom*r, index)

        context.set_source_rgba(1, 1, 1)
        context.move_to(xo - 0.32 * zoom, yo + 0.32 * zoom)
        context.line_to(xo + 0.32 * zoom, yo + 0.32 * zoom)
        context.line_to(xo + 0.32 * zoom, yo - 0.32 * zoom)
        context.line_to(xo - 0.32 * zoom, yo - 0.32 * zoom)
        context.line_to(xo - 0.32 * zoom, yo + 0.32 * zoom)
        context.fill()

        context.set_source_rgba(0, 0, 0)
        context.move_to(xo - 0.29 * zoom, yo + 0.29 * zoom)
        context.line_to(xo + 0.29 * zoom, yo + 0.29 * zoom)
        context.line_to(xo + 0.29 * zoom, yo - 0.29 * zoom)
        context.line_to(xo - 0.29 * zoom, yo - 0.29 * zoom)
        context.line_to(xo - 0.29 * zoom, yo + 0.29 * zoom)
        context.fill()

        context.set_source_rgba(*color)
        context.move_to(xo - 0.26 * zoom, yo + 0.26 * zoom)
        context.line_to(xo + 0.26 * zoom, yo + 0.26 * zoom)
        context.line_to(xo + 0.26 * zoom, yo - 0.26 * zoom)
        context.line_to(xo - 0.26 * zoom, yo - 0.26 * zoom)
        context.line_to(xo - 0.26 * zoom, yo + 0.26 * zoom)
        context.fill()

    def draw_infra_link(self, context, vex, index, own, **item): 
        r = self.saver.settings.get("hex-radius", 1.0)
        zoom = self.saver.settings["window-zoom"]
        color = self.saver.controls[own]["base-color"]
        loc = AbstractPainter.vex_to_loc(vex, r)                
        xo, yo = self.translate_xy(*loc)
        xo, yo = self.__to_slot(xo, yo, zoom*r, index)

        context.set_source_rgba(1, 1, 1)
        context.move_to(xo - 0.32 * zoom, yo - 0.08 * zoom)
        context.line_to(xo + 0.32 * zoom, yo + 0.32 * zoom)
        context.line_to(xo + 0.32 * zoom, yo + 0.08 * zoom)
        context.line_to(xo - 0.32 * zoom, yo - 0.32 * zoom)
        context.line_to(xo - 0.32 * zoom, yo - 0.08 * zoom)
        context.fill()
        context.move_to(xo - 0.32 * zoom, yo + 0.08 * zoom)
        context.line_to(xo + 0.32 * zoom, yo - 0.32 * zoom)
        context.line_to(xo + 0.32 * zoom, yo - 0.08 * zoom)
        context.line_to(xo - 0.32 * zoom, yo + 0.32 * zoom)
        context.line_to(xo - 0.32 * zoom, yo + 0.08 * zoom)
        context.fill()

        context.set_source_rgba(0, 0, 0)
        context.move_to(xo - 0.29 * zoom, yo + 0.27 * zoom)
        context.line_to(xo + 0.29 * zoom, yo - 0.1 * zoom)
        context.line_to(xo + 0.29 * zoom, yo - 0.27 * zoom)
        context.line_to(xo - 0.29 * zoom, yo + 0.1 * zoom)
        context.line_to(xo - 0.29 * zoom, yo + 0.27 * zoom)
        context.fill()
        context.move_to(xo - 0.29 * zoom, yo - 0.27 * zoom)
        context.line_to(xo + 0.29 * zoom, yo + 0.1 * zoom)
        context.line_to(xo + 0.29 * zoom, yo + 0.27 * zoom)
        context.line_to(xo - 0.29 * zoom, yo - 0.1 * zoom)
        context.line_to(xo - 0.29 * zoom, yo - 0.27 * zoom)
        context.fill()

        context.set_source_rgba(*color)
        context.move_to(xo - 0.26 * zoom, yo + 0.22 * zoom)
        context.line_to(xo + 0.26 * zoom, yo - 0.12 * zoom)
        context.line_to(xo + 0.26 * zoom, yo - 0.22 * zoom)
        context.line_to(xo - 0.26 * zoom, yo + 0.12 * zoom)
        context.line_to(xo - 0.26 * zoom, yo + 0.22 * zoom)
        context.fill()
        context.move_to(xo - 0.26 * zoom, yo - 0.22 * zoom)
        context.line_to(xo + 0.26 * zoom, yo + 0.12 * zoom)
        context.line_to(xo + 0.26 * zoom, yo + 0.22 * zoom)
        context.line_to(xo - 0.26 * zoom, yo - 0.12 * zoom)
        context.line_to(xo - 0.26 * zoom, yo - 0.22 * zoom)
        context.fill()
    
    def draw_infra_port(self, context, vex, index, own, **item): 
        r = self.saver.settings.get("hex-radius", 1.0)
        zoom = self.saver.settings["window-zoom"]
        color = self.saver.controls[own]["base-color"]
        loc = AbstractPainter.vex_to_loc(vex, r)                
        xo, yo = self.translate_xy(*loc)
        xo, yo = self.__to_slot(xo, yo, zoom*r, index)

        context.set_source_rgba(1, 1, 1)
        context.move_to(xo - 0.32 * zoom, yo + 0.32 * zoom)
        context.line_to(xo - 0.07 * zoom, yo + 0.32 * zoom)
        context.line_to(xo - 0.07 * zoom, yo - 0.32 * zoom)
        context.line_to(xo - 0.32 * zoom, yo - 0.32 * zoom)
        context.line_to(xo - 0.32 * zoom, yo + 0.32 * zoom)
        context.fill()
        context.move_to(xo + 0.32 * zoom, yo + 0.32 * zoom)
        context.line_to(xo + 0.07 * zoom, yo + 0.32 * zoom)
        context.line_to(xo + 0.07 * zoom, yo - 0.32 * zoom)
        context.line_to(xo + 0.32 * zoom, yo - 0.32 * zoom)
        context.line_to(xo + 0.32 * zoom, yo + 0.32 * zoom)
        context.fill()
        context.move_to(xo - 0.32 * zoom, yo + 0.32 * zoom)
        context.line_to(xo + 0.32 * zoom, yo + 0.32 * zoom)
        context.line_to(xo + 0.32 * zoom, yo - 0.05 * zoom)
        context.line_to(xo - 0.32 * zoom, yo - 0.05 * zoom)
        context.line_to(xo - 0.32 * zoom, yo + 0.32 * zoom)
        context.fill()

        context.set_source_rgba(0, 0, 0)
        context.move_to(xo - 0.29 * zoom, yo + 0.29 * zoom)
        context.line_to(xo - 0.1 * zoom, yo + 0.29 * zoom)
        context.line_to(xo - 0.1 * zoom, yo - 0.29 * zoom)
        context.line_to(xo - 0.29 * zoom, yo - 0.29 * zoom)
        context.line_to(xo - 0.29 * zoom, yo + 0.29 * zoom)
        context.fill()
        context.move_to(xo + 0.29 * zoom, yo + 0.29 * zoom)
        context.line_to(xo + 0.1 * zoom, yo + 0.29 * zoom)
        context.line_to(xo + 0.1 * zoom, yo - 0.29 * zoom)
        context.line_to(xo + 0.29 * zoom, yo - 0.29 * zoom)
        context.line_to(xo + 0.29 * zoom, yo + 0.29 * zoom)
        context.fill()
        context.move_to(xo - 0.29 * zoom, yo + 0.29 * zoom)
        context.line_to(xo + 0.29 * zoom, yo + 0.29 * zoom)
        context.line_to(xo + 0.29 * zoom, yo - 0.02 * zoom)
        context.line_to(xo - 0.29 * zoom, yo - 0.02 * zoom)
        context.line_to(xo - 0.29 * zoom, yo + 0.29 * zoom)
        context.fill()

        context.set_source_rgba(*color)
        context.move_to(xo - 0.26 * zoom, yo + 0.26 * zoom)
        context.line_to(xo - 0.13 * zoom, yo + 0.26 * zoom)
        context.line_to(xo - 0.13 * zoom, yo - 0.26 * zoom)
        context.line_to(xo - 0.26 * zoom, yo - 0.26 * zoom)
        context.line_to(xo - 0.26 * zoom, yo + 0.26 * zoom)
        context.fill()
        context.move_to(xo + 0.26 * zoom, yo + 0.26 * zoom)
        context.line_to(xo + 0.13 * zoom, yo + 0.26 * zoom)
        context.line_to(xo + 0.13 * zoom, yo - 0.26 * zoom)
        context.line_to(xo + 0.26 * zoom, yo - 0.26 * zoom)
        context.line_to(xo + 0.26 * zoom, yo + 0.26 * zoom)
        context.fill()
        context.move_to(xo - 0.26 * zoom, yo + 0.26 * zoom)
        context.line_to(xo + 0.26 * zoom, yo + 0.26 * zoom)
        context.line_to(xo + 0.26 * zoom, yo + 0.01 * zoom)
        context.line_to(xo - 0.26 * zoom, yo + 0.01 * zoom)
        context.line_to(xo - 0.26 * zoom, yo + 0.26 * zoom)
        context.fill()

    def draw_infra_plant(self, context, vex, index, own, **item):
        r = self.saver.settings.get("hex-radius", 1.0)
        zoom = self.saver.settings["window-zoom"]
        color = self.saver.controls[own]["base-color"]
        loc = AbstractPainter.vex_to_loc(vex, r)
        xo, yo = self.translate_xy(*loc)
        xo, yo = self.__to_slot(xo, yo, zoom*r, index)

        context.set_source_rgba(1, 1, 1)
        context.move_to(xo - 0.42 * zoom, yo + 0.25 * zoom)
        context.line_to(xo + 0.42 * zoom, yo + 0.25 * zoom)
        context.line_to(xo, yo - 0.44 * zoom)
        context.line_to(xo - 0.42 * zoom, yo + 0.25 * zoom)
        context.fill()
        context.move_to(xo - 0.42 * zoom, yo - 0.25 * zoom)
        context.line_to(xo + 0.42 * zoom, yo - 0.25 * zoom)
        context.line_to(xo, yo + 0.44 * zoom)
        context.line_to(xo - 0.42 * zoom, yo - 0.25 * zoom)
        context.fill()

        context.set_source_rgba(0, 0, 0)
        context.move_to(xo - 0.36 * zoom, yo + 0.215 * zoom)
        context.line_to(xo + 0.36 * zoom, yo + 0.215 * zoom)
        context.line_to(xo, yo - 0.38 * zoom)
        context.line_to(xo - 0.36 * zoom, yo + 0.215 * zoom)
        context.fill()
        context.move_to(xo - 0.36 * zoom, yo - 0.215 * zoom)
        context.line_to(xo + 0.36 * zoom, yo - 0.215 * zoom)
        context.line_to(xo, yo + 0.38 * zoom)
        context.line_to(xo - 0.36 * zoom, yo - 0.215 * zoom)
        context.fill()

        context.set_source_rgba(*color)
        context.move_to(xo - 0.3 * zoom, yo + 0.18 * zoom)
        context.line_to(xo + 0.3 * zoom, yo + 0.18 * zoom)
        context.line_to(xo, yo - 0.32 * zoom)
        context.line_to(xo - 0.3 * zoom, yo + 0.18 * zoom)
        context.fill()
        context.move_to(xo - 0.3 * zoom, yo - 0.18 * zoom)
        context.line_to(xo + 0.3 * zoom, yo - 0.18 * zoom)
        context.line_to(xo, yo + 0.32 * zoom)
        context.line_to(xo - 0.3 * zoom, yo - 0.18 * zoom)
        context.fill()

    def draw_infra_airhub(self, context, vex, index, own, **item):
        r = self.saver.settings.get("hex-radius", 1.0)
        zoom = self.saver.settings["window-zoom"]
        color = self.saver.controls[own]["base-color"]
        loc = AbstractPainter.vex_to_loc(vex, r)                
        xo, yo = self.translate_xy(*loc)
        xo, yo = self.__to_slot(xo, yo, zoom*r, index)

        context.set_source_rgba(1, 1, 1)
        context.move_to(xo - 0.32 * zoom, yo + 0.08 * zoom)
        context.line_to(xo + 0.32 * zoom, yo + 0.08 * zoom)
        context.line_to(xo + 0.32 * zoom, yo - 0.24 * zoom)
        context.line_to(xo - 0.32 * zoom, yo - 0.24 * zoom)
        context.line_to(xo - 0.32 * zoom, yo + 0.08 * zoom)
        context.fill()
        context.move_to(xo - 0.16 * zoom, yo + 0.32 * zoom)
        context.line_to(xo + 0.16 * zoom, yo + 0.32 * zoom)
        context.line_to(xo + 0.16 * zoom, yo - 0.32 * zoom)
        context.line_to(xo - 0.16 * zoom, yo - 0.32 * zoom)
        context.line_to(xo - 0.16 * zoom, yo + 0.32 * zoom)
        context.fill()
        context.move_to(xo - 0.22 * zoom, yo + 0.35 * zoom)
        context.line_to(xo + 0.22 * zoom, yo + 0.35 * zoom)
        context.line_to(xo + 0.22 * zoom, yo + 0.13 * zoom)
        context.line_to(xo - 0.22 * zoom, yo + 0.13 * zoom)
        context.line_to(xo - 0.22 * zoom, yo + 0.35 * zoom)
        context.fill()

        context.set_source_rgba(0, 0, 0)
        context.move_to(xo - 0.29 * zoom, yo + 0.05 * zoom)
        context.line_to(xo + 0.29 * zoom, yo + 0.05 * zoom)
        context.line_to(xo + 0.29 * zoom, yo - 0.21 * zoom)
        context.line_to(xo - 0.29 * zoom, yo - 0.21 * zoom)
        context.line_to(xo - 0.29 * zoom, yo + 0.05 * zoom)
        context.fill()
        context.move_to(xo - 0.13 * zoom, yo + 0.29 * zoom)
        context.line_to(xo + 0.13 * zoom, yo + 0.29 * zoom)
        context.line_to(xo + 0.13 * zoom, yo - 0.29 * zoom)
        context.line_to(xo - 0.13 * zoom, yo - 0.29 * zoom)
        context.line_to(xo - 0.13 * zoom, yo + 0.29 * zoom)
        context.fill()
        context.move_to(xo - 0.19 * zoom, yo + 0.32 * zoom)
        context.line_to(xo + 0.19 * zoom, yo + 0.32 * zoom)
        context.line_to(xo + 0.19 * zoom, yo + 0.16 * zoom)
        context.line_to(xo - 0.19 * zoom, yo + 0.16 * zoom)
        context.line_to(xo - 0.19 * zoom, yo + 0.32 * zoom)
        context.fill()
         
        context.set_source_rgba(*color)
        context.move_to(xo - 0.26 * zoom, yo + 0.02 * zoom)
        context.line_to(xo + 0.26 * zoom, yo + 0.02 * zoom)
        context.line_to(xo + 0.26 * zoom, yo - 0.18 * zoom)
        context.line_to(xo - 0.26 * zoom, yo - 0.18 * zoom)
        context.line_to(xo - 0.26 * zoom, yo + 0.02 * zoom)
        context.fill()
        context.move_to(xo - 0.1 * zoom, yo + 0.26 * zoom)
        context.line_to(xo + 0.1 * zoom, yo + 0.26 * zoom)
        context.line_to(xo + 0.1 * zoom, yo - 0.26 * zoom)
        context.line_to(xo - 0.1 * zoom, yo - 0.26 * zoom)
        context.line_to(xo - 0.1 * zoom, yo + 0.26 * zoom)
        context.fill()
        context.move_to(xo - 0.16 * zoom, yo + 0.29 * zoom)
        context.line_to(xo + 0.16 * zoom, yo + 0.29 * zoom)
        context.line_to(xo + 0.16 * zoom, yo + 0.19 * zoom)
        context.line_to(xo - 0.16 * zoom, yo + 0.19 * zoom)
        context.line_to(xo - 0.16 * zoom, yo + 0.29 * zoom)
        context.fill()
    
    def draw_infra_unit(self, context, vex, index, own, **item):
        r = self.saver.settings.get("hex-radius", 1.0)
        zoom = self.saver.settings["window-zoom"]
        color = self.saver.controls[own]["base-color"]
        loc = AbstractPainter.vex_to_loc(vex, r)                
        xo, yo = self.translate_xy(*loc)
        xo, yo = self.__to_slot(xo, yo, zoom*r, index)

        context.set_source_rgba(1, 1, 1)
        context.move_to(xo - 0.42 * zoom, yo + 0.27 * zoom)
        context.line_to(xo + 0.42 * zoom, yo + 0.27 * zoom)
        context.line_to(xo, yo - 0.42 * zoom)
        context.line_to(xo - 0.42 * zoom, yo + 0.27 * zoom)
        context.fill()

        context.set_source_rgba(0, 0, 0)
        context.move_to(xo - 0.36 * zoom, yo + 0.235 * zoom)
        context.line_to(xo + 0.36 * zoom, yo + 0.235 * zoom)
        context.line_to(xo, yo - 0.36 * zoom)
        context.line_to(xo - 0.36 * zoom, yo + 0.235 * zoom)
        context.fill()

        context.set_source_rgba(*color)
        context.move_to(xo - 0.3 * zoom, yo + 0.2 * zoom)
        context.line_to(xo + 0.3 * zoom, yo + 0.2 * zoom)
        context.line_to(xo, yo - 0.3 * zoom)
        context.line_to(xo - 0.3 * zoom, yo + 0.2 * zoom)
        context.fill()

    def draw_infra_tech(self, context, vex, index, own, **item):
        r = self.saver.settings.get("hex-radius", 1.0)
        zoom = self.saver.settings["window-zoom"]
        color = self.saver.controls[own]["base-color"]
        loc = AbstractPainter.vex_to_loc(vex, r)                
        xo, yo = self.translate_xy(*loc)
        xo, yo = self.__to_slot(xo, yo, zoom*r, index)

        context.set_source_rgba(1, 1, 1)
        context.arc(xo, yo, 0.38*zoom, 0, TWO_PI)
        context.fill()
        context.set_source_rgba(0, 0, 0)
        context.arc(xo, yo, 0.34*zoom, 0, TWO_PI)
        context.fill()
        context.set_source_rgba(*color)
        context.arc(xo, yo, 0.3*zoom, 0, TWO_PI)
        context.fill()