
from rectangle import Rect
import numpy as np
from gym.spaces import Box, Discrete

def space_n_to_shape_n(space_n):
    """
    Takes a list of gym spaces and returns a list of their shapes
    """
    return np.array([space_to_shape(space) for space in space_n])

def space_to_shape(space):
    """
    Takes a gym.space and returns its shape
    """
    if isinstance(space, Box):
        return space.shape
    elif isinstance(space, Discrete):
        return [space.n]
    else:
        raise RuntimeError("Unknown space type. Can't return shape.")

def isIntersect(r1:Rect, r2:Rect):
    '''
    判断两个矩形是否相交
    '''    
    w = abs(r1._x - r2._x)
    h = abs(r1._y - r2._y)

    if(w < (r1._width_half + r2._width_half) and h < (r1._height_half + r2._height_half)):
        return True
    else:
        return False

def overlapArea(r1:Rect, r2:Rect):
    '''
    计算两个矩形重叠的面积
    '''
    r1_x1 = r1._x - r1._width_half
    r1_x2 = r1._x + r1._width_half
    r1_y1 = r1._y - r1._height_half
    r1_y2 = r1._y + r1._height_half

    r2_x1 = r2._x - r2._width_half
    r2_x2 = r2._x + r2._width_half
    r2_y1 = r2._y - r2._height_half
    r2_y2 = r2._y + r2._height_half

    overlapWidth = min(r1_x2, r2_x2) - max(r1_x1, r2_x1)
    overlapHeight = min(r1_y2, r2_y2) - max(r1_y1, r2_y1)
    overlapArea = max(overlapWidth, 0) * max(overlapHeight, 0)

    # print()
    # print("==========================")
    # print(r1_x1, r1_y1, r1_x2, r1_y2)
    # print(r2_x1, r2_y1, r2_x2, r2_y2)
    # print(overlapArea)
    # print("==========================")
    # print()

    return overlapArea

# class LinearSchedule(object):
#     """
#     Linear interpolation between initial_p and final_p over
#     schedule_timesteps. After this many timesteps pass final_p is
#     returned.
#     FROM STABLE BASELINES
#     :param schedule_timesteps: (int) Number of timesteps for which to linearly anneal initial_p to final_p
#     :param initial_p: (float) initial output value
#     :param final_p: (float) final output value
#     """

#     def __init__(self, schedule_timesteps, final_p, initial_p=1.0):
#         self.schedule_timesteps = schedule_timesteps
#         self.current_step = 0
#         self.final_p = final_p
#         self.initial_p = initial_p

#     def value(self, step):
#         fraction = min(float(step) / self.schedule_timesteps, 1.0)
#         return self.initial_p + fraction * (self.final_p - self.initial_p)

# import tensorflow as tf

# def softmax_to_argmax(action_n, agents):
#     """
#     If given a list of action probabilities performs argmax on each of them and outputs
#     a one-hot-encoded representation.
#     Example:
#         [0.1, 0.8, 0.1, 0.0] -> [0.0, 1.0, 0.0, 0.0]
#     :param action_n: list of actions per agent
#     :param agents: list of agents
#     :return List of one-hot-encoded argmax per agent
#     """
#     hard_action_n = []
#     for ag_idx, (action, agent) in enumerate(zip(action_n, agents)):
#         hard_action_n.append(tf.keras.utils.to_categorical(np.argmax(action), agent.act_shape_n[ag_idx,0]))

#     return hard_action_n