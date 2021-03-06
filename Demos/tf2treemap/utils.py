
from rectangle import Rect
import numpy as np
from gym.spaces import Box, Discrete
import tensorflow as tf

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

class LinearSchedule(object):
    """
    Linear interpolation between initial_p and final_p over
    schedule_timesteps. After this many timesteps pass final_p is
    returned.
    FROM STABLE BASELINES
    :param schedule_timesteps: (int) Number of timesteps for which to linearly anneal initial_p to final_p
    :param initial_p: (float) initial output value
    :param final_p: (float) final output value
    """

    def __init__(self, schedule_timesteps, final_p, initial_p=1.0):
        self.schedule_timesteps = schedule_timesteps
        self.current_step = 0
        self.final_p = final_p
        self.initial_p = initial_p

    def value(self, step):
        fraction = min(float(step) / self.schedule_timesteps, 1.0)
        return self.initial_p + fraction * (self.final_p - self.initial_p)

def clip_by_local_norm(gradients, norm):
    """
    Clips gradients by their own norm, NOT by the global norm
    as it should be done (according to TF documentation).
    This here is the way MADDPG does it.
    """
    for idx, grad in enumerate(gradients):
        gradients[idx] = tf.clip_by_norm(grad, norm)
    return gradients

class FakeRun(object):
    def __init__(self):
        """
        A fake run object as sacred uses, meant to be used as a replacement in unit test.
        """
        self.counter = 0

    def log_scalar(self, name, val, step):
        self.counter += 1

def softmax_to_argmax(action_n, agents):
    """
    If given a list of action probabilities performs argmax on each of them and outputs
    a one-hot-encoded representation.
    Example:
        [0.1, 0.8, 0.1, 0.0] -> [0.0, 1.0, 0.0, 0.0]
    :param action_n: list of actions per agent
    :param agents: list of agents
    :return List of one-hot-encoded argmax per agent
    """
    hard_action_n = []
    for ag_idx, (action, agent) in enumerate(zip(action_n, agents)):
        hard_action_n.append(tf.keras.utils.to_categorical(np.argmax(action), agent.act_shape_n[ag_idx,0]))

    return hard_action_n

# judge whether the two rectangles intersect.
def isIntersect(r1:Rect, r2:Rect):
    w1 = r1.x2 - r1.x1
    h1 = r1.y2 - r1.y1
    w2 = r2.x2 - r2.x1
    h2 = r2.y2 - r2.y1
    w = abs((r1.x1+r1.x2)/2-(r2.x1+r2.x2)/2)
    h = abs((r1.y1+r1.y2)/2-(r2.y1+r2.y2)/2)
    if(w < (w1 + w2)/2 and h < (h1 + h2)/2):
        return True
    else:
        return False

# compute the overlapArea of the two rectangles
def overlapArea(r1:Rect, r2:Rect):
    overlapWidth = min(r1.x2, r2.x2) - max(r1.x1, r2.x1)
    overlapHeight = min(r1.y2, r2.y2) - max(r1.y1, r2.y1)
    overlapArea = max(overlapWidth, 0) * max(overlapHeight, 0)
    return overlapArea




# r = Rect()
# r1 = Rect()
# r.setAttr(0,3,4,0,0,3,3)
# r1.setAttr(1,3,4,-1,1,1,3)

# print(overlapArea(r,r1))