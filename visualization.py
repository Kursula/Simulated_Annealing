import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.ndimage import gaussian_filter1d

from rectangle import Rectangle
from box import Box
from simulated_annealing import SimulatedAnnealing



def plot_history(sa : SimulatedAnnealing,
                 box : Box, 
                 fig_size : tuple = (10, 4), 
                 font_size : float = 12,
                 line_color : str = 'cornflowerblue',
                 ma_color : str = 'orangered') -> None: 
    
    plt.rcParams.update({'font.size': font_size})
    
    # Decision history
    plt.figure(figsize=fig_size)
    plt.scatter(
        np.arange(len(sa.decision_log)),
        sa.decision_log, 
        color=line_color,
        s=10,
        label='Decision'
    )
    plt.plot(
        gaussian_filter1d(np.array(sa.decision_log).astype(np.float32), sigma=100),
        label='Rolling average', 
        color=ma_color
    )
    plt.title('Algorithm decisions')
    plt.ylabel('Decision: 1=Accept, 0=Reject')
    plt.xlabel('Iteration')
    plt.legend()
    plt.show()
    
    # Bad move acceptance probability history
    plt.figure(figsize=fig_size)
    data = np.array(sa.bad_move_acc_prob_log)
    mask = data != None
    data = data[mask].astype(np.float32)
    plt.scatter(
        np.arange(len(sa.bad_move_acc_prob_log))[mask],
        data, 
        color=line_color, 
        s=10,
        label='Probability'
    )
    plt.plot(
        np.arange(len(sa.bad_move_acc_prob_log))[mask],
        gaussian_filter1d(data, sigma=100),
        label='Rolling average', 
        color=ma_color
    )
    plt.title('Bad move acceptance probability')
    plt.ylabel('Probability')
    plt.xlabel('Iteration')
    plt.legend()
    plt.show()


    # Cost history
    plt.figure(figsize=fig_size)
    plt.plot(sa.cost_log, label='Cost', color=line_color)
    plt.plot(
        gaussian_filter1d(np.array(sa.cost_log).astype(np.float32), sigma=100),
        label='Rolling average', 
        color=ma_color
    )
    plt.axhline(0, color='grey', ls=':')
    plt.title('Cost, final value={:0.3f}'.format(sa.cost_log[-1]))
    plt.ylabel('Total cost')
    plt.xlabel('Iteration')
    plt.legend()
    plt.show()

    # Algorithm temperature curve
    plt.figure(figsize=fig_size)
    plt.plot(sa.temperature_log, label='Temperature', color=line_color)
    plt.axhline(0, color='grey', ls=':')
    plt.title('Temperature')
    plt.ylabel('Temperature')
    plt.xlabel('Iteration')
    plt.show()

    # Average distance of nonzero moves
    all_dists = []
    for rect in box.rectangles: 
        coords = np.zeros((len(rect.x_log), 2))
        coords[:, 0] = np.array(rect.x_log)
        coords[:, 1] = np.array(rect.y_log)
        dists = np.linalg.norm(coords[1:] - coords[:-1], axis=1) 
        all_dists.append(dists)
    
    all_dists = np.stack(all_dists, axis=1)
    agg_dist = np.average(all_dists, weights=(all_dists != 0) * 1 + 1e-12, axis=1)
    plt.figure(figsize=fig_size)
    plt.scatter(
        np.arange(len(agg_dist)),
        agg_dist, 
        color=line_color,
        s=10, 
        label='Distance'
    )
    plt.plot(
        gaussian_filter1d(agg_dist, sigma=100),
        label='Rolling average', 
        color=ma_color
    )
    plt.title('Average accepted move distance')
    plt.ylabel('Distance')
    plt.xlabel('Iteration')
    plt.legend()
    plt.show()


def plot_rect_paths(box : Box,
                    fig_size : tuple = (6, 6), 
                    font_size : float = 12,
                    line_color : str = 'cornflowerblue') -> None: 
                        
    plt.rcParams.update({'font.size': font_size})

    for rect in box.rectangles: 
        fig = plt.figure(figsize=fig_size)
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')

        # Plot box borders as black line
        x1 = box.x
        x2 = box.x + box.size_x
        y1 = box.y
        y2 = box.y + box.size_y
        plt.plot(
            [x1, x2, x2, x1, x1],
            [y1, y1, y2, y2, y1],
            lw=2,
            color='black'
        )
        
        # Plot path line
        plt.plot(rect.x_log, rect.y_log, color=line_color)
        
        # Starting and ending points
        plt.scatter(
            rect.x_log[0], 
            rect.y_log[0], 
            color='red'
        )
        plt.annotate(
            xy=(rect.x_log[0], rect.y_log[0]),
            s='Start',
            ha='left'
        )

        plt.scatter(
            rect.x_log[-1], 
            rect.y_log[-1], 
            color='green'
        )
        plt.annotate(
            xy=(rect.x_log[-1], rect.y_log[-1]),
            s='End',
            ha='left'
        )
        plt.title(rect.name)
        plt.show()
        
        
def plot_rects(box : Box,
               fig_size : tuple = (10, 10), 
               font_size : float = 12) -> None: 
    
    plt.rcParams.update({'font.size': font_size})
    
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    # Plot box borders as black line
    x1 = box.x
    x2 = box.x + box.size_x
    y1 = box.y
    y2 = box.y + box.size_y
    plt.plot(
        [x1, x2, x2, x1, x1],
        [y1, y1, y2, y2, y1],
        lw=2,
        color='black'
    )
    
    # Plot the rectangles
    for rect in box.rectangles:
        rect_patch = patches.Rectangle(
            xy=(rect.x, rect.y),
            width=rect.size_x,
            height=rect.size_y,
            linewidth=2,
            edgecolor='dimgrey',
            facecolor=rect.color
        )
        ax.add_patch(rect_patch)
        # Plot some dummy markers just to get pyplot plotting auto scale 
        # behaving correctly. 
        plt.scatter(rect.x, rect.y, s=1)
        plt.scatter(rect.x + rect.size_x, rect.y + rect.size_y, s=1)

        text = rect.name
        plt.annotate(
            xy=(rect.x + rect.size_x / 2, rect.y + rect.size_y / 2),
            s=text,
            ha='center',
            va='center',
            rotation=90 if (rect.size_x < rect.size_y) else 0
        )
    plt.show()