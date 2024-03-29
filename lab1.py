import tkinter as tk

class LineEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Графический редактор")

        self.canvas_width = 600
        self.canvas_height = 400
        self.debug_mode = False

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side=tk.LEFT)

        self.toolbar = tk.Frame(self.master)
        self.toolbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.debug_var = tk.BooleanVar()
        self.debug_checkbox = tk.Checkbutton(self.toolbar, text="Отладочный режим", variable=self.debug_var, command=self.toggle_debug_mode)
        self.debug_checkbox.pack()

        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("ЦДА")
        self.algorithm_menu = tk.OptionMenu(self.toolbar, self.algorithm_var, "ЦДА", "Брезенхем", "Ву")
        self.algorithm_menu.pack()

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        self.debug_text = tk.Text(self.master, height=20, width=40)
        self.debug_text.pack(side=tk.RIGHT)

        self.debug_text.insert(tk.END, "Для отладки\n")

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def toggle_debug_mode(self):
        self.debug_mode = self.debug_var.get()

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def draw(self, event):
        self.canvas.delete("line")
        self.end_x = event.x
        self.end_y = event.y
        self.draw_line(self.start_x, self.start_y, self.end_x, self.end_y)

    def end_draw(self, event):
        if self.debug_mode:
            self.debug_text.delete(1.0, tk.END)
            if self.algorithm_var.get() == "ЦДА":
                self.debug_text.insert(tk.END, "ЦДА:\n")
                self.draw_dda(self.start_x, self.start_y, self.end_x, self.end_y)
            elif self.algorithm_var.get() == "Брезенхем":
                self.debug_text.insert(tk.END, "Брезенхем:\n")
                self.draw_bresenham(self.start_x, self.start_y, self.end_x, self.end_y)
            elif self.algorithm_var.get() == "Ву":
                self.debug_text.insert(tk.END, "Ву:\n")
                self.draw_wu(self.start_x, self.start_y, self.end_x, self.end_y)

    def draw_line(self, x0, y0, x1, y1):
        self.canvas.create_line(x0, y0, x1, y1, tags="line")

    def draw_dda(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy))
        x_increment = dx / steps
        y_increment = dy / steps
        x = x0
        y = y0
        for _ in range(steps):
            self.canvas.create_rectangle(round(x), round(y), round(x), round(y), fill="black")
            x += x_increment
            y += y_increment
            self.debug_text.insert(tk.END, f"({round(x)}, {round(y)})\n")
            self.debug_text.see(tk.END)
            self.master.update()  
            self.master.after(50) 

    def draw_bresenham(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while x0 != x1 or y0 != y1:
            self.canvas.create_rectangle(x0, y0, x0, y0, fill="black")
            self.debug_text.insert(tk.END, f"({x0}, {y0})\n")
            self.debug_text.see(tk.END)
            self.master.update() 
            self.master.after(50)  
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def draw_wu(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        if dx > dy:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            gradient = dy / dx
            xend = round(x0)
            yend = y0 + gradient * (xend - x0)
            xgap = 1 - (x0 + 0.5) % 1
            xpxl1 = xend
            ypxl1 = int(yend)
            self.canvas.create_rectangle(xpxl1, ypxl1, xpxl1, ypxl1, fill="black", width=1)
            self.canvas.create_rectangle(xpxl1, ypxl1 + 1, xpxl1, ypxl1 + 1, fill="black", width=1)
            intery = yend + gradient

            xend = round(x1)
            yend = y1 + gradient * (xend - x1)
            xgap = (x0 + 0.5) % 1
            xpxl2 = xend
            ypxl2 = int(yend)
            self.canvas.create_rectangle(xpxl2, ypxl2, xpxl2, ypxl2, fill="black", width=1)
            self.canvas.create_rectangle(xpxl2, ypxl2 + 1, xpxl2, ypxl2 + 1, fill="black", width=1)

            for x in range(int(xpxl1 + 1), int(xpxl2)):
                self.canvas.create_rectangle(x, int(intery), x, int(intery), fill="black", width=1)
                self.canvas.create_rectangle(x, int(intery) + 1, x, int(intery) + 1, fill="black", width=1)
                self.canvas.create_rectangle(x, int(intery) + 1, x, int(intery) + 1, fill="black", width=1)
                intery += gradient
                self.debug_text.insert(tk.END, f"({x}, {int(intery)})\n")
                self.debug_text.see(tk.END) 
                self.master.update()  
                self.master.after(50) 
        else:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            gradient = dx / dy
            yend = round(y0)
            xend = x0 + gradient * (yend - y0)
            ygap = 1 - (y0 + 0.5) % 1
            ypxl1 = yend
            xpxl1 = int(xend)
            self.canvas.create_rectangle(xpxl1, ypxl1, xpxl1, ypxl1, fill="black", width=1)
            self.canvas.create_rectangle(xpxl1, ypxl1 + 1, xpxl1, ypxl1 + 1, fill="black", width=1)
            interx = xend + gradient

            yend = round(y1)
            xend = x1 + gradient * (yend - y1)
            ygap = (y0 + 0.5) % 1
            ypxl2 = yend
            xpxl2 = int(xend)
            self.canvas.create_rectangle(xpxl2, ypxl2, xpxl2, ypxl2, fill="black", width=1)
            self.canvas.create_rectangle(xpxl2, ypxl2 + 1, xpxl2, ypxl2 + 1, fill="black", width=1)

            for y in range(int(ypxl1 + 1), int(ypxl2)):
                self.canvas.create_rectangle(int(interx), y, int(interx), y, fill="black", width=1)
                self.canvas.create_rectangle(int(interx) + 1, y, int(interx) + 1, y, fill="black", width=1)
                self.canvas.create_rectangle(int(interx) + 1, y, int(interx) + 1, y, fill="black", width=1)
                interx += gradient
                self.debug_text.insert(tk.END, f"({int(interx)}, {y})\n")
                self.debug_text.see(tk.END) 
                self.master.update()
                self.master.after(50)  

def main():
    root = tk.Tk()
    app = LineEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
