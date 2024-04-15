import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

class Lab4(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lab 4")
        self.wm_state('zoomed')

        self.toolbar_frame = tk.Frame(self.master)
        self.toolbar_frame.pack(anchor=tk.NE)

        self.label_voxels = tk.Label(self.toolbar_frame, text = 'Количество вокселей:')         
        self.label_voxels.pack(side=tk.TOP)
    
        self.entry_voxels = tk.Entry(self.toolbar_frame)
        self.entry_voxels.pack(side=tk.TOP)

        self.button_enter = tk.Button(self.toolbar_frame, text="Ввод", command=self.set_changes)
        self.button_enter.pack(side=tk.TOP)
        
    def set_changes(self):
        n = int(self.entry_voxels.get()) 
        axes = [n, n, n]
        
        data = np.ones(axes, bool)
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.voxels(data, facecolors='red', edgecolors='white')
    
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

if __name__ == "__main__":
    app = Lab4()
    app.mainloop()
