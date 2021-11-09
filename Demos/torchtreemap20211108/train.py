
import time
import os
import argparse
from typing import List
import pandas as pd
import numpy as np
from sacred import Experiment
from sacred.observers import FileStorageObserver

from environment import MultiAgentEnv
from maadqn import MAA2CAgent
import parameters as param

def make_env(scenario_name, args) -> MultiAgentEnv:
    import scenarios as scenarios
    # load scenario from script
    scenario = scenarios.load(scenario_name + '.py').Scenario(args)
    # create world
    world = scenario.make_world()
    env = MultiAgentEnv(world, scenario.reset_world, scenario.reward, scenario.observation, scenario.done)
    return env

def get_agents(env,args):
    agents = []
    for agent in env.agents:
        agent = MAA2CAgent(env, env.observation_space,env.action_space,agent.ag_id,agent.ag_name,args)
        agents.append(agent)
    return agents

def train(args):
    env = make_env('simple_scenario', args)
    agents = get_agents(env, args)
    obs_n = env.reset()

    for i in range(param.MAXEPOISE):
        print('Starting '+str(i+1)+' iterations...')
        while True:
            action_n = np.array([agent.toaction(obs.flatten()) for agent, obs in zip(agents, obs_n)])
            # print(f"ation_n: {action_n}")
            
            # if args.save == True:
            #     filepath = args.fold_name
            #     info = pd.DataFrame([[action_n[0],action_n[1],action_n[2],action_n[3],action_n[4]]], columns=['agent_0','agent_1','agent_2','agent_3','agent_4'])
            #     info.to_csv(filepath+'actions.csv', mode='a', header=False, index=None)

            new_obs_n, rew_n, done_n = env.step(action_n)

            # print(f"done: {done_n}")
            if done_n[0]:
                obs_n = env.reset()
                break

            for agent in agents:
                agent.add_transition(obs_n[agent.ag_id].flatten(),action_n[agent.ag_id],rew_n[agent.ag_id],new_obs_n[agent.ag_id].flatten())
            
            obs_n = new_obs_n

            for agent in agents:
                agent.update(agents)

def create_actions_file(args):
    import csv
    field_order = []
    for i in range(len(param.SUB_RECT_SIZE_LIST)):
        field_order.append("agent_"+str(i))
    
    if len(field_order) != 0:
        with open(args.fold_name+"actions.csv", 'w', encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, field_order)
            writer.writeheader()

def create_infos_file(args):
    import csv
    field_order = ['x','y','h','w','reward','aspect-ratio','overlap','outrange','area_diff']
    for i in range(len(param.SUB_RECT_SIZE_LIST)):
        with open(args.fold_name+"agent_"+str(i)+"_info.csv", 'w', encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, field_order)
            writer.writeheader()

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='RL TreeMap')
    parser.add_argument('--seed', default=12345, type=int)
    parser.add_argument('--create_file', default=True, type=bool)
    # area_diff overlap outrange 
    parser.add_argument('--fold_name', default='./data/data-normal/test-2-without-seed/', type=str)


    parser.add_argument('--save', default=True, type=bool)

    parser.add_argument('--done', default=True, type=bool)

    args = parser.parse_args()

    if args.create_file:
        create_actions_file(args)
        create_infos_file(args)
    
    np.random.seed(args.seed)
    train(args)

    print("...")
