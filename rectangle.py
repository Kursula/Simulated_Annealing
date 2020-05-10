


class Rectangle: 
    
    """
    Data structures for the rectangle objects that will be stuffed inside 
    a box. 
    
    Few things to notice:    
    - Positions always refer to lower left corner. 
    
    - The current state (position and rotation) and new state proposal
    from the optimization algorithm are stored inside this object. 
    
    - The position and rotation properties will always use the proposal 
    values if those are available.
    
    - Rotation means 90 degree roration that is done by swapping the 
    size_x and size_y parameters. 
    """
    
    
    def __init__(self, 
                 name : str, 
                 size_x : float, 
                 size_y : float, 
                 color : list) -> None:
        
        self.name = name
        
        # Size of the rectangle
        self._size_x = size_x
        self._size_y = size_y
        
        # Position of lower left corner
        self._x = 0 
        self._y = 0 
        
        # Rotation flag 
        self.rotated = False
        
        # Algorithm position update variables
        self.new_pos_available = False
        self.new_x = 0 
        self.new_y = 0 
        self.new_rotated = False
        
        # Position history (for debugging etc)
        self.x_log = []
        self.y_log = []
        self.rotated_log = []
        
        # Visualization params
        self.color = color 

        
    @property
    def x(self) -> float: 
        if self.new_pos_available: 
            return self.new_x
        else:
            return self._x


    @x.setter
    def x(self, value : float) -> None: 
        self._x = value

        
    @property
    def y(self) -> float: 
        if self.new_pos_available: 
            return self.new_y
        else:
            return self._y

        
    @y.setter
    def y(self, value : float) -> None: 
        self._y = value

        
    @property
    def size_x(self) -> float: 
        if self.new_pos_available: 
            if self.new_rotated: 
                return self._size_y
            else:
                return self._size_x
        elif self.rotated: 
            return self._size_y
        else:
            return self._size_x

        
    @property
    def size_y(self) -> float: 
        if self.new_pos_available: 
            if self.new_rotated: 
                return self._size_x
            else:
                return self._size_y
        elif self.rotated: 
            return self._size_x
        else:
            return self._size_y