import sys 
sys.path.append("..") 

import parameters as params
import utils
import numpy as np
from core import World, Agent
from scenario import BaseScenario

class Scenario(BaseScenario):

    def make_world(self):
        # create world
        world = World()
        # add agents
        num_agents = params.NUM_SUBRECT
        world.agents = [Agent(i,'agent_'+str(i)) for i in range(num_agents)]
        # init conditions
        self.reset_world(world)
        return world
    
    def reset_world(self, world):
        world.t = 0
        for agent in world.agents:
            agent.resetAgent(agent.ag_id)
    
    # for all agents in the world
    def reward(self, agent, world, action):
        r = 0
        r = r + params.ALPHA * self.aspect_ratio(agent) + params.BETA * (self.overlap(agent, world) + self.outrange(agent, world, action))
        return r

    # for each agent in the world
    # def aspect_ratio(self,agent, world, action):
        # cost1 = 0
        # if agent.action.allowmove(self, agent.state.rect, world.root):
        #     cost1 = agent.state.rect.aspect_ratio
        # else:
        #     cost1 = agent.action.failmove_aspect_ratio(agent.state.rect, action)
        
        # return 0 - cost1

    # return the aspect ratio of the agent
    def aspect_ratio(self,agent):
        return 0 - agent.state.rect.aspect_ratio

    # return the overlap area of the agent when the agent allowed to move, and do the normalization
    def overlap(self, agent, world):
        cost2 = 0.0
        num = 0
        for agent_i in world.agents:
            if(agent.ag_id != agent_i.ag_id):
                num += 1
                cost2 += utils.overlapArea(agent.state.rect, agent_i.state.rect)
        return (0 - cost2)/(num * world.root.area)
    
    # return the agent fail to move, but want to get the remaining area for overlap area on the rootRect, and do the normalization
    def outrange(self,agent, world, action):
        cost3 = 0.0
        if not(agent.action.allowmove(agent.state.rect, world.root)):
            cost3 = (agent.state.rect.area -  agent.action.failmove_overlap_area(agent.state.rect, action, world.root))/(world.root.area)
        return 0 - cost3


    def observation(self, agent, world):
        re = []
        # observations consit of itself and overlap rectangles' coordinate and aspect ratio 
        overlap_rects = self.overlaps(agent, world)
        re.append(agent.state.rect.listObservations)
        for agent_i in overlap_rects:
            re.append(agent_i.state.rect.listObservations)

        re = np.asarray(re)
        return re

    def done(self, world):
        if world.t > 1e5:
            return True
        else:
            return False
    
    def overlaps(self, agent, world):
        re = []
        for agent_i in world.agents:
            if utils.isIntersect(agent.state.rect, agent_i.state.rect):
                re.append(agent_i)
        return re

if __name__=="__main__":
    # s = Scenario()
    # w = s.make_world()    
    # print(len(s.observation(w)))
    # print("w.num_agents:",len(w.agents))

    # for i in range(len(w.agents)):
    #     print(w.agents[i].ag_name)
    #     print(w.agents[i].state.rect.listLocations)
    #     print(w.agents[i].state.rect.area)
    # w.step(np.asarray([[-100,2,3] for _ in range(5)]),w.root)


    # print("reward: ",s.reward(w.agents[0],w,[-100,2,3]))
    # print("aspect ratio: ",s.aspect_ratio(w.agents[0]))
    # print("overlap: ",s.overlap(w.agents[0],w))
    # print("outrange: ",s.outrange(w.agents[0],w,[-100,2,3]))


    # print("===============================================================")
    # print(s.observation(w.agents[0],w)[8:])
    # print(s.observation(w.agents[0],w)[:])
    # for i in range(w.numagents()):
        # print(w.agents[i].action.c)
    # for i in range(w.numagents()):
        # print("w.agents["+str(i)+"] reward:",s.reward(w.agents[i],w,np.asarray([0,1,2,3])))
    # for i in range(w.numagents()):
        # print(sum(w.agents[i].state.cache_state))
    print("...")








