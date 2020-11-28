import matplotlib.pyplot as plt
import src.tracker
import numpy as np
from collections import defaultdict

# Visualization of Map with Labels
positions = defaultdict(list)
xa = np.random.randint(255, size=1000)
ya = np.random.randint(255, size=1000)
for x, y in zip(xa, ya):
    position = src.tracker.divide_map(x, y)
    positions[position].append((x, y))

fig, ax = plt.subplots()
for position, color in zip(positions, ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#641e16', '#ba4a00']):
    print(position, positions[position])
    x, y = zip(*positions[position])
    ax.scatter(x, y, c=color, label=position)

ax.legend()
ax.grid(True)
plt.show()
# plt.scatter(positions[0], positions[1], )