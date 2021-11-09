# for i in range(1):
#     print(1)

import numpy as np

np.random.seed(12345)
for i in range(10):
    action = np.random.randint(0, 11)
    un = np.random.uniform()
    sample_index = np.random.choice(8, 32)
    print(un)
    print(action)
    print(sample_index)