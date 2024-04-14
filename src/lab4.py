import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
 
def set_changes():
    n = int(e1.get()) 
    axes = [n, n, n]
    
    data = np.ones(axes, bool)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.voxels(data, facecolors='red', edgecolors='white')

    plt.show()

root = Tk()

e1 = Entry(width=10)
b1 = Button(text="Ввод", command=set_changes)

e1.grid(row=0, column=0)
b1.grid(row=0, column=1)

root.mainloop()