import numpy as np
from rectangle import Rectangle
from box import Box
from rectangle_mover import RectangleMover
from cost_analysis import CostAnalyzer



class SimulatedAnnealing: 
    
    def __init__(self, 
                 iterations : int, 
                 early_stop : bool, 
                 start_temperature : float, 
                 end_temperature : float, 
                 rect_mover : RectangleMover,
                 cost_analyzer : CostAnalyzer) -> None: 
        
        # Basic params 
        self.iterations = iterations
        self.early_stop = early_stop
        
        # Algorithm business logic and cost analysis
        self.rect_mover = rect_mover
        self.cost_analyzer = cost_analyzer
        
        # Algorithm temperature
        self.start_temperature = start_temperature
        self.end_temperature = end_temperature
        self.current_temperature = None 
        
        # Debug logging 
        self.cost_log = []
        self.bad_move_acc_prob_log = []
        self.decision_log = []
        self.temperature_log = []

        
    
    def acceptance_probability(self, 
                               cost : float, 
                               new_cost : float) -> float: 
        """
        Calculates probability for accepting a new move. 
        Moves to lower cost direction are always accepted. 
        Moves to higher cost direction are accepted depending on the temperature
        and the cost difference. 
        
        Note that the higher cost acceptance calculation differs from the typical formula 
        exp(-1 * (new_cost - cost) / temperature) that is used in academic literature. 
        The method used here uses the ratio of new cost to old cost in the exp function, 
        because it gives better fine-optimized results in cases where cost values are very high 
        in the beginning. This needs attention in the temperature tuning, i.e. almost linearly 
        reducing temperature often works best, with starting value approximately 1.
        """
        
        eps = 1e-12
        if new_cost <= cost:
            return 1
        else:
            probability = np.exp(-1 * ((new_cost + eps) / (cost + eps)) / (self.current_temperature + eps))
            return probability

    
    def update_temperature(self, 
                           iteration : int) -> None: 
        """
        Algorithm temperature. See notes at acceptance_probability method for more details. 
        """
        fraction = float(iteration / self.iterations)
        temp = ((1.0 - fraction) ** 1.20) * self.start_temperature        
        temp = max(temp, self.end_temperature)
        
        self.current_temperature = temp
        
    
    def optimize(self, 
                 box : Box) -> None: 
        """
        Optimization. 
        """
        # Analyze starting point 
        cost = self.cost_analyzer.analyze(box)
        
        # Run optimization
        for iteration in range(self.iterations):
            
            # Update temperature for each interation round
            self.update_temperature(iteration)
            
            # Make random move to rectangle position and analyze the cost impact
            progress_fraction = iteration / self.iterations
            self.rect_mover.make_move(box, progress_fraction=progress_fraction)
            new_cost = self.cost_analyzer.analyze(box)

            # Get probability for accepting the new move
            acc_prob = self.acceptance_probability(
                cost=cost, 
                new_cost=new_cost
            )
            
            # Make decision about the new move
            if np.random.rand() < acc_prob: 
                self.rect_mover.deploy_moves(box)
                cost = new_cost
                decision = 1
            else: 
                self.rect_mover.reject_moves(box)
                decision = 0

            # Log data for debugging purposes 
            self.rect_mover.save_history(box)
            self.cost_log.append(cost)
            if acc_prob == 1: 
                self.bad_move_acc_prob_log.append(None)
            else: 
                self.bad_move_acc_prob_log.append(acc_prob)            
            self.decision_log.append(decision)
            self.temperature_log.append(self.current_temperature)
            
            # Check if cost is zero and early stop is enabled
            if (cost == 0) and (self.early_stop == True):
                print('Early stop at iteration {}.'.format(iteration))
                print('Optimization achieved zero cost result.')
                return

        # All iterations done. Check the final result
        print('Final result: {:0.3f}'.format(cost))
        if cost > 0: 
            print('Full optimization not achieved.')