
import parameters as params
from rectangle import Rect
import utils
import numpy as np
from core import World, Agent
from scenario import BaseScenario
import pandas as pd

class Scenario(BaseScenario):
    def __init__(self, args):
        super(Scenario, self).__init__()
        self.args = args

    def make_world(self):
        world = World()
        num_agents = len(params.SUB_RECT_SIZE_LIST)
        world.agents = [Agent(world, i,'agent_'+str(i)) for i in range(num_agents)]
        self.reset_world(world)
        return world
    
    def reset_world(self, world):
        world.t = 0
        for agent in world.policy_agents:
            agent.resetAgent(world)

    def reward(self, agent, world):
        aspect_ratio_ = self.aspect_ratio(agent)
        over_lap_ = self.over_lap(agent, world)
        out_range_ = self.out_range(agent, world)
        area_diff_ = self.area_diff(agent)

        r = area_diff_ + 10 * over_lap_ + 100 * out_range_
        s = agent.state.rect.getState()

        #==save==
        if self.args.save:
            filepath = self.args.fold_name
            info = pd.DataFrame([[str(s[0]),str(s[1]),str(s[2]),str(s[3]),str(r),str(aspect_ratio_),str(over_lap_),str(out_range_),str(area_diff_)]], columns=['x','y','h','w','reward','aspect-ratio','overlap','outrange','area_diff'])
            info.to_csv(filepath+'agent_'+str(agent.ag_id)+'_info.csv', mode='a', header=False, index=None)
        #========
        return r

    def aspect_ratio(self, agent):
        square_h = round(agent.state.rect.getChangeArea()**(1/2))
        square_w = square_h
        tmp_rect = Rect(agent.state.rect.getSize(),agent.state.rect.getChangeArea(),square_h, square_w, agent.state.rect.getCenter()[0], agent.state.rect.getCenter()[1])
        aspect_ratio = 0 - abs(2 * agent.state.rect.getArea() - 2 * utils.overlapArea(tmp_rect, agent.state.rect))
        return aspect_ratio

    def over_lap(self, agent, world):
        cost2 = 0
        for agent_i in world.policy_agents:
            if(agent.ag_id != agent_i.ag_id):
                cost2 += utils.overlapArea(agent.state.rect, agent_i.state.rect)/(agent.state.rect.getChangeArea() + agent_i.state.rect.getChangeArea() - 2 * utils.overlapArea(agent.state.rect, agent_i.state.rect))
        # width变化到0 或者 height变化到0怎么办？
        if agent.state.rect.getWidth() <=0  or agent.state.rect.getHeight()<=0:
            overlap = -100
        else:
            overlap = (0 - cost2)/len(world.policy_agents)
        return overlap

    def out_range(self,agent, world):
        cost3 = 0
        if not(agent.state.rect.getChangeArea() == utils.overlapArea(agent.state.rect, world.root)):
            cost3 = agent.state.rect.getChangeArea() - utils.overlapArea(agent.state.rect, world.root)
        # width变化到0 或者 height变化到0怎么办？
        if agent.state.rect.getWidth() <=0  or agent.state.rect.getHeight()<=0:
            outrange = -100
        else:
            outrange = (0 - cost3) / (agent.state.rect.getChangeArea())
        return outrange

    def area_diff(self, agent):
        orig_area = agent.state.rect.getArea()
        now_area = agent.state.rect.getChangeArea()
        areadiff = (0 - abs(orig_area - now_area))/orig_area
        return areadiff

    def observation(self, agent, world):
        '''
        单个矩形(智能体)的观测值：
            当前环境状态 = 自身矩形状态 + 其他矩形状态
            叠加状态(overlap) = 与自身产生overlap的各个矩形的状态
            最差为全部叠加,叠加数目为子矩形列表长度减一,因此我们规定叠加状态长度固定为最差叠加长度,
            未达到长度的叠加状态用零数组代替 
        '''
        re = []
        re.append(agent.state.rect.getState())
        # 添加根矩形的状态
        re.append(world.root.getState())
        for agent_i in world.policy_agents:
            if agent.ag_id != agent_i.ag_id:
                re.append(list(agent_i.state.rect.getState()))
        
        re = np.array(re)
        return re

    def done(self, world):

        if self.args.done:
            for agent in world.policy_agents:
                if (utils.overlapArea(agent.state.rect, world.root)<1):
                    return True

            # for agent in world.policy_agents:
            #     if (agent.state.rect.getChangeArea() != utils.overlapArea(agent.state.rect, world.root)):
            #         return True

        elif world.t > 1e5:
            return True
        else:
            return False

    def overLaps(self, agent, world):
        '''
        计算与当前矩形发生重叠的智能体 -> list
        '''
        ans = []
        for agent_i in world.policy_agents:
            if (agent.ag_id != agent_i.ag_id) and utils.isIntersect(agent.state.rect, agent_i.state.rect):
                ans.append(agent_i)
        return ans