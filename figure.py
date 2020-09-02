class Figure(object):
    def __init__(self, tbox):
        """ 
        Tarea comun: Buscar colores y ancho del trazo actualmente seleccionados.
        """
        self.tbox = tbox
        self.width = tbox.spbtn.get_value()
        self.fill_color = tbox.fill_colbtn.get_color()
        self.stroke_color = tbox.stroke_colbtn.get_color()