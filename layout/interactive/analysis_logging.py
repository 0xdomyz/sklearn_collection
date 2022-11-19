"""Analyse random data and make summary"""
import logging
import random
from pathlib import Path

import numpy as np
import pandas as pd

# __file__ = r'E:\git_repo\python_collection\layout\interactive\analysis_logging.py'
_module_path, _file_name = Path(__file__).parent, Path(__file__).stem
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(_module_path / f"{_file_name}_log.log", "w"),
    ],
)
logger.info(__doc__)

seed = 0
n = 100
logger.info(f"{seed = }")
logger.info(f"{n = }")

random.seed(seed)
df = pd.DataFrame(
    dict(
        cat=[random.choice(["a", "b", "c"]) for i in range(n)],
        score=[random.random() for i in range(n)],
    )
)
res = df.groupby("cat").agg(score=("score", np.mean)).reset_index()

_result_path = _module_path / f"{_file_name}_result.csv"
res.to_csv(_result_path)
logger.info(f"Results saved to {_result_path}")
