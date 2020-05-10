import numpy as np
from rectangle import Rectangle
from box import Box



class RectangleMover:
    """
    This class contains all necessary methods for moving the rectangles in 
    the box when optimizing the packing solution.
    """
    
    def __init__(self, 
                 max_move_limit : float = 10.0, 
                 min_move_limit : float = 0.02) -> None: 
        
        self.max_move_limit = max_move_limit
        self.min_move_limit = min_move_limit
    
    
    def random_initialization(self, 
                              box : Box) -> None:
        
        for rect in box.rectangles: 
            rect.x = np.random.rand() * (box.size_x - rect.size_x)
            rect.y = np.random.rand() * (box.size_y - rect.size_y)

    
    def select_random_rectangle(self, 
                                box : Box) -> Rectangle: 
        
        rect = np.random.choice(box.rectangles)
        return rect

    
    def make_move(self, 
                  box : Box, 
                  progress_fraction : float) -> None:
        """
        Moves a random rectangle by random amount. Move is done in only 
        x or y direction while making sure that the new position is inside 
        the box. 
        
        Sometimes times this also rotates the rectangle. 
        """
       
        # Calculate limit for the move. The limit reduces towards the end 
        # of the optimization process. 
        move_limit = self.max_move_limit * (1 - progress_fraction) ** 2
        move_limit = max(move_limit, self.min_move_limit)
        
        if np.random.rand() < 0.5: 
            move_x = (np.random.rand() - 0.5) * move_limit 
            move_y = 0 
        else:
            move_x = 0
            move_y = (np.random.rand() - 0.5) * move_limit 

        rect = self.select_random_rectangle(box)
        rect.new_x = np.clip(rect.x + move_x, 0, box.size_x - rect.size_x)
        rect.new_y = np.clip(rect.y + move_y, 0, box.size_y - rect.size_y)
        rect.new_rotated = rect.rotated # Ignore possible earlier rotation proposal. 
        rect.new_pos_available = True
            
        if np.random.rand() < (1 - progress_fraction):
            # Rotate the rectangle
            rect.new_rotated = not rect.rotated 
            return
        
    
    def deploy_moves(self, 
                    box : Box) -> None:
        """
        Make all proposed position values effective. 
        """
        for rect in box.rectangles: 
            if rect.new_pos_available:
                rect.x = rect.new_x
                rect.y = rect.new_y
                rect.rotated = rect.new_rotated
                rect.new_pos_available = False

                
    def reject_moves(self, 
                     box : Box) -> None:
        """
        Reject all proposed position values. 
        """
        for rect in box.rectangles: 
            rect.new_pos_available = False
            rect.new_rotated = rect.rotated

            
    def save_history(self, 
                     box : Box) -> None:
        """
        Save history for debugging purposes
        """
        for rect in box.rectangles: 
            rect.x_log.append(rect.x)
            rect.y_log.append(rect.y)
            rect.rotated_log.append(rect.rotated)

    