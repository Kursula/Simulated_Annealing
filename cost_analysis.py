import numpy as np
from rectangle import Rectangle
from box import Box



class CostAnalyzer: 
    """
    Functions for analyzing the cost of a box packing. Here cost refers 
    to the amount of problems found in the packing. The problem types are: 
    - rectangles are overlapping
    - rectangles are outside of the box
    """
    
    def __init__(self) -> None: 
        pass
    
    
    def analyze(self, 
                box : Box) -> None: 
        """
        Analyze total cost for all rectangles in the box. 
        """
        cost = 0 
        
        # Calculate amount of overlaps between rectangles. 
        for rect_a in box.rectangles: 
            for rect_b in box.rectangles: 
                
                if rect_a.name == rect_b.name: 
                    continue
                    
                overlap_area = self.overlap_area(rect_a, rect_b)
                if overlap_area > 0: 
                    cost += overlap_area

        # Calculate area of rectangles outside of the box
        for rect in box.rectangles: 
            outside_area = self.out_of_box_area(rect, box)
            if outside_area > 0: 
                cost += outside_area 
                
        return cost
                
        
    def out_of_box_area(self, 
                        rect : Rectangle, 
                        box : Box) -> float:
        
        """
        Out of box area is calculated as difference between rect area 
        and in-box area. 
        
        When rectangle is at least partially outside of the box, this will 
        multiply the value by square of the distance from box center point. 
        This ensured that the optimization can get the rectangle back inside
        the box. 
        """
        rect_area = rect.size_x * rect.size_y
        in_box_area = self.overlap_area(rect, box)
        outside_area_cost = rect_area - in_box_area
        
        if outside_area_cost > 0: 
            rect_cp = [rect.x + rect.size_x / 2, rect.y + rect.size_y / 2]
            box_cp = [box.x + box.size_x / 2, box.y + box.size_y / 2]
            dist = np.linalg.norm(np.array(rect_cp) - np.array(box_cp))
            outside_area_cost = outside_area_cost * (dist ** 2)
        
        return outside_area_cost
        
        
    def overlap_area(self, 
                     rect_a : Rectangle, 
                     rect_b : Rectangle) -> float: 
        
        """
        Calculate overlapping area of two rectangles.
        """
        # Test for no overlap cases
        if rect_a.x + rect_a.size_x  <= rect_b.x: 
            return 0
        if rect_b.x + rect_b.size_x <= rect_a.x: 
            return 0
        if rect_a.y + rect_a.size_y  <= rect_b.y: 
            return 0
        if rect_b.y + rect_b.size_y  <= rect_a.y: 
            return 0

        # At this point the rectangles are known to overlap 
        x_overlap = min(
            # a is smaller than b and a is totally inside b
            rect_a.size_x, 
            
            # b is smaller than a and b is totally inside a
            rect_b.size_x, 
            
            # a is at lower position than b 
            rect_a.x + rect_a.size_x - rect_b.x,
            
            # b is at lower position than a
            rect_b.x + rect_b.size_x - rect_a.x
        )
        y_overlap = min(
            # a is smaller than b and a is totally inside b
            rect_a.size_y, 
            
            # b is smaller than a and b is totally inside a
            rect_b.size_y, 
            
            # a is at lower position than b 
            rect_a.y + rect_a.size_y - rect_b.y,
            
            # b is at lower position than a
            rect_b.y + rect_b.size_y - rect_a.y
        )
        return x_overlap * y_overlap
        