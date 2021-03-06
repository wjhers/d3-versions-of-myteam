
import parameters as params
from rectangle import Rect
import utils
import numpy as np
from core import World, Agent
from scenario import BaseScenario
import pandas as pd

class Scenario(BaseScenario):

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
        # r = aspect_ratio_ + (area_diff_ + over_lap_ + out_range_)
        r = (area_diff_ + over_lap_ + out_range_)
        print(f"reward: {agent.ag_id} : {r}")

        # floadName = './results-with-aspect-ratio-without-done/'
        # floadName = './results-with-aspect-ratio-with-done/'
        # floadName = './results-without-aspect-ratio-without-done/'
        # floadName = './results-without-aspect-ratio-with-done/'

        floadName = './results-without-aspect-ratio-without-done-mean-overlap/'
        s = agent.state.rect.getState()
        info = pd.DataFrame([[str(s[0]),str(s[1]),str(s[2]),str(s[3]),str(r),str(aspect_ratio_),str(over_lap_),str(out_range_),str(area_diff_)]], columns=['x','y','h','w','reward','aspect-ratio','overlap','outrange','area_diff'])
        info.to_csv(floadName+'agent_'+str(agent.ag_id)+'_info.csv', mode='a', header=False, index=None)
        return r

        # mean-overlap-self-outrange-self-areadiff
        # r = (5 * over_lap_ + out_range_ + area_diff_)
        # r = over_lap_
        # print(f"reward: {agent.ag_id} : {r}")
        # floadName = './results-without-aspect-ratio-with-mean-overlap-self-outrange-self-areadiff/overlap-5-outrange-1-areadiff-1/'
        # s = agent.state.rect.getState()
        # info = pd.DataFrame([[str(s[0]),str(s[1]),str(s[2]),str(s[3]),str(r),str(aspect_ratio_),str(over_lap_),str(out_range_),str(area_diff_)]], columns=['x','y','h','w','reward','aspect-ratio','overlap','outrange','area_diff'])
        # info.to_csv(floadName+'agent_'+str(agent.ag_id)+'_info.csv', mode='a', header=False, index=None)
        # return r


    def aspect_ratio(self, agent):
        square_h = round(agent.state.rect.getChangeArea()**(1/2))
        square_w = square_h
        tmp_rect = Rect(agent.state.rect.getSize(),agent.state.rect.getChangeArea(),square_h, square_w, agent.state.rect.getCenter()[0], agent.state.rect.getCenter()[1])
        aspect_ratio = 0 - abs(2 * agent.state.rect.getArea() - 2 * utils.overlapArea(tmp_rect, agent.state.rect))
        return aspect_ratio

    def over_lap(self, agent, world):
        cost2 = 0
        num = 0
        for agent_i in world.policy_agents:
            if(agent.ag_id != agent_i.ag_id):
                num += 1
                cost2 += utils.overlapArea(agent.state.rect, agent_i.state.rect)
        overlap = (0 - cost2) / num
        return overlap

        # cost2 = 0
        # for agent_i in world.policy_agents:
        #     if(agent.ag_id != agent_i.ag_id):
        #         cost2 += utils.overlapArea(agent.state.rect, agent_i.state.rect)/(agent.state.rect.getChangeArea() + agent_i.state.rect.getChangeArea() - utils.overlapArea(agent.state.rect, agent_i.state.rect))
        # overlap = (0 - cost2)/len(world.policy_agents)
        # return overlap


    def out_range(self,agent, world):
        cost3 = 0
        if not(agent.state.rect.getChangeArea() == utils.overlapArea(agent.state.rect, world.root)):
            cost3 = agent.state.rect.getChangeArea() - utils.overlapArea(agent.state.rect, world.root)
        outrange = 0 - cost3
        return outrange

        # cost3 = 0
        # if not(agent.state.rect.getChangeArea() == utils.overlapArea(agent.state.rect, world.root)):
        #     cost3 = agent.state.rect.getChangeArea() - utils.overlapArea(agent.state.rect, world.root)
        # outrange = (0 - cost3) / (agent.state.rect.getChangeArea()+0.00000001)
        # return outrange

    def area_diff(self, agent):
        orig_area = agent.state.rect.getArea()
        now_area = agent.state.rect.getChangeArea()
        areadiff = 0 - abs(orig_area - now_area)
        return areadiff

        # orig_area = agent.state.rect.getArea()
        # now_area = agent.state.rect.getChangeArea()
        # areadiff = (0 - abs(orig_area - now_area))/orig_area
        # return areadiff

    def observation(self, agent, world):
        '''
        ????????????(?????????)???????????????
            ?????????????????? = ?????????????????? + ??????????????????
            ????????????(overlap) = ???????????????overlap????????????????????????
            ?????????????????????,??????????????????????????????????????????,???????????????????????????????????????????????????????????????,
            ???????????????????????????????????????????????? 
        '''
        re = []
        re.append(agent.state.rect.getState())
        for agent_i in world.policy_agents:
            if agent.ag_id != agent_i.ag_id:
                re.append(list(agent_i.state.rect.getState()))
        
        re = np.array(re)
        return re

    def done(self, world):
        for agent in world.policy_agents:
            if (0 in agent.state.rect.getState()):
                return True
        # for agent in world.policy_agents:
        #     if (agent.state.rect.getChangeArea() != utils.overlapArea(agent.state.rect, world.root)):
        #         return True
        if world.t > 1e5:
            return True
        else:
            return False

    def overLaps(self, agent, world):
        '''
        ????????????????????????????????????????????? -> list
        '''
        ans = []
        for agent_i in world.policy_agents:
            if (agent.ag_id != agent_i.ag_id) and utils.isIntersect(agent.state.rect, agent_i.state.rect):
                ans.append(agent_i)
        return ans