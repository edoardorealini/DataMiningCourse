import subprocess 
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from os import listdir
from os import rename
from pandas.plotting import table 


def gen_table(df, file_name):
    df = pd.DataFrame(np.array([df["task"], df['init_policy'], df['delta'], df['edgeCut'], df['swaps'], df['migrations']]).transpose(),
                        columns=["Task", "Init_Policy", "Delta", "EdgeCut", "Swaps", "Migrations"])
    # set fig size
    fig, ax = plt.subplots(figsize=(12, 3)) 
    # no axes
    ax.xaxis.set_visible(False)  
    ax.yaxis.set_visible(False)  
    # no frame
    ax.set_frame_on(False)  
    # plot table
    tab = table(ax, df, loc='upper right')  
    # set font manually
    tab.auto_set_font_size(False)
    tab.set_fontsize(8) 
    # save the result
    file_name = file_name.replace(".csv", ".png")
    plt.savefig(file_name)
    #plt.show()


def gen_graph(path_of):
    command = [
        "./plot.sh",
        path_of
    ]

    out = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()

    new_name = path_of.replace(".txt", ".png")
    new_name = new_name.replace("./output/", "")

    time.sleep(3)

    print("New name: " + new_name)

    rename('graph.png', new_name)


if __name__ == '__main__':

    path = './plot/tuning/best_values'
    file_list = ["twitter.csv"]

    for file_name in file_list: #listdir(path):
        df = pd.read_csv(path + '/' + file_name)

        of_list = df['OutFile'].tolist()
        
        print("Generating table png for file:" + file_name)
        gen_table(df, file_name)
        
        '''
        for of in of_list:
            print("Generating plot for file:" + of)
            gen_graph(of)
        '''      
            
    