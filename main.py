import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GooCanvas", "2.0")
from gi.repository import Gtk, GooCanvas, GdkPixbuf
from toolbox import Toolbox

class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", self.quit)
        self.set_default_size(1200,1200)

        canvas = GooCanvas.Canvas(
                    hexpand = True,
                    vexpand = True)
        cvroot = canvas.get_root_item()

        scroller = Gtk.ScrolledWindow()
        scroller.add(canvas)

        toolbox = Toolbox(cvroot)
        grid = Gtk.Grid()
        grid.attach(scroller, 0, 0, 1, 1)
        grid.attach(toolbox, 1, 0, 1, 1)

        self.add(grid)

        self.show_all()
    
    def quit(self, event):
        Gtk.main_quit()
    
    def run(self):
        Gtk.main()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))