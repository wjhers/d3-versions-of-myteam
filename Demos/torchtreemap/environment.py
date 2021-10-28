import gym
from gym import spaces
import numpy as np
import parameters as params

class MultiAgentEnv(gym.Env):
    metadata = {
        'render.modes' : ['human', 'rgb_array']
    }
    def __init__(self,world,reset_callback=None,reward_callback=None,observation_callback=None,done_callback=None):
        self.world = world
        self.agents = self.world.policy_agents
        self.n = len(self.world.policy_agents)
        # scenario callbacks
        self.reset_callback = reset_callback
        self.reward_callback = reward_callback
        self.observation_callback = observation_callback
        self.done_callback = done_callback
        self.time = self.world.t
        
        self.action_space = [] # [Discrete(8), Discrete(8), ...] -> list
        self.observation_space = [] #[Discrete(len(subrects)*(len(subrects)-1)), ...] -> list

        for agent in self.agents:
            action_dim = len(agent.action.actions_list)
            self.action_space.append(spaces.Discrete(action_dim))
            # 观测值 = 环境中各个矩形状态 + 重叠状态
            obs_dim = len(observation_callback(agent, self.world)) * 4
            self.observation_space.append(spaces.Discrete(obs_dim))

    def step(self, action_n):
        obs_n = []
        reward_n = []
        done_n = []

        self.world.step(action_n)
        
        for i,agent in enumerate(self.agents):
            obs_n.append(self._get_obs(agent))
            reward_n.append(self._get_reward(agent, action_n[i]))
            done_n.append(self._get_done())
        
        obs_n = np.asarray(obs_n)
        reward_n = np.asarray(reward_n)
        done_n = np.asarray(done_n)
        return obs_n, reward_n, done_n          

    def reset(self):
        self.reset_callback(self.world)
        self.time = self.world.t
        obs_n = []
        self.agents = self.world.policy_agents
        for agent in self.agents:
            obs_n.append(self._get_obs(agent))
        obs_n = np.asarray(obs_n)
        return obs_n

    # get observation for a particular agent
    def _get_obs(self, agent):
        if self.observation_callback is None:
            return np.zeros(0)
        return self.observation_callback(agent, self.world).astype(np.int32)

    # get reward for a particular agent
    def _get_reward(self,agent,action):
        if self.reward_callback is None:
            return 0.0
        return self.reward_callback(agent,self.world)

    # get dones for a particular agent
    def _get_done(self):
        if self.done_callback is None:
            return False
        return self.done_callback(self.world)