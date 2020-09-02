import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "2.0")
from gi.repository import Gtk, GooCanvas, GdkPixbuf

class Marker():
    def __init__(self, layer, x, y, radius = 10, color = "White", callback = None, id=None):
        self.x, self.y = x, y
        self.radius = radius
        self.color = color
        self.position = None
        self.callback = callback
        self.id = id

        self.marker = GooCanvas.CanvasEllipse(
                    parent = layer,
                    center_x = x, center_y = y,
                    radius_x = radius, radius_y = radius,
                    stroke_color = color,
                    fill_color_rgba = 0xffffff05,
                    line_width = 2)

        self.marker.connect("button-press-event", self.button_pressed)
        self.marker.connect("button-release-event", self.button_released) #el profe tiene layer
        self.marker.connect("motion-notify-event", self.button_moved)


    def button_pressed(self, src, tgt, event):
        self.position = event.x, event.y
        return True # si ponemos true en un evento no va a escuchar a otros


    def button_released(self, src, tgt, event):
        self.position = None

    def moveto(self, x, y):
        self.marker.set_property('center-x', x)
        self.marker.set_property('center-y', y)

    def get_position(self):
        return self.marker.get_property("center-x"), self.marker.get_property("center-y")

    def button_moved(self, src, tgt, event): #si queremos modificar el rectangulo anteior deberiamos de hacer un callback
        if self.position is None:
            return

        dx = event.x - self.position[0]
        dy = event.y - self.position[1]

        new_x = self.marker.get_property("center-x") + dx
        new_y = self.marker.get_property("center-y") + dy

        self.marker.set_property("center-x", new_x)
        self.marker.set_property("center-y", new_y)

        self.position = new_x, new_y

        if self.callback is not None:
            if self.id is not None:
                self.callback(new_x, new_y, self.id)
            else:
                self.callback(new_x, new_y)