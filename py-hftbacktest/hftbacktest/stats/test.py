import numpy as np
from hftbacktest.stats import LinearAssetRecord

recorder = np.load("test_run.npz")['0']

stats = LinearAssetRecord(recorder).stats()

stats.plot()