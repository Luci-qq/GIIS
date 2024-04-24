from operator import itemgetter
from tkinter import *

pointsMax = []
choice = 0

def delay(x, y):
    c.create_rectangle(x-5, y-5, x+5, y+5, fill='black')

def zero():
    c.create_rectangle(0, 0, 1920, 1080, fill='white')

def get_point():
    with open('points.txt', "r") as file:
        points = []
        for line in file:
            point = line.split()
            result = [int(item) for item in point]
            points.append(result)
        return points

def create_grem():
    points = get_point()
    c.create_rectangle(0, 0, 1920, 1080, outline='white', fill='white')
    global pointsMax
    for point in points:
        c.create_rectangle(point[0], point[1], point[0]+50, point[1]+50, fill='black')
    pointsMax.extend(points)

def razv(event):
    test = pointsMax.copy()
    
    unique_points = []
    for point in test:
        if point not in unique_points:
            unique_points.append(point)
    

    unique_points.sort(key=itemgetter(1, 0))
    intervals = []
    i = 0
    while i < len(unique_points) - 1:
        interval = [unique_points[i]]
        j = i + 1
        while j < len(unique_points) and unique_points[j][1] == interval[0][1]:
            interval.append(unique_points[j])
            j += 1
        intervals.append(interval)
        i = j
    
    for interval in intervals:
        start_x = interval[0][0] + 50
        end_x = interval[-1][0]
        y = interval[0][1]
        for i in range(start_x, end_x, 50):
            if not any(point[0] == i and point[1] == y for point in pointsMax):
                c.create_rectangle(i, y, i + 50, y + 50, fill='cyan', outline='black')
                c.after(100, root.update()) 

    
def simple_Z(event):
    x = event.x - (event.x % 50)
    y = event.y - (event.y % 50)
    stack = [[x, y]]
    visited = []
    while len(stack) > 0:
        c.create_rectangle(stack[0][0], stack[0][1], stack[0][0]+50, stack[0][1]+50, fill='cyan', outline='black')
        visited.append(stack[0])
        test_point = stack[0]
        stack.pop(0)
        points = []
        points.append([test_point[0], test_point[1] + 50])
        points.append([test_point[0] + 50, test_point[1]])
        points.append([test_point[0], test_point[1] - 50])
        points.append([test_point[0] - 50, test_point[1]])
        for point in points:
            if point not in visited and point not in pointsMax:
                stack.insert(0, point)
        c.after(100, root.update())

def str_Z(event):
    x = event.x - (event.x % 50)
    y = event.y - (event.y % 50)
    stack = [[x, y]]
    visited = []
    while len(stack) > 0:
        c.create_rectangle(stack[0][0], stack[0][1], stack[0][0]+50, stack[0][1]+50, fill='cyan', outline='black')
        visited.append(stack[0])
        test_point = stack[0]
        stack.pop(0)
        point = [test_point[0] - 50, test_point[1]]
        x_right = 0
        while point not in visited and point not in pointsMax:
            c.create_rectangle(point[0], point[1], point[0]+50, point[1]+50, fill='cyan', outline='black')
            visited.append(point)
            point = [point[0] - 50, point[1]]
            c.after(100, root.update())
        point = [test_point[0] + 50, test_point[1]]
        x_right = test_point[0]
        while point not in visited and point not in pointsMax:
            c.create_rectangle(point[0], point[1], point[0]+50, point[1]+50, fill='cyan', outline='black')
            visited.append(point)
            x_right = point[0]
            point = [point[0] + 50, point[1]]
            c.after(100, root.update())
        pointUp = [x_right, test_point[1]+50]
        pointDown = [x_right, test_point[1]-50]
        if pointDown not in visited and pointDown not in pointsMax:
            stack.insert(0, pointDown)
        if pointUp not in visited and pointUp not in pointsMax:
            stack.insert(0, pointUp)

def clear_canvas():
    c.delete("all")

def reset_all():
    clear_canvas()
    global pointsMax
    pointsMax = []

root = Tk()

mainmenu = Menu(root)
root.config(menu=mainmenu)
segmentMenu = Menu(mainmenu, tearoff=0)
segmentMenu.add_command(label="Грэхам", command=create_grem)

methodMenu = Menu(mainmenu, tearoff=0)
methodMenu.add_command(label="Простой затравочный", command=lambda: bind_method(simple_Z))
methodMenu.add_command(label="Затравочный построчный", command=lambda: bind_method(str_Z))
methodMenu.add_command(label="Растровой развертки", command=lambda: bind_method(razv))

mainmenu.add_cascade(label="Алгоритм", menu=segmentMenu)
mainmenu.add_cascade(label="Метод", menu=methodMenu)

c = Canvas(width=1000, height=1000, bg='white')

def bind_method(method):
    c.unbind("<Button-3>")
    c.bind("<Button-3>", method)

c.pack(side=LEFT)

clearButton = Button(root, text="Очистить холст", command=reset_all)
clearButton.pack(side=TOP)

root.mainloop()