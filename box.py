from rectangle import Rectangle


class Box:
    """
    Simple container where rectandles are stuffed in. 
    """
    
    
    def __init__(self, 
                 size_x : float, 
                 size_y : float) -> None:

        self.size_x = size_x
        self.size_y = size_y
        self.x = 0 
        self.y = 0 
        self.rectangles = []
        
        
    def add_rectangle(self, 
                      rectangle : Rectangle) -> None: 
        
        self.rectangles.append(rectangle)