from operator import itemgetter
from tkinter import *
from scipy.spatial import Delaunay, voronoi_plot_2d
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt

active_edge = []
pointsMax = []
choice = 0

def zero():
    global active_edge, pointsMax
    active_edge = []
    pointsMax = []
    c.delete("all")

def Delone(event):
    global pointsMax
    point = []
    point.append(event.x)
    point.append(event.y)
    c.create_oval(point[0]-5, point[1]-5, point[0]+5, point[1]+5, fill='black')
    pointsMax.append(point)
    triangulate(point)

def triangulate(point_new):
    global active_edge
    if len(pointsMax) > 2:
        tri = Delaunay(pointsMax)
        for triangle in tri.simplices:
            p1, p2, p3 = triangle
            c.create_line(pointsMax[p1][0], pointsMax[p1][1], pointsMax[p2][0], pointsMax[p2][1])
            c.create_line(pointsMax[p2][0], pointsMax[p2][1], pointsMax[p3][0], pointsMax[p3][1])
            c.create_line(pointsMax[p3][0], pointsMax[p3][1], pointsMax[p1][0], pointsMax[p1][1])

def close(event):
    global active_edge
    for edge1 in active_edge:
        for edge2 in active_edge:
            if edge1 != edge2:
                if edge1[0] == edge2[0]:
                    c.create_line(edge1[1][0], edge1[1][1], edge2[1][0], edge2[1][1])
                    active_edge.remove(edge1)
                    active_edge.remove(edge2)
                elif edge1[1] == edge2[0]:
                    c.create_line(edge1[0][0], edge1[0][1], edge2[1][0], edge2[1][1])
                    active_edge.remove(edge1)
                    active_edge.remove(edge2)

def Voron(event):
    vor = Voronoi(pointsMax)
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax)  
    plt.show()

root = Tk()
mainmenu = Menu(root)
root.config(menu=mainmenu)
segmentMenu = Menu(mainmenu, tearoff=0)
segmentMenu.add_command(label="Очистить", command=zero)
mainmenu.add_cascade(label="Алгоритм", menu=segmentMenu)
methodMenu = Menu(mainmenu, tearoff=0)
methodMenu.add_command(label="Триангуляция Делоне", command=lambda: set_choice(0))
methodMenu.add_command(label="Диаграмма Вороного", command=lambda: set_choice(1))
mainmenu.add_cascade(label="Метод", menu=methodMenu)

def set_choice(new_choice):
    global choice
    choice = new_choice

c = Canvas(width=1000, height=1000, bg='white')
c.bind("<Button-1>", Delone)
c.bind("<Button-3>", lambda event: Voron(event) if choice == 1 else triangulate(event.x, event.y))
c.grid(row=6, column=3)
root.mainloop()