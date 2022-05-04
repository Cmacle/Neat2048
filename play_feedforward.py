from os import getcwd
import pickle
from tkinter import filedialog
import TwentyFortyEight
import tkinter as tk


def create_network(netpath):
    with open(netpath, 'rb') as f:
        data = pickle.load(f)
    genome = data[0]
    config = data[1]
    print(genome, config)



if __name__ == '__main__':
    print("Choose the file.")
    root = tk.Tk()
    root.withdraw()
    netpath = filedialog.askopenfilename(filetypes=[('Pickle','.pkl')], initialdir=getcwd())
    net = create_network(netpath)
    
