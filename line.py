import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "2.0")
from gi.repository import Gtk, GooCanvas, GdkPixbuf
from marker import Marker
from figure import Figure

"""
Tenes que crear una instancia de una linea
* pode mover la linea con todos los valores
* poder re escalar la linea (y que persista su forma)
esto es una lineal : 7
bonus:
* si queres un 10 tenes que hacer una cuadratica.
* poder agregarle mas puntos
"""

class Line(Figure):
    def __init__(self, tbox, x, y):
        super(Line, self).__init__(tbox)
        self.tbox = tbox

        self.data = '' 
        self.origin = x, y

        self.marker_move = Marker(self.tbox.layer, x, y, 2, "Green", self.moveto)

        stroke_color = self.to_rgba(self.tbox.stroke_colbtn.get_rgba())
        fill_color = self.to_rgba(self.tbox.fill_colbtn.get_rgba())
        line_width = self.tbox.spbtn.get_value()

        # son los puntos de tu linea
        # cambiar estos atributos cambian tu figura
        # llamar luego draw para redibujarlo.
        self.point_line = [
            [x,y],
            [x,y],
            [x,y]
        ]

        self.draw()

        self.line = GooCanvas.CanvasPath(
            parent = tbox.layer, 
            x = x, 
            y = y, 
            data = self.data,
            width = 0, 
            height = 0,
            fill_color_rgba = fill_color,
            stroke_color_rgba = stroke_color,
            line_width = line_width
        )

        self.id_release = tbox.layer.connect("button-release-event", self.button_released)
        self.id_moved = tbox.layer.connect("motion-notify-event", self.button_moved)

        

    def button_released(self, src, tgt, event):
        # reescalar en la creacion
        width = event.x - self.origin[0]
        height = event.y - self.origin[1]
        self.line.set_property('width', width)
        self.line.set_property('height', height)
        self.tbox.layer.disconnect(self.id_release)
        self.tbox.layer.disconnect(self.id_moved)


        x_med, y_med = (event.x - self.origin[0])/2 , (event.y - self.origin[1])/2

        #marcador del medio.
        self.marker_curve = Marker(self.tbox.layer, x_med, y_med, 2, "Blue", callback=self.mover_medio)

        #marcador inferior derecha
        #cambiar 2 por 3
        self.marker_resize = Marker(self.tbox.layer, event.x, event.y, 2, "Green", callback=self.resize)
        self.point_line[3][0] = event.x
        self.point_line[3][1] = event.y
        
        self.draw()
        

    def to_rgba(self, stroke_color):
        return  ((int(stroke_color.red * 255) << 24) +
                (int(stroke_color.green * 255) << 16) +
                (int(stroke_color.blue * 255) << 8) +
                int(stroke_color.alpha * 255))


    def button_moved(self, src, tgt, event):
        # crear
        width = event.x - self.origin[0]
        height = event.y - self.origin[1]
        #self.line.set_property('width', width)
        #self.line.set_property('height', height)
        self.tbox.layer.disconnect(self.id_moved)

    def moveto(self, x, y): 
        self.line.set_property('x', x)
        self.line.set_property('y', y)
        #w = self.line.get_property('width')
        #h = self.line.get_property('height')
        self.marker2.moveto(x+w, y+h)

        self.origin = self.line.get_property('x'), self.line.get_property('y')


    
    def resize(self, xnew, ynew):
        x = self.line.get_property('x')
        y = self.line.get_property('y')
        self.line.set_property('width', xnew - x)
        self.line.set_property('height', ynew - y)

        #llamar siempre cuando lo editamos lo vamos a redibujar (self.draw())
        self.draw()

    def draw(self):
        self.data = 'M {:g} {:g} Q{:g} {:g} {:g} {:g} Z'.format(self.point_line[0][0], self.point_line[0][1], self.point_line[1][0], self.point_line[1][1], self.point_line[2][0], self.point_line[2][1] )


    def mover_medio(self, xnew, ynew):
        # x e y son los puntos que moves el marcador
        # esta funcion sirve para mover el punto del medio
        # al final volver a llamar la funcion draw()
        self.draw()

