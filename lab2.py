import tkinter as tk
import numpy as np

TIMER = 1
NUM_POINTS = 1000


class FigureDrawer:
    def __init__(self, master):
        self.master = master
        self.master.title("Графический редактор")

        self.canvas_width = 400
        self.canvas_height = 400
        self.center_x = 200
        self.center_y = 200
        self.debug_mode = False

        self.points = []
        self.hypepoints_up = []
        self.hypepoints_down = []

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side=tk.LEFT)

        self.toolbar = tk.Frame(self.master)
        self.toolbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.debug_var = tk.BooleanVar()
        self.debug_checkbox = tk.Checkbutton(self.toolbar, text="Отладочный режим", variable=self.debug_var,command=self.toggle_debug_mode)
        self.debug_checkbox.pack()

        self.figure_type = tk.StringVar()
        self.figure_type.set("Окружность")
        self.figure_menu = tk.OptionMenu(self.toolbar, self.figure_type, "Окружность", "Эллипс", "Гипербола", "Парабола")
        self.figure_menu.pack()

        self.axis_a = tk.Label(master,text='Полуось a: ')
        self.entry_axis_a =tk.Entry(master)
        self.axis_b = tk.Label(master,text= 'Полуось b:')
        self.entry_axis_b = tk.Entry(master)
        
        self.axis_a.pack(after=self.figure_menu)
        self.entry_axis_a.pack(after=self.axis_a)
        self.axis_b.pack(after=self.entry_axis_a)
        self.entry_axis_b.pack(after=self.axis_b)
        
        self.draw_button=tk.Button(text='Нарисовать',command=self.draw_conic)
        self.draw_button.pack(after=self.entry_axis_b,pady=10)

        self.debug_text = tk.Text(self.master, height=25, width=40)
        self.debug_text.pack(side=tk.RIGHT)

        self.debug_text.insert(tk.END, "Построение: \n")
        self.figure_type.trace_add("write", self.update_fields)

    def toggle_debug_mode(self):
        self.debug_mode = self.debug_var.get()
        if self.debug_mode:
            self.debug_text.insert(tk.END,"Режим отладки включен. \n")
        else:
            self.debug_text.insert(tk.END,"Режим отладки отключен. \n")
    
    def update_fields(self,*args):
        if self.figure_type.get() == "Окружность":
            self.axis_a.config(text="Радиус окружности:")
            self.entry_axis_b.config(state=tk.DISABLED)
        elif self.figure_type.get() == "Парабола":
            self.axis_a.config(text="Значение коэффициента:")
            self.entry_axis_b.config(state=tk.DISABLED)
        else:
            self.axis_a.config(text="Полуось a:")
            self.entry_axis_b.config(state=tk.NORMAL)

    def draw_conic(self):
        try:
            self.clear_canvas()
            a = float(self.entry_axis_a.get())
            if self.figure_type.get() == "Эллипс":
                b = float(self.entry_axis_b.get())
                self.get_ellipse_points(a, b)
                self.draw()
            elif self.figure_type.get() == "Гипербола":
                b = float(self.entry_axis_b.get())
                self.get_hyperbola_points(a, b)
                self.draw()
            elif self.figure_type.get() == "Окружность":
                self.get_ellipse_points(a, a)
                self.draw()
            elif self.figure_type.get() == "Парабола":
                self.get_parabola_points(a)
                self.draw()
        except ValueError:
            self.debug_text.insert(tk.END,'Ошибка, отсутствуют параметры фигуры.')

#x = h + a * cos(O)
#y = k + b * sin(O)
    def get_ellipse_points(self, a, b):
        self.points.clear()
        for angle in np.linspace(0, 2 * np.pi, NUM_POINTS):
            x = self.center_x + a * np.cos(angle)
            y = self.center_y + b * np.sin(angle)
            self.points.append((x, y))

#y = ax^2
    def get_parabola_points(self, a):
        self.points.clear()
        for x in np.linspace(-10, 10, NUM_POINTS):
            y = a * x ** 2
            screen_x = self.center_x + x * 20
            screen_y = self.center_y - y * 20 
            if 0 <= screen_y <= self.canvas_height:
                self.points.append((screen_x, screen_y))

    def get_hyperbola_points(self, a, b):
        self.hypepoints_up = []
        self.hypepoints_down = []
        for x in np.linspace(self.center_x - a - 200, self.center_x + a + 200, NUM_POINTS):
            y1 = self.center_y + b * np.sqrt(1 + ((x - self.center_x) / a) ** 2)
            y2 = self.center_y - b * np.sqrt(1 + ((x - self.center_x) / a) ** 2)
            if 0 <= y1 <= self.canvas_height:
                self.hypepoints_up.append((x, y1))
            if 0 <= y2 <= self.canvas_height:
                self.hypepoints_down.append((x, y2))

    def draw(self):
        if self.debug_mode:
            if self.figure_type.get() == 'Гипербола':
               self.draw_debug(self.hypepoints_up)
               self.draw_debug(self.hypepoints_down)
            else:
                self.draw_debug(self.points)
        else:
            if self.figure_type.get() == 'Гипербола':
                self.draw_hype()
            else:
                self.draw_default(self.points)
               
    def draw_debug(self,points):
        for point in points:
            self.canvas.create_rectangle(point[0], point[1], point[0], point[1], fill="black")
            self.debug_text.insert(tk.END, f"({round(point[0])}, {round(point[1])})\n")
            self.debug_text.see(tk.END)  
            self.master.update()  
            self.master.after(TIMER) 

    def draw_default(self,points):
        for point in points:
            self.canvas.create_rectangle(point[0], point[1], point[0], point[1], fill="black")

    def draw_hype(self):
        for point in self.hypepoints_up:
            self.canvas.create_rectangle(point[0], point[1], point[0], point[1], fill="black")
        for point in self.hypepoints_down:
            self.canvas.create_rectangle(point[0], point[1], point[0], point[1], fill="black")

    def clear_canvas(self):
            self.canvas.delete("all")


if __name__=='__main__':
    root = tk.Tk()
    app = FigureDrawer(root)
    root.mainloop()