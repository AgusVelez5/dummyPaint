import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "2.0")
from gi.repository import Gtk, GooCanvas, GdkPixbuf
from marker import Marker
from figure import Figure


class Rectangle(Figure):
    def __init__(self, tbox, x, y):
        super(Rectangle, self).__init__(tbox)
        self.tbox = tbox
        self.origin = x, y
        self.marker1 = Marker(self.tbox.layer, x, y, 2, "Red", self.moveto)

        stroke_color = self.to_rgba(self.tbox.stroke_colbtn.get_rgba())

        fill_color = self.to_rgba(self.tbox.fill_colbtn.get_rgba())

        line_width = self.tbox.spbtn.get_value()

        self.line = GooCanvas.CanvasRect(parent = tbox.layer, 
            x = x, 
            y = y, 
            width = 0, 
            height = 0,
            fill_color_rgba = fill_color,
            stroke_color_rgba= stroke_color,
            line_width=line_width)
        self.id_release = tbox.layer.connect("button-release-event", self.button_released) #evento que apreta boton
        self.id_moved = tbox.layer.connect("motion-notify-event", self.button_moved)

    def button_released(self, src, tgt, event):
        width = event.x - self.origin[0]
        height = event.y - self.origin[1]
        self.line.set_property('width', width)
        self.line.set_property('height', height)
        self.tbox.layer.disconnect(self.id_release)
        self.tbox.layer.disconnect(self.id_moved)
        # ~ self.marker_top_left = Marker(tbox.layer, x, y, color='Red')
        # ~ self.marker_bottom_right = Marker(tbox.layer, x, y)

        self.marker2 = Marker(self.tbox.layer, event.x, event.y, 2, "Red", callback=self.resize)

    def to_rgba(self, stroke_color):
        return  ((int(stroke_color.red * 255) << 24) +
                (int(stroke_color.green * 255) << 16) +
                (int(stroke_color.blue * 255) << 8) +
                int(stroke_color.alpha * 255))


    def button_moved(self, src, tgt, event):
        width = event.x - self.origin[0]
        height = event.y - self.origin[1]
        self.line.set_property('width', width)
        self.line.set_property('height', height)
        #self.tbox.layer.disconnect(self.id_moved)

    def moveto(self, x, y):
        self.line.set_property('x', x)
        self.line.set_property('y', y)
        w = self.line.get_property('width')
        h = self.line.get_property('height')
        self.marker2.moveto(x+w, y+h)


    
    def resize(self, xnew, ynew):
        x = self.line.get_property('x')
        y = self.line.get_property('y')
        self.line.set_property('width', xnew - x)
        self.line.set_property('height', ynew - y)