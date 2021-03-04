import numpy as np
import pandas as pd

df = pd.DataFrame(
    data = [[1,2,3],[4,5,6],[7,8,9]],
    index = ['a', 'b', 'c'],
    columns = ['x', 'y', 'z']
)

print(df)