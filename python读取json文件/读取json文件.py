import pandas as pd 
import os 

print(os.getcwd())
print(os.listdir())

df = pd.read_json('补充特征.json')

print(df)