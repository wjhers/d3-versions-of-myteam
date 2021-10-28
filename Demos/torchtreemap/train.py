
import time
import os
from typing import List
import pandas as pd
import numpy as np
# import tensorflow as tf
from sacred import Experiment
from sacred.observers import FileStorageObserver

from environment import MultiAgentEnv
from maadqn import MAA2CAgent
import parameters as param

# if tf.config.experimental.list_physical_devices('GPU'):
#     tf.config.experimental.set_memory_growth(tf.config.experimental.list_physical_devices('GPU')[0],True)

def make_env(scenario_name) -> MultiAgentEnv:
    '''
    Create an environment
    :param scenario_name:
    :return:
    '''
    import scenarios as scenarios
    # load scenario from script
    scenario = scenarios.load(scenario_name + '.py').Scenario()
    # create world
    world = scenario.make_world()
    env = MultiAgentEnv(world, scenario.reset_world, scenario.reward, scenario.observation, scenario.done)
    return env

def get_agents(env):
    agents = []
    for agent in env.agents:
        agent = MAA2CAgent(env.observation_space,env.action_space,agent.ag_id,agent.ag_name)
        agents.append(agent)
    
    return agents

def train():
    env = make_env('simple_scenario')
    agents = get_agents(env)
    obs_n = env.reset()
    
    for i in range(param.MAXEPOISE):
        print('Starting '+str(i+1)+' iterations...')
        while True:
            action_n = np.array([agent.toaction(obs.flatten()) for agent, obs in zip(agents, obs_n)])
            print(f"ation_n: {action_n}")
            print()
            print(f"agent-info:")
            print(env.world.policy_agents[0].state.rect.printInfo())
            new_obs_n, rew_n, done_n = env.step(action_n)  
            
            for agent in agents:
                agent.add_transition(obs_n[agent.ag_id].flatten(),action_n[agent.ag_id],rew_n[agent.ag_id],new_obs_n[agent.ag_id].flatten())   
            
            print("env.world.t:",env.world.t)
            # print(env.world.policy_agents[0].action.actions_list)
            print("agent_0 reward:",rew_n[0])
            
            obs_n = new_obs_n
            
            if done_n[0]:
                obs_n = env.reset()
                break

            for agent in agents:
                agent.update(agents)


if __name__=="__main__":

    train()
    print("...")
