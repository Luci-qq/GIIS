import tkinter as tk
from tkinter import filedialog

class Lab5(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title = 'smth'
        self.wm_state('zoomed')
        self.points = []
        self.create_canvas()
        self.create_debugger()
        self.create_toolbar()
        self.create_x_y_inputs(0)
        self.file_picker_button = tk.Button(self.toolbar_frame,text='Выбрать файл',command=self.open_file)
        self.file_picker_button.pack(pady=10,side=tk.TOP)

    def create_canvas(self):
        self.canvas_frame = tk.Frame(self.master)
        self.canvas = tk.Canvas(self.canvas_frame,width=1000,height=1000,bg='white',highlightbackground='gray')
        self.canvas.pack(padx=5,pady=5)
        self.canvas_frame.pack(side=tk.LEFT)
        
    def create_debugger(self):
        self.debug_text_frame = tk.Frame(self.master)
        self.debug_text_frame.pack(side=tk.LEFT,expand=True)

        self.debug_text = tk.Text(self.debug_text_frame,height=48,width=45)
        self.debug_text.config(state=tk.DISABLED)
        self.debug_text.pack()

    def create_toolbar(self):
        self.toolbar_frame = tk.Frame(self.master)
        self.toolbar_frame.pack(anchor=tk.CENTER)

        self.debug_var = tk.BooleanVar()
        self.debug_checkbox = tk.Checkbutton(self.toolbar_frame,text='Отладочный режим',variable=self.debug_var,command=self.toggle_debug_mode)
        self.debug_checkbox.pack()

        self.graphics_type = tk.StringVar()
        self.graphics_type.set('Алгоритм Джарвиса')
        self.graphics_menu = tk.OptionMenu(self.toolbar_frame,self.graphics_type, 
                                           *['Алгоритм Джарвиса','Алгоритм Грэхема'])
        self.graphics_menu.pack()

    def create_x_y_inputs(self,points_value):
        self.x_y_columns_frame = tk.Frame(self.toolbar_frame)
        self.x_y_columns_frame.pack(side=tk.TOP)

        self.column1 = tk.Frame(self.x_y_columns_frame)
        self.column1.pack(side=tk.LEFT)
        self.column2 = tk.Frame(self.x_y_columns_frame)
        self.column2.pack(side=tk.LEFT)

        self.entries_points = []
        self.labels_points = []

        for _ in range(1, points_value+1):
            dot_x = tk.Label(self.column1,text=f'X{_}:')
            self.labels_points.append(dot_x)
            entry_dot_x = tk.Entry(self.column1,width=10)
            dot_x.pack(side=tk.TOP)
            entry_dot_x.pack(side=tk.TOP)
            self.entries_points.append(entry_dot_x)

            dot_y = tk.Label(self.column2,text=f'Y{_}:')
            self.labels_points.append(dot_y)
            entry_dot_y= tk.Entry(self.column2,width=10)
            dot_y.pack(side=tk.TOP)
            entry_dot_y.pack(side=tk.TOP)
            self.entries_points.append(entry_dot_y)
            
    def create_buttons(self):
        self.draw_button=tk.Button(self.toolbar_frame,text='Нарисовать',command=self.drawer)
        self.draw_button.pack(pady=10,side=tk.TOP)

    def toggle_debug_mode(self):
        if self.debug_var.get():
            self.debug_text.config(state=tk.NORMAL)
            self.debug_text.insert(tk.END,"Режим отладки включен. \n")
            self.debug_text.config(state=tk.DISABLED)
        else:
            self.debug_text.config(state=tk.NORMAL)
            self.debug_text.insert(tk.END,"Режим отладки отключен. \n")
            self.debug_text.config(state=tk.DISABLED)

    def draw_utility(self,x,y):
        self.canvas.create_rectangle(x-5,y-5,x+5,y+5, outline='black',fill='white')
    
    def draw_segment(self, segment):
        self.canvas.create_line(segment[0][0], segment[0][1], segment[1][0], segment[1][1])
    
    def clear_canvas(self):
        self.canvas.delete('all')

    def open_file(self):
        file_path = filedialog.askopenfilename()
        self.points.clear()
        if file_path:
            with open(file_path, "r") as file:
                for line in file:
                    point = line.split()
                    result = [int(item) for item in point]
                    self.points.append(result)
                
        if self.entries_points:
            self.x_y_columns_frame.destroy()
            self.draw_button.destroy()
            for label,entry in zip(self.labels_points,self.entries_points):
                label.destroy()
                entry.destroy()
            
            self.labels_points.clear()
            self.entries_points.clear()
            self.draw_button.destroy()
            
        self.create_x_y_inputs(len(self.points))
        for i, (entry_x, entry_y) in enumerate(zip(self.entries_points[::2], self.entries_points[1::2])):
            entry_x.insert(0, self.points[i][0])
            entry_y.insert(0, self.points[i][1])  
        self.create_buttons()
        
    def graham_handler(self):
        points = self.points.copy()
        graham_points = []
        sorted_points = sorted(points, key=lambda point: point[1])   
        first_point = sorted_points[0]
        sorted_points.remove(first_point)
        sorted_points = sorted(sorted_points, key=lambda point: (first_point[1] - point[1]) / (first_point[0] - point[0]))
        graham_points.append(first_point)
        graham_points.insert(0, sorted_points[0])
        sorted_points.remove(sorted_points[0])
        for point in sorted_points:
            while (graham_points[0][0] - graham_points[1][0]) * (point[1] - graham_points[0][1]) - (graham_points[0][1] - graham_points[1][1]) * (point[0] - graham_points[0][0]) < 0:
                graham_points.pop(0)
            graham_points.insert(0, point)
        graham_points.append(graham_points[0])
        if self.debug_var.get():
            self.debug_text.config(state=tk.NORMAL)
            self.debug_text.insert(tk.END, "Выпуклая оболочка (метод Грэхема):\n")
            for point in graham_points:
                self.debug_text.insert(tk.END, f"{point}\n")
            self.debug_text.see(tk.END)
            self.debug_text.config(state=tk.DISABLED)
        return graham_points

    def draw_gram(self):
        gram_points = self.graham_handler()
        points = self.get_points()
        for point in points:
            self.draw_utility(point[0], point[1])
        for point in gram_points:
            self.canvas.create_rectangle(point[0]-5, point[1]-5, point[0]+5, point[1]+5, outline='black', fill='green')
        
        segments = []
        for i in range(len(gram_points)):
            segment = []
            if i == 0:
                segment.append(gram_points[len(gram_points)-1])
                segment.append(gram_points[i])
            else:
                segment.append(gram_points[i-1])
                segment.append(gram_points[i])
            segments.append(segment)
        
        for segment in segments:
            self.after(100, self.draw_segment, segment)

    def jarvis_handler(self):
        points = self.points.copy()
        convex_hull = []
        sorted_points = sorted(points, key=lambda point: point[1])   
        first_point = sorted_points[0]
        sorted_points.remove(first_point)
        sorted_points = sorted(sorted_points, key=lambda point: (first_point[1] - point[1]) / (first_point[0] - point[0]))
        sorted_points.insert(0, first_point)
        convex_hull.append(first_point)
        convex_hull.append(sorted_points[1])
        remaining_points = sorted_points
        remaining_points.pop(1)
        i = 1   
        while convex_hull[i] != convex_hull[0]:
            remaining_points = sorted(remaining_points, key=lambda s: (abs((convex_hull[i][0] - convex_hull[i - 1][0]) * (s[0] - convex_hull[i][0])) + abs((convex_hull[i][1] - convex_hull[i - 1][1]) * (s[1] - convex_hull[i][1]))) / (((convex_hull[i][0] - convex_hull[i - 1][0]) ** 2 + (convex_hull[i][1] - convex_hull[i - 1][1]) ** 2) ** 0.5 * ((s[0] - convex_hull[i][0]) ** 2 + (s[1] - convex_hull[i][1]) ** 2) ** 0.5))
            convex_hull.append(remaining_points[0])
            remaining_points.pop(0)
            i += 1
        if self.debug_var.get():
            self.debug_text.config(state=tk.NORMAL)
            self.debug_text.insert(tk.END, "Выпуклая оболочка (метод Джарвиса):\n")
            for point in convex_hull:
                self.debug_text.insert(tk.END, f"{point}\n")
            self.debug_text.see(tk.END)
            self.debug_text.config(state=tk.DISABLED)
        return convex_hull

    def draw_jarvis(self):
        points = self.jarvis_handler()
        points.remove(points[len(points)-1])
        p = self.get_points()
        for point in p:
            self.draw_utility(point[0], point[1])
            
        for point in points:
            self.canvas.create_rectangle(point[0]-5, point[1]-5, point[0]+5, point[1]+5, outline='black', fill='green')

        segments = []
        for i in range(len(points)):
            segment = []
            segment.append(points[i])
            if i == len(points)-1:
                segment.append(points[0])
            else:
                segment.append(points[i+1])
            segments.append(segment)

        for segment in segments:
            self.after(100, self.draw_segment, segment)

    def get_points(self):
        self.points.clear()
        for i in range(0, len(self.entries_points), 2):
            x = int(self.entries_points[i].get())
            y = int(self.entries_points[i + 1].get()) 
            self.points.append([x, y])
        return self.points

    def drawer(self):
        if self.graphics_type.get() == 'Алгоритм Грэхема':
            self.clear_canvas()
            self.points = self.get_points()
            self.draw_gram()
        elif self.graphics_type.get() == 'Алгоритм Джарвиса':
            self.clear_canvas()
            self.points = self.get_points()
            self.draw_jarvis()

if __name__ == '__main__':
    Lab5().mainloop()