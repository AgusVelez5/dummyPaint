import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "2.0")
from gi.repository import Gtk, GooCanvas, GdkPixbuf
from marker import Marker
from figure import Figure

class Mountain(Figure):
    def __init__(self, tbox, x, y):
        super(Mountain, self).__init__(tbox)
        self.tbox = tbox

        self.data = '' 
        self.origin = x, y

        self.marker_move = Marker(self.tbox.layer, x, y, 2, "Green", self.moveto)

        stroke_color = self.to_rgba(self.tbox.stroke_colbtn.get_rgba())
        fill_color = self.to_rgba(self.tbox.fill_colbtn.get_rgba())
        line_width = self.tbox.spbtn.get_value()

        self.point_line = [
            [x,y],
            [x,y],
            [x,y]
        ]

        self.mountain = GooCanvas.CanvasPath(
            parent = tbox.layer,
            data = self.data,
            fill_color_rgba = fill_color,
            stroke_color_rgba = stroke_color,
            line_width = line_width
        )

        self.draw()

        self.id_release = tbox.layer.connect("button-release-event", self.button_released)
        self.id_moved = tbox.layer.connect("motion-notify-event", self.button_moved)

        

    def button_released(self, src, tgt, event):
        width = abs(event.x - self.origin[0]) 
        height = abs(event.y - self.origin[1])
        self.mountain.set_property('width', width)
        self.mountain.set_property('height', height)
        self.tbox.layer.disconnect(self.id_release)
        self.tbox.layer.disconnect(self.id_moved)

        x_med, y_med = self.origin[0] + (event.x - self.origin[0])/2 ,  self.origin[1] +(event.y - self.origin[1])/2
        self.marker_curve = Marker(self.tbox.layer, x_med, y_med, 2, "Blue", callback=self.mover_medio)
        
        self.marker_resize = Marker(self.tbox.layer, event.x, event.y, 2, "Green", callback=self.resize)

        self.point_line[2][0] = event.x
        self.point_line[2][1] = event.y
        
        self.draw()
        self.mountain.props.data = self.data
        

    def to_rgba(self, stroke_color):
        return  ((int(stroke_color.red * 255) << 24) +
                (int(stroke_color.green * 255) << 16) +
                (int(stroke_color.blue * 255) << 8) +
                int(stroke_color.alpha * 255))


    def button_moved(self, src, tgt, event):
        width = abs(event.x - self.origin[0])
        height = abs(event.y - self.origin[1])
        self.mountain.set_property('width', width)
        self.mountain.set_property('height', height)
        self.tbox.layer.disconnect(self.id_moved)

        self.draw()
        self.mountain.props.data = self.data

    def moveto(self, x, y): 
        
        x_diff = x - self.point_line[0][0]
        y_diff = y - self.point_line[0][1]
        
        self.mountain.set_property('x', x)
        self.mountain.set_property('y', y)
        self.point_line[0][0] = x
        self.point_line[0][1] = y
        self.origin = self.mountain.get_property('x'), self.mountain.get_property('y')

        x_prev_med, y_prev_med = self.point_line[1][0], self.point_line[1][1]
        x_med, y_med = x_prev_med + x_diff,  y_prev_med + y_diff
        self.point_line[1][0] = x_med
        self.point_line[1][1] = y_med
        self.marker_curve.moveto(x_med, y_med)

        x_prev_end, y_prev_end = self.point_line[2][0], self.point_line[2][1]
        x_end, y_end = x_prev_end + x_diff,  y_prev_end + y_diff
        self.point_line[2][0] = x_end
        self.point_line[2][1] = y_end
        self.marker_resize.moveto(x_end, y_end)

        self.draw()
        self.mountain.props.data = self.data


    
    def resize(self, x, y):
        x_diff = x - self.point_line[2][0]
        y_diff = y - self.point_line[2][1]
        
        x_prev_med, y_prev_med = self.point_line[1][0], self.point_line[1][1]
        x_med, y_med = x_prev_med + x_diff,  y_prev_med + y_diff
        self.point_line[1][0] = x_med
        self.point_line[1][1] = y_med
        self.marker_curve.moveto(x_med, y_med)

        self.point_line[2][0] = x
        self.point_line[2][1] = y
        self.marker_resize.moveto(x, y)

        self.draw()
        self.mountain.props.data = self.data
        

    def draw(self):
        self.data = 'M {:g} {:g} Q{:g} {:g} {:g} {:g}Z'.format(self.point_line[0][0], self.point_line[0][1], self.point_line[1][0], self.point_line[1][1], self.point_line[2][0], self.point_line[2][1])


    def mover_medio(self, x, y):
        self.point_line[1][0] = x
        self.point_line[1][1] = y
        self.marker_curve.moveto(x, y)

        self.draw()
        self.mountain.props.data = self.data
