import numpy as np


def reward_computation(samples):
    base_treasure = 10000

    inhabitants = [1, 6, 3, 1, 10, 2, 4, 2, 4, 8]
    multiplier = [10, 80, 37, 17, 90, 31, 50, 20, 73, 89]

    rewards = []

    for i in range(len(inhabitants)):
        rewards.append(base_treasure * multiplier[i] / (inhabitants[i] + samples[i]))

    return rewards


def reward_simulation():
    all_rewards = []
    times = 10000
    for i in range(times):
        # Assume that weights of players opening a specific container are uniformly distributed
        uniform_samples = np.random.uniform(low=0, high=100, size=10)
        normalized_samples = (uniform_samples / np.sum(uniform_samples)) * 100

        # Giving more weight to equilibrium outcomes
        normalized_samples[1] += 50
        normalized_samples[8] += 25
        normalized_samples = (normalized_samples / np.sum(uniform_samples)) * 100

        all_rewards.append(reward_computation(normalized_samples))

    avg_rewards = []
    for j in range(10):
        total = 0
        for i in range(times):
            total += all_rewards[i][j]

        avg_rewards.append(total/times)

    return np.round(avg_rewards), np.round(max(avg_rewards), 0)


print(reward_simulation())
