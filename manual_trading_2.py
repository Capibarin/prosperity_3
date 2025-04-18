import numpy as np

base_treasure = 10000
game_round = 2

if round == 2:
    inhabitants = [1, 6, 3, 1, 10, 2, 4, 2, 4, 8]
    multiplier = [10, 80, 37, 17, 90, 31, 50, 20, 73, 89]
    arr_size = 10
else:
    inhabitants = [6, 4, 7, 2, 4, 8, 1, 3, 4, 10, 1, 3, 4, 15, 2, 3, 5, 2, 3, 2]
    multiplier = [80, 50, 83, 31, 60, 89, 10, 37, 70, 90, 17, 40, 73, 100, 20, 41, 79, 23, 47, 30]
    arr_size = 20

# pos 12: 73x4, 16 79x5, 0 80x6, 18 47x3, cond: 6 10x1, 14 20x2
def reward_computation(samples):
    rewards = []

    for i in range(len(inhabitants)):
        rewards.append(base_treasure * multiplier[i] / (inhabitants[i] + samples[i]))

    return rewards


def reward_simulation():
    all_rewards = []
    times = 10000
    for i in range(times):
        # Assume that weights of players opening a specific container are uniformly distributed
        uniform_samples = np.random.uniform(low=0, high=100, size=arr_size)
        normalized_samples = (uniform_samples / np.sum(uniform_samples)) * 100

        # Giving more weight to equilibrium outcomes
        normalized_samples[12] += 80
        normalized_samples[16] += 70
        normalized_samples[0] += 60
        normalized_samples[18] += 50
        # Previous rounds
        normalized_samples[6] += 80
        normalized_samples[14] += 80
        normalized_samples = (normalized_samples / np.sum(normalized_samples)) * 100

        all_rewards.append(reward_computation(normalized_samples))

    avg_rewards = []
    for j in range(arr_size):
        total = 0
        for i in range(times):
            total += all_rewards[i][j]

        avg_rewards.append(total/times)

    return np.round(avg_rewards).tolist(), int(np.round(max(avg_rewards), 0))


print(reward_simulation())

# Rewards > 100k: 2 3 4 5 9 12 15 16 20
