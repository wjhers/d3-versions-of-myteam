
import numpy as np
import sys


ROOT_RECT_ID = -1

ROOT_RECT_SIZE = 900
ROOT_RECT_AREA = 90000

ROOT_RECT_X1 = 0
ROOT_RECT_Y1 = 0
ROOT_RECT_X2 = 300
ROOT_RECT_Y2 = 300

ROOT_WIDTH = ROOT_RECT_X2 - ROOT_RECT_X1
ROOT_HEIGHT = ROOT_RECT_Y2 - ROOT_RECT_Y1

NUM_SUBRECT = 5

SUB_RECT_SIZE_LIST = [400,100,200,200,100]

# return a list of initing attr for subrect
def sub_rect_attr(rect_size):
    return [rect_size,
            float(rect_size*ROOT_RECT_AREA/ROOT_RECT_SIZE),
            0,
            0,
            min(ROOT_WIDTH, ROOT_HEIGHT),
            float((rect_size*ROOT_RECT_AREA/ROOT_RECT_SIZE)/(min(ROOT_WIDTH, ROOT_HEIGHT)))]


# hyperparameter
ALPHA = 1
BETA = 10

# Actor-Critic网络学习率
lr_actor = 5e-4
lr_critic = 2e-4

# 折扣因子γ
gamma = 0.99

beta_ = 0.0001

# int最大值
MAX_INT=sys.maxsize

# float 最大值
MAX_FLOAT =float('inf')

# 训练迭代次数
MAXEPOISE = 2