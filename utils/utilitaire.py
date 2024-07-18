from utils.brute_force import brute_force
from utils.heuristique import heuristique

from shapely.geometry import Polygon
from objet.forme import Forme
from objet.rectangle import Rectangle
from objet.triangle_isocele import TriangleIsocele
from objet.cercle import Cercle

from utils.twod_functions import *

class Utilitaire:

    @staticmethod
    def choose_fit(fit_string, formes, W, H):
        boundary = Utilitaire.create_boundery(W, H)
        shapes = Utilitaire.canvas_element_to_polygon(formes)
        match fit_string:
            case "Heuristique":
                return heuristique(boundary, shapes)
            case "Brute force":
                return brute_force(boundary, shapes)
            
    @staticmethod
    def create_boundery(W, H):
        x1 = (0, 0)
        x2 = (W, 0)
        y2 = (W, H)
        y1 = (0, H)
        points = [x1, x2, y2, y1]
        return Polygon(points)
    
    @staticmethod
    def canvas_element_to_polygon(formes):
        shapes = []
        for form in formes:
            shape = None
            if isinstance(form, Rectangle):
                shape = generate_rectangle(form.width, form.height)
            elif isinstance(form, Cercle):
                shape = generate_circle(form.rayon)
            elif isinstance(form, TriangleIsocele):
                shape = generate_triangle(form.base, form.hauteur)
            shapes.append(shape)
        return shapes
    
    @staticmethod
    def transform_polygon(index , shape: Polygon):
        bounds = shape.exterior.bounds
        coords = shape.exterior.coords
        form = Forme(index)
        form.x = bounds[0]
        form.y = bounds[1]
        scale_factor = 1
        for x, y in coords:
            form.coords.append(x * scale_factor)
            form.coords.append(y * scale_factor)
        return form
    
    @staticmethod
    def polygon_to_canvas_element(shapes):
        formes = []
        for i, shape in enumerate(shapes):
            formes.append(Utilitaire.transform_polygon(i, shape))
        return formes
        