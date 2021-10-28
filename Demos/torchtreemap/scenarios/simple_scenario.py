
import parameters as params
import utils
import numpy as np
from core import World, Agent
from scenario import BaseScenario

class Scenario(BaseScenario):

    def make_world(self):
        '''
        初始化 World agents
        '''
        world = World()
        num_agents = len(params.SUB_RECT_SIZE_LIST)
        world.agents = [Agent(world, i,'agent_'+str(i)) for i in range(num_agents)]
        self.reset_world(world)
        return world
    
    def reset_world(self, world):
        world.t = 0
        for agent in world.agents:
            agent.resetAgent(world)

    def reward(self, agent, world):
        r = params.ALPHA * self.aspect_ratio(agent) + params.BETA * (self.area_diff(agent) + self.over_lap(agent, world) + self.out_range(agent, world))
        # print(f"reward: {agent.ag_id} : {r}")
        return r

    def aspect_ratio(self, agent):        
        aspect_ratio = 0 - abs(1 - agent.state.rect.getAspectRatio())
        # print(f"aspect-ratio: {agent.ag_id} : {aspect_ratio}")
        return aspect_ratio

    def over_lap(self, agent, world):
        cost2 = 0.0
        # num = 0
        for agent_i in world.agents:
            if(agent.ag_id != agent_i.ag_id):
                # num += 1
                cost2 += utils.overlapArea(agent.state.rect, agent_i.state.rect)
        
        overlap = (0 - cost2)/(agent.state.rect.getArea())
        # print(f"overlap: {agent.ag_id} : {overlap}")
        return overlap
    
    def out_range(self,agent, world):
        cost3 = 0.0
        if not(agent.state.rect.getChangeArea() == utils.overlapArea(agent.state.rect, world.root)):
            cost3 = (agent.state.rect.getChangeArea() - utils.overlapArea(agent.state.rect, world.root))/(agent.state.rect.getChangeArea())
            # print()
            # print("=============================")
            # print(f"原始面积：{agent.state.rect.getArea()}")
            # print(f"变化后面积： {agent.state.rect.getChangeArea()}")
            # print(f"变化后面积与ROOT相交面积： {utils.overlapArea(agent.state.rect, world.root)}")
            # print(f"(变化后面积 - 变化后面积与ROOT相交面积)/变化后面积： {cost3}")
            # print("=============================")
            # print()
        outrange = 0 - cost3
        # print(f"outrange: {agent.ag_id} : {outrange}")
        return outrange

    def area_diff(self, agent):
        orig_area = agent.state.rect.getArea()
        now_area = agent.state.rect.getChangeArea()
        areadiff = 0 - (abs(orig_area - now_area)/orig_area)
        # print()
        # print("=============================")
        # print(f"原始面积：{agent.state.rect.getArea()}")
        # print(f"变化后面积： {agent.state.rect.getChangeArea()}")
        # print(f"abs(原始面积 - 变化后面积)/原始面积： {-areadiff}")
        # print("=============================")
        # print()
        # print(f"areadiff: {agent.ag_id} : {areadiff}")
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
        # num_agents = len(world.policy_agents)
        # overlaps = self.overLaps(agent, world)
        # fill_state = [0, 0, 0, 0]
        re.append(agent.state.rect.getState())
        for agent_i in world.policy_agents:
            if agent.ag_id != agent_i.ag_id:
                re.append(list(agent_i.state.rect.getState()))
        
        # for agent_i in overlaps:
        #     re.append(list(agent_i.state.rect.getState()))

        # for i in range(num_agents - len(overlaps) - 1): # 减一
        #     re.append(fill_state)

        re = np.array(re)
        return re

    def done(self, world):
        for agent in world.policy_agents:
            if (0 in agent.state.rect.getState()):
                return True
        if world.t > 1e5:
            return True
        else:
            return False

    def overLaps(self, agent, world):
        '''
        计算与当前矩形发生重叠的智能体 -> list
        '''
        ans = []
        for agent_i in world.agents:
            if (agent.ag_id != agent_i.ag_id) and utils.isIntersect(agent.state.rect, agent_i.state.rect):
                ans.append(agent_i)
        return ans