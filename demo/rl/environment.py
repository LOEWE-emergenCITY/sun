#!/usr/bin/python3

import time
import gym
import ray
import numpy as np
from ray.rllib.agents.ppo import ppo
from ray.tune import register_env


class CoreGazeboEnv(gym.Env):
    def __init__(self):
        self.curr_time = None
        self.t = 0

        self.observation_space = gym.spaces.Box(-1, 1, shape=(2,), dtype=float)
        self.action_space = gym.spaces.Box(-1, 1, shape=(2,), dtype=float)

        self.reset()

    def reset(self):
        # TODO reset the entire simulation
        physical_state = self.poll_gazebo_state()
        network_state = self.poll_network_state()
        return self.get_observation(physical_state, network_state)

    def send_actions(self, action):
        pass  # TODO send the flight controller the desired actions for the next time step, see MavSDK

    def poll_gazebo_state(self):
        print("capturing positions from gazebo...")

        result = subprocess.run(['docker', 'exec', '-it', 'px4', 'bash', '-c', 'gz topic -e /gazebo/default/pose/info'],
                                stdout=subprocess.PIPE)

        scanning = False
        for line in result.stdout:
            line = line.decode("utf-8").strip()
            if '"iris"' in line:
                x = 0.0
                y = 0.0
                z = 0.0
                scanning = True
            elif 'x:' in line and scanning:
                x = float(line.split(' ')[1])
            elif 'y:' in line and scanning:
                y = float(line.split(' ')[1])
            elif 'z' in line and scanning:
                scanning = False
                z = float(line.split(' ')[1])
                print("position: ", x, y, z, '\r\n')
        
        pass  # TODO poll gazebo container information

    def poll_network_state(self):
        pass  # TODO poll core container information: The Core API doesn't work?

    def get_observation(self, physical_state, network_state):
        return np.array(self.observation_space.sample())  # TODO

    def get_reward(self, physical_state, network_state):
        return 0  # TODO

    def get_done(self):
        return self.t >= 50

    def step(self, action):
        self.send_actions(action)
        time.sleep(1)
        physical_state = self.poll_gazebo_state()
        network_state = self.poll_network_state()

        print("###########")
        print(self.t)
        print(physical_state)
        print(network_state)
        print("###########", flush=True)

        obs = self.get_observation(physical_state, network_state)
        reward = self.get_reward(physical_state, network_state)
        done = self.get_done()
        self.t += 1
        return obs, reward, done, {}

    def render(self, mode="human"):
        pass


if __name__ == '__main__':
    def env_creator(env_config=None):
        return CoreGazeboEnv()

    # env_creator().step(None)

    ray.init(local_mode=True)
    register_env("Env-v0", env_creator)
    trainer = ppo.PPOTrainer(env="Env-v0", config={
        "num_gpus": 0,
        'num_workers': 1,
        "num_envs_per_worker": 1,
        "gamma": 0.99,
        # "entropy_coeff": 0.01,
        "clip_param": 0.3,
        "kl_target": 0.01,
        "normalize_actions": True,
        # "no_done_at_end": True,
        "framework": 'torch',
    })

    logs = []
    for iteration in range(5):
        log = trainer.train()
        print("Loop {} mean {} ent {}".format(iteration, log['episode_reward_mean'],
                                                      log['info']['learner']['default_policy']['learner_stats']['entropy']))
        if iteration % 50 == 0:
            checkpoint = trainer.save()
            trainer.load_checkpoint(checkpoint)
        logs.append(log)
