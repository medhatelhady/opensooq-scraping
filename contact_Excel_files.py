
import os
import pandas as pd
from glob import glob

# name of folder that you would like to gather all data stored in it
FOLDER_NAME = 'Gathered_data'

if not os.path.exists(FOLDER_NAME):
    os.makedirs(FOLDER_NAME)


# A list of all joined files is returned
joined_list = glob("./"+FOLDER_NAME+'/*.csv')
  
# Finally, the files are joined
df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)
df = df.drop_duplicates()
df.to_csv('./Gathered_data/'+ FOLDER_NAME+'.csv', index=False)
