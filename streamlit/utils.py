import pandas as pd
import numpy as np

def percent_str_to_float(s):
    if isinstance(s, str) and s.endswith("%"):
        return float(s.strip("%"))
    elif pd.isnull(s):
        return np.nan
    else:
        return float(s)