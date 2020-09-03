import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "2.0")
from gi.repository import Gtk, GooCanvas, GdkPixbuf
from rectangle import Rectangle
from mountain import Mountain
from triangle import Triangle

class Toolbox(Gtk.Frame):
    def __init__(self, layer):
        super(Toolbox, self).__init__(label="Herramientas", margin = 6)
        
        self.layer = layer
        self.layer.connect("button-press-event", self.layer_click)
        self.figure = None

        vbox = Gtk.VBox(margin = 6)
        self.add(vbox)

        lbl = Gtk.Label(label = "Ancho trazo:", xalign = 0)
        vbox.pack_start(lbl, False, False, 0)
        self.spbtn = Gtk.SpinButton.new_with_range(0, 20, 0.1)
        vbox.pack_start(self.spbtn, False, False, 0)

        lbl = Gtk.Label(label = "Color trazo:", xalign = 0)
        vbox.pack_start(lbl, False, False, 0)
        self.stroke_colbtn = Gtk.ColorButton()
        vbox.pack_start(self.stroke_colbtn, False, False, 0)

        lbl = Gtk.Label(label = "Color relleno:", xalign = 0)
        vbox.pack_start(lbl, False, False, 0)
        self.fill_colbtn = Gtk.ColorButton()
        vbox.pack_start(self.fill_colbtn, False, False, 0)

        lbl = Gtk.Label(label = "Figuras:", xalign = 0)
        vbox.pack_start(lbl, False, False, 0)

        figuras = (
            ("rectangle.svg", "Rectangulo", Rectangle),
            ("mountain.svg", "Montania", Mountain),
            ("triangle.svg", "Triangulo", Triangle),
        )

        for file, tooltip, figure in figuras:
            try: 
                pxb = GdkPixbuf.Pixbuf.new_from_file_at_scale(file, -1, 32, True)
                img = Gtk.Image.new_from_pixbuf(pxb)
            except:
                img = Gtk.Image.new_from_file("invalid")
            btn = Gtk.Button(
                   image = img,
                   tooltip_text = tooltip,
                   relief = Gtk.ReliefStyle.NONE)
            btn.connect("clicked", self.figure_selected, figure)
            vbox.pack_start(btn, False, False, 0)

    def figure_selected(self, btn, which):
        self.figure = which

    def layer_click(self, src, target, event): 
        if self.figure is not None:
            self.figure(self, event.x, event.y)