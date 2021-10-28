
import numpy as np
import sys

'''
CANVAS:
    Attributes of Canvas
'''
HEIGHT = 3
WIDTH = 4
AREA = HEIGHT * WIDTH

'''
ROOT_RECT: 
    Attributes of the Root Rect
'''
ROOT_RECT_SIZE = 15
ROOT_RECT_HEIGHT = HEIGHT * 100 # 100 is the divisions of HEIGHT
ROOT_RECT_WIDTH = WIDTH * 100
ROOT_RECT_AREA = ROOT_RECT_HEIGHT * ROOT_RECT_WIDTH
ROOT_RECT_X = ROOT_RECT_WIDTH / 2
ROOT_RECT_Y = ROOT_RECT_HEIGHT / 2

'''
SUB_RECT:
    A list of subrects
'''
SUB_RECT_SIZE_LIST = [5, 4, 3, 2, 1]


'''
dqn学习率
'''
LR = 0.01
BATCH_SIZE = 32                                 # 样本数量
LR = 0.01                                       # 学习率
EPSILON = 0.9                                   # greedy policy
GAMMA = 0.9                                     # reward discount
TARGET_REPLACE_ITER = 100                       # 目标网络更新频率


'''
Hyper parameters
'''
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
MAXEPOISE = 200