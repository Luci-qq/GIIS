import tkinter as tk 

DELAY = 0.5

class CurveDrawer(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title = 'smth'
        self.wm_state('zoomed')
        self.canvas_frame = tk.Frame(self.master)
        self.canvas = tk.Canvas(self.canvas_frame,width=1000,height=1000,bg='white',highlightbackground='gray')
        self.canvas.pack(padx=5,pady=5)
        self.canvas_frame.pack(side=tk.LEFT)

        self.debug_text_frame = tk.Frame(self.master)
        self.debug_text_frame.pack(side=tk.LEFT,expand=True)

        self.debug_text = tk.Text(self.debug_text_frame,height=48,width=45)
        self.debug_text.config(state=tk.DISABLED)
        self.debug_text.pack()

        self.toolbar_frame = tk.Frame(self.master)
        self.toolbar_frame.pack(anchor=tk.CENTER)

        self.debug_var = tk.BooleanVar()
        self.debug_checkbox = tk.Checkbutton(self.toolbar_frame,text='Отладочный режим',variable=self.debug_var,command=self.toggle_debug_mode)
        self.debug_checkbox.pack()

        self.graphics_type = tk.StringVar()
        self.graphics_type.set('Кривая Безье')
        self.graphics_menu = tk.OptionMenu(self.toolbar_frame,self.graphics_type, 
                                           *['Кривая Безье','Форма Эрмита','В-сплайн'])
        self.graphics_menu.pack()

        self.x_y_columns_frame = tk.Frame(self.toolbar_frame)
        self.x_y_columns_frame.pack(side=tk.TOP)

        self.column1 = tk.Frame(self.x_y_columns_frame)
        self.column1.pack(side=tk.LEFT)
        
        self.column2 = tk.Frame(self.x_y_columns_frame)
        self.column2.pack(side=tk.LEFT)

        self.dot_x1 = tk.Label(self.column1,text='X1:')
        self.entry_dot_x1 = tk.Entry(self.column1,width=10)
        self.dot_x1.pack(side=tk.TOP)
        self.entry_dot_x1.pack(side=tk.TOP)

        self.dot_y1 = tk.Label(self.column2,text='Y1:')
        self.entry_dot_y1= tk.Entry(self.column2,width=10)
        self.dot_y1.pack(side=tk.TOP)
        self.entry_dot_y1.pack(side=tk.TOP)

        self.dot_x2 = tk.Label(self.column1,text='X2:')
        self.entry_dot_x2 = tk.Entry(self.column1,width=10)
        self.dot_x2.pack(side=tk.TOP)
        self.entry_dot_x2.pack(side=tk.TOP)

        self.dot_y2 = tk.Label(self.column2,text='Y2:')
        self.entry_dot_y2= tk.Entry(self.column2,width=10)
        self.dot_y2.pack(side=tk.TOP)
        self.entry_dot_y2.pack(side=tk.TOP)

        self.dot_x3 = tk.Label(self.column1,text='X3:')
        self.entry_dot_x3 = tk.Entry(self.column1,width=10)
        self.dot_x3.pack(side=tk.TOP)
        self.entry_dot_x3.pack(side=tk.TOP)

        self.dot_y3 = tk.Label(self.column2,text='Y3:')
        self.entry_dot_y3= tk.Entry(self.column2,width=10)
        self.dot_y3.pack(side=tk.TOP)
        self.entry_dot_y3.pack(side=tk.TOP)


        self.dot_x4 = tk.Label(self.column1,text='X4:')
        self.entry_dot_x4 = tk.Entry(self.column1,width=10)
        self.dot_x4.pack(side=tk.TOP)
        self.entry_dot_x4.pack(side=tk.TOP)

        self.dot_y4 = tk.Label(self.column2,text='Y4:')
        self.entry_dot_y4= tk.Entry(self.column2,width=10)
        self.dot_y4.pack(side=tk.TOP)
        self.entry_dot_y4.pack(side=tk.TOP)

        self.draw_button=tk.Button(self.toolbar_frame,text='Нарисовать',command=self.drawer)
        self.draw_button.pack(pady=10,side=tk.TOP)

    def toggle_debug_mode(self):
        self.debug_mode = self.debug_var.get()
        if self.debug_mode:
            self.debug_text.config(state=tk.NORMAL)
            self.debug_text.insert(tk.END,"Режим отладки включен. \n")
            self.debug_text.config(state=tk.DISABLED)
        else:
            self.debug_text.config(state=tk.NORMAL)
            self.debug_text.insert(tk.END,"Режим отладки отключен. \n")
            self.debug_text.config(state=tk.DISABLED)

    def get_points(self):
        return (float)(self.entry_dot_x1.get()), \
            (float)(self.entry_dot_y1.get()), \
            (float)(self.entry_dot_x2.get()), \
            (float)(self.entry_dot_y2.get()), \
            (float)(self.entry_dot_x3.get()), \
            (float)(self.entry_dot_y3.get()), \
            (float)(self.entry_dot_x4.get()), \
            (float)(self.entry_dot_y4.get())      

    def draw_utility(self,x,y):
        self.canvas.create_rectangle(x,y,x,y, fill='black')

    def create_B_spline(self):
        self.clear_canvas()
        x1,y1,x2,y2,x3,y3,x4,y4 =  self.get_points()
        t = 0
        self.canvas.create_rectangle(x1-5,y1-5,x1+5,y1+5, outline='red', fill='red')
        self.canvas.create_rectangle(x4-5,y4-5,x4+5,y4+5, outline='red', fill='red')
        self.canvas.create_rectangle(x2-5,y2-5,x2+5,y2+5, outline='red', fill='red')
        self.canvas.create_rectangle(x3-5,y3-5,x3+5,y3+5, outline='red', fill='red')
        x1_prev,y1_prev = x1 + 2*(x2-x1) / 3, y1 + 2*(y2-y1) / 3
        x2_prev,y2_prev = x2 + (x3-x2) / 3, y2 + (y3-y2) / 3
        x3_prev,y3_prev = x2 + 2*(x3-x2) / 3, y2 + 2*(y3-y2) / 3
        x4_prev,y4_prev = x3 + (x4-x3) / 3, y3 + (y4-y3) / 3
        x1_new, y1_new = x1_prev + (x2_prev - x1_prev) / 2, y1_prev + (y2_prev - y1_prev) /2
        x2_new,y2_new = x2_prev,y2_prev
        x3_new,y3_new = x3_prev,y3_prev
        x4_new, y4_new = x3_prev + (x4_prev - x3_prev) / 2, y3_prev + (y4_prev - y3_prev) /2
        while t <= 1:
            x = (1 - t)**3 * x1_new + 3*t*(1 - t)**2 * x2_new + 3*t**2 * (1-t) * x3_new + t**3 * x4_new
            y = (1 - t)**3 * y1_new + 3*t*(1 - t)**2 * y2_new + 3*t**2 * (1-t) * y3_new + t**3 * y4_new
            if self.debug_mode: 
                self.debug_text.config(state = tk.NORMAL)
                self.debug_text.insert(tk.END,f'Текущая точка: {round(x,3)},{round(y,3)}\n')
                self.debug_text.config(state=tk.DISABLED)
                self.debug_text.see(tk.END)
            self.after(1, self.draw_utility(x,y))
            self.update()
            t+=0.001

    def create_bezie(self):
        self.clear_canvas()
        x1,y1,x2,y2,x3,y3,x4,y4 = self.get_points()
        t = 0
        self.canvas.create_rectangle(x1-5,y1-5,x1+5,y1+5, outline='red', fill='red')
        self.canvas.create_rectangle(x4-5,y4-5,x4+5,y4+5, outline='red', fill='red')
        self.canvas.create_rectangle(x2-5,y2-5,x2+5,y2+5, outline='red', fill='red')
        self.canvas.create_rectangle(x3-5,y3-5,x3+5,y3+5, outline='red', fill='red')
        while t <= 1:
            x = (1 - t)**3 * x1 + 3*t*(1 - t)**2 * x2 + 3*t**2 * (1-t) * x3 + t**3 * x4
            y = (1 - t)**3 * y1 + 3*t*(1 - t)**2 * y2 + 3*t**2 * (1-t) * y3 + t**3 * y4
            if self.debug_mode: 
                self.debug_text.config(state = tk.NORMAL)
                self.debug_text.insert(tk.END,f'Текущая точка: {round(x,3)},{round(y,3)}\n')
                self.debug_text.config(state=tk.DISABLED)
                self.debug_text.see(tk.END)
            self.after(1, self.draw_utility(x,y))
            self.update()
            t+=0.001

    def create_ermit(self):
        self.clear_canvas()
        x1,y1,x2,y2,x3,y3,x4,y4 = self.get_points()
        t = 0
        self.canvas.create_rectangle(x1-5,y1-5,x1+5,y1+5, outline='red', fill='red')
        self.canvas.create_rectangle(x2-5,y2-5,x2+5,y2+5, outline='red', fill='red')
        self.canvas.create_line(x1, y1, x1 + x3, y1 + y3, fill='green',
                width=3, arrow=tk.LAST,
                activefill='lightgreen',
                arrowshape=(10, 20, 10))
        self.canvas.create_line(x2, y2, x2 + x4, y2 + y4, fill='green',
                width=3, arrow=tk.LAST,
                activefill='lightgreen',
                arrowshape=(10, 20, 10))
        
        while t <= 1:
            x = x1 + x3*t + (-3*x1 + 3*x2 - 2*x3 - x4)* t**2 + (2*x1 - 2*x2 +x3 +x4)* t**3
            y = y1 + y3*t + (-3*y1 + 3*y2 - 2*y3 - y4)* t**2 + (2*y1 - 2*y2 +y3 +y4)* t**3
            if self.debug_mode: 
                self.debug_text.config(state = tk.NORMAL)
                self.debug_text.insert(tk.END,f'Текущая точка: {round(x,3)},{round(y,3)}\n')
                self.debug_text.config(state=tk.DISABLED)
                self.debug_text.see(tk.END)
            self.after(1, self.draw_utility(x,y))
            self.update()
            t+=0.001

    def drawer(self):
        if self.debug_mode:
            selected_graphics = self.graphics_type.get()
            debug_info = f"Выбранный метод рисования: {selected_graphics}\n"
            debug_info += "Введенные точки:\n"
            debug_info += f"X1: {self.entry_dot_x1.get()}, Y1: {self.entry_dot_y1.get()}\n"
            debug_info += f"X2: {self.entry_dot_x2.get()}, Y2: {self.entry_dot_y2.get()}\n"
            debug_info += f"X3: {self.entry_dot_x3.get()}, Y3: {self.entry_dot_y3.get()}\n"
            debug_info += f"X4: {self.entry_dot_x4.get()}, Y4: {self.entry_dot_y4.get()}\n"
            self.debug_text.config(state=tk.NORMAL)
            self.debug_text.insert(tk.END, debug_info)
            self.debug_text.config(state=tk.DISABLED)
        if self.graphics_type.get() == 'Кривая Безье':
            self.create_bezie()
        elif self.graphics_type.get() == 'Форма Эрмита':
            self.create_ermit()
        else:
            self.create_B_spline()

    def clear_canvas(self):
        self.canvas.delete('all')


smth = CurveDrawer()
smth.mainloop()