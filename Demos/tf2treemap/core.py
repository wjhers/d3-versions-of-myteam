
import numpy as np
from rectangle import Rect
import parameters as params
import utils

# state of agents
class AgentState(object):
    def __init__(self,ag_id):
        self.rect = Rect()
        self.set_rect(ag_id)

    def set_rect(self,ag_id):
        sub_rect = params.sub_rect_attr(params.SUB_RECT_SIZE_LIST[ag_id])
        # print(sub_rect)
        self.rect.setAttr(ag_id,sub_rect[0],sub_rect[1],sub_rect[2],sub_rect[3],sub_rect[4],sub_rect[5])
    
    def resetAgentState(self,ag_id):
        self.set_rect(ag_id)

# action of agents
class AgentAction(object):
    def __init__(self):
        self.delta_list = np.zeros(3,dtype=np.float32)
        # delta_list = [delta_x1, delta_y1, delta_x2]

    def resetAgentAction(self):
        self.delta_list = np.zeros(3,dtype=np.float32)

    # can move return True
    # else return False
    def allowmove(self, rect, rootRect):
        x1 = rect.x1 + self.delta_list[0]
        y1 = rect.y1 + self.delta_list[1]
        x2 = rect.x2 + self.delta_list[2]
        width = x2 - x1
        y2 = y1 + float(rect.area / width)
        if x2 > x1 and y2 > y1 \
            and rootRect.x1<=x1 and x1 <= rootRect.x2 \
            and rootRect.y1<=y1 and y1 <= rootRect.y2 \
            and rootRect.x1<=x2 and x2 <= rootRect.x2 \
            and rootRect.y1<=y2 and y2 <= rootRect.y2:
            return True
        else:
            return False

    # fail to move, but want to get the overlapArea on the rootRect
    def failmove_overlap_area(self, rect, action, rootRect):
        x1 = rect.x1 + action[0]
        y1 = rect.y1 + action[1]
        x2 = rect.x2 + action[2]
        width = x2 - x1
        y2 = y1 + float(rect.area / width)

        new_rect = Rect()
        # -999 represent the new_rect
        new_rect.setAttr(-999,rect.size,rect.area,x1,y1,x2,y2)

        return utils.overlapArea(new_rect, rootRect)


# properties of agent entities
class Agent(object):
    def __init__(self, ag_id, ag_name=""):
        
        self.ag_id = int(ag_id)
        self.ag_name = ag_name
        # state
        self.state = AgentState(ag_id)
        # action
        self.action = AgentAction()
        # script behavior to execute
        self.action_callback = None
    
    def resetAgent(self,ag_id):
        self.state.resetAgentState(ag_id)
        self.action.resetAgentAction()

# multi-agent world
class World(object):
    def __init__(self):
        # list of agents
        self.agents = []
        # root Rect
        self.root = Rect()
        self.set_root()

        self.t = 0
        # communication channel dimensionality
        self.dim_c = 0
        # position dimensionality
        self.dim_p = 2
        # simulation timestep
        self.dt = 0.1

    def set_root(self):
        self.root.setAttr(params.ROOT_RECT_ID,params.ROOT_RECT_SIZE,params.ROOT_RECT_AREA,params.ROOT_RECT_X1,params.ROOT_RECT_Y1,params.ROOT_RECT_X2,params.ROOT_RECT_Y2)
    
    #return all agents
    @property
    def entities(self):
        return self.agents
    
    # return all agents controllable by external policies
    @property
    def policy_agents(self):
        return [agent for agent in self.agents if agent.action_callback is None]

    # return all agents controlled by world scripts
    @property
    def scripted_agents(self):
        return [agent for agent in self.agents if agent.action_callback is not None]

    # update state of the world
    def step(self, action_n, rootRect):
        # collect all agents loactions [[x1,y1,x2,y2],...,[x1,y1,x2,y2]]
        p_agent_loactions = [None] * len(self.entities)
        p_agent_loactions = self.apply_locations(p_agent_loactions)
        
        self.t = self.t + 1
        
        for agent in self.agents:
            self.update_agent_state(agent,action_n[agent.ag_id], rootRect)

    def apply_locations(self, p_agent_loactions):
        for i,agent in enumerate(self.agents):
            p_agent_loactions[i] = self.getAgentLocation(agent)

    def getAgentLocation(self, agent):
        return [agent.state.rect.listLocations]

    def update_agent_state(self, agent, action_n_i, rootRect):
        for j in range(len(action_n_i)):
            agent.action.delta_list[j] = action_n_i[j]
        t_or_f = agent.action.allowmove(agent.state.rect, rootRect)
        agent.state.rect.tomove(action_n_i[0], action_n_i[1], action_n_i[2], t_or_f)

print("core.py========")