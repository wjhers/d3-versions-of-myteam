
import numpy as np
from rectangle import Rect, getSubRectInfoFromRoot
import parameters as params
import utils

class AgentState(object):
    def __init__(self, size, area, height, width, x, y):
        '''
        矩形的状态即当前矩形的属性
        '''
        self.rect = Rect(size, area, height, width, x, y)

class AgentAction(object):
    def __init__(self):
        '''
        矩形的动作共9个[up, down, left, right, w+, w-, h+, h-, keep]
        [1, 0, 0, 0, 0, 0, 0, 0] or 0 up
        [0, 1, 0, 0, 0, 0, 0, 0] or 1 down
        [0, 0, 0, 1, 0, 0, 0, 0] or 2 left
        ...
        [0, 0, 0, 0, 0, 0, 0, 1] or 8 h-
        '''
        self.actions_list = np.zeros(9,dtype=np.int32)

class Agent(object):
    def __init__(self, world, ag_id, ag_name=""):
        '''
        ag_id 矩形的id，智能体的id
        ag_name 矩形的name，智能体的name
        state 矩形的状态，智能的状态
        action 矩形的动作，智能体的动作
        '''
        self.ag_id = int(ag_id)
        self.ag_name = ag_name
        self.state = None
        self.setState(world, ag_id)
        self.action = AgentAction()
        self.action_callback = None

    def setState(self, world, ag_id):
        sub_rect_info = getSubRectInfoFromRoot(world.root.getSize(), world.root.getArea(), params.SUB_RECT_SIZE_LIST[ag_id])
        root_center = world.root.getCenter()
        if sub_rect_info != "error":
            self.state = AgentState(
                sub_rect_info[0],
                sub_rect_info[1],
                sub_rect_info[2],
                sub_rect_info[3],
                root_center[0],
                root_center[1])

    def resetAgent(self, world):
        self.setState(world, self.ag_id)

class World(object):
    def __init__(self):
        '''
        智能体交互的世界
        agents 智能体集合
        root Root矩形
        t 交互世界的时间步
        '''
        self.agents = []
        self.root = None
        self.setRoot()
        self.t = 0

    def setRoot(self):
        '''
        函数setRoot：
        设置Root矩形属性
        '''
        self.root = Rect(
            params.ROOT_RECT_SIZE,
            params.ROOT_RECT_AREA,
            params.ROOT_RECT_HEIGHT,
            params.ROOT_RECT_WIDTH,
            params.ROOT_RECT_X,
            params.ROOT_RECT_Y)

    @property
    def entities(self):
        return self.agents
    
    @property
    def policy_agents(self):
        return [agent for agent in self.agents if agent.action_callback is None]

    # update state of the world
    def step(self, action_n):
        # collect agents' states
        c_agents_states = [None] * len(self.entities)
        c_agents_states = self.apply_states(c_agents_states)        
        self.t = self.t + 1
        for agent in self.agents:
            self.update_agent_state(agent, action_n[agent.ag_id])

    def apply_states(self, c_agents_states):
        for i,agent in enumerate(self.agents):
            c_agents_states[i] = self.getAgentState(agent)

    def getAgentState(self, agent):
        return list(agent.state.rect.getState())

    def update_agent_state(self, agent, action_n_i):
        agent.action.actions_list[:] = 0
        agent.action.actions_list[action_n_i] = 1
        agent.state.rect.toMove(action_n_i)