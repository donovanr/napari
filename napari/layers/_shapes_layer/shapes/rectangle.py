import numpy as np
from .shape import Shape
from ..shape_util import find_corners, rectangle_to_box


class Rectangle(Shape):
    """Class for a single rectangle

    Parameters
    ----------
    data : np.ndarray
        Nx2 array of vertices specifying the shape.
    edge_width : float
        thickness of lines and edges.
    edge_color : str | tuple
        If string can be any color name recognized by vispy or hex value if
        starting with `#`. If array-like must be 1-dimensional array with 3 or
        4 elements.
    face_color : str | tuple
        If string can be any color name recognized by vispy or hex value if
        starting with `#`. If array-like must be 1-dimensional array with 3 or
        4 elements.
    opacity : float
        Opacity of the shape, must be between 0 and 1.
    z_index : int
        Specifier of z order priority. Shapes with higher z order are displayed
        ontop of others.
    """
    def __init__(self, data, *, edge_width=1, edge_color='black',
                 face_color='white', opacity=1, z_index=0):

        super().__init__(edge_width=edge_width, edge_color=edge_color,
                         face_color=face_color, opacity=opacity,
                         z_index=z_index)

        self._closed = True
        self.data = np.array(data)
        self.name = 'rectangle'

    @property
    def data(self):
        """np.ndarray: Nx2 array of vertices.
        """
        return self._data

    @data.setter
    def data(self, data):
        if len(data) == 2:
            data = find_corners(data)
        if len(data) != 4:
            raise ValueError("""Data shape does not match a rectangle.
                             Rectangle expects four corner vertices""")
        else:
            # Add four boundary lines and then two triangles for each
            self._set_meshes(data, face=False)
            self._face_vertices = data
            self._face_triangles = np.array([[0, 1, 2], [0, 2, 3]])
            self._box = rectangle_to_box(data)

        self._data = data
