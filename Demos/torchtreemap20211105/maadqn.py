
import argparse
import numpy as np
import utils as util
from gym import Space
from gym.spaces import Box, Discrete
import parameters as params

import torch                               
import torch.nn as nn                         
import torch.nn.functional as F                
import numpy as np                              
import gym                                      


class MAA2CAgent(object):
    def __init__(self,obs_space_n,act_space_n,agent_index,agent_name):
    
        assert isinstance(obs_space_n[0], Space)
        assert isinstance(act_space_n[0], Space)
        
        self.obs_shape_n = util.space_n_to_shape_n(obs_space_n)
        self.act_shape_n = util.space_n_to_shape_n(act_space_n)
        
        self.dqn = DQN(self.obs_shape_n[agent_index][0],self.act_shape_n[agent_index][0], 8000)
        
        self.ag_id = agent_index
        self.ag_name = agent_name

    def add_transition(self,obs_n,action_n,rew_n,new_obs_n):
        self.dqn.store_transition(obs_n,action_n,rew_n,new_obs_n)

    def toaction(self, obs):
        return self.dqn.choose_action(obs)

    def update(self, agents):
        assert agents[self.ag_id] is self
        self.dqn.learn()

class Net(nn.Module):
    def __init__(self, N_STATES, N_ACTIONS):
        super(Net, self).__init__()                                         

        self.fc1 = nn.Linear(N_STATES, 50)                                      
        self.fc1.weight.data.normal_(0, 0.1)                                    
        self.out = nn.Linear(50, N_ACTIONS)                                     
        self.out.weight.data.normal_(0, 0.1)                                    

    def forward(self, x):                                                       
        x = F.relu(self.fc1(x))                                                
        actions_value = self.out(x)                                             
        return actions_value                                                  

class DQN(object):
    def __init__(self, N_STATES, N_ACTIONS, MEMORY_CAPACITY):
        
        self.N_STATES = N_STATES
        self.N_ACTIONS = N_ACTIONS
        self.MEMORY_CAPACITY = MEMORY_CAPACITY

        self.eval_net, self.target_net = Net(self.N_STATES, self.N_ACTIONS), Net(self.N_STATES, self.N_ACTIONS)
        self.learn_step_counter = 0
        self.memory_counter = 0
        self.memory = np.zeros((self.MEMORY_CAPACITY, self.N_STATES * 2 + 2))
        self.optimizer = torch.optim.SGD(self.eval_net.parameters(), lr=params.LR)
        self.loss_func = nn.MSELoss()

    def choose_action(self, x):                                                 
        x = torch.unsqueeze(torch.FloatTensor(x), 0)
        if np.random.uniform() < params.EPSILON:   
            actions_value = self.eval_net.forward(x)                            
            action = torch.max(actions_value, 1)[1].data.numpy()               
            action = action[0]                                                  
        else:                                                                 
            action = np.random.randint(0, self.N_ACTIONS)                          
        return action                                                        

    def store_transition(self, s, a, r, s_):                                    
        transition = np.hstack((s, [a, r], s_))                               
        index = self.memory_counter % self.MEMORY_CAPACITY                     
        self.memory[index, :] = transition                                   
        self.memory_counter += 1                                              

    def learn(self):                                                         
        if self.learn_step_counter % params.TARGET_REPLACE_ITER == 0:        
            self.target_net.load_state_dict(self.eval_net.state_dict())      
        self.learn_step_counter += 1                                      
        sample_index = np.random.choice(self.MEMORY_CAPACITY, params.BATCH_SIZE)    
        b_memory = self.memory[sample_index, :]                        
        b_s = torch.FloatTensor(b_memory[:, :self.N_STATES])
        b_a = torch.LongTensor(b_memory[:, self.N_STATES:self.N_STATES+1].astype(int))
        b_r = torch.FloatTensor(b_memory[:, self.N_STATES+1:self.N_STATES+2])
        b_s_ = torch.FloatTensor(b_memory[:, -self.N_STATES:])


        q_eval = self.eval_net(b_s).gather(1, b_a)
        q_next = self.target_net(b_s_).detach()
        q_target = b_r + params.GAMMA * q_next.max(1)[0].view(params.BATCH_SIZE, 1)
        loss = self.loss_func(q_eval, q_target)
        self.optimizer.zero_grad()                   
        loss.backward()                           
        self.optimizer.step()