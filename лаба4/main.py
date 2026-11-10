import tkinter as tk
from tkinter import ttk
import math


class WireframeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3D-визуализатор каркасных моделей")
        self.root.geometry("1100x750")

        # Панель управления (Верхняя)
        control_frame = ttk.Frame(root, padding=12)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        for col in (1, 3, 5):
            control_frame.columnconfigure(col, weight=1, uniform="ctrl_cols")

        # Ряд 1 Фигура, Проекция, Масштаб
        ttk.Label(control_frame, text="Фигура:").grid(row=0, column=0, padx=(5, 2), pady=6, sticky=tk.W)
        self.shape_var = tk.StringVar(value="Куб")
        shapes = ["Куб", "Пирамида", "Октаэдр", "Треугольная призма"]
        self.shape_combo = ttk.Combobox(control_frame, textvariable=self.shape_var, values=shapes, state="readonly")
        self.shape_combo.grid(row=0, column=1, padx=(0, 15), pady=6, sticky="ew")
        self.shape_combo.bind("<<ComboboxSelected>>", lambda e: self.draw())

        ttk.Label(control_frame, text="Проекция:").grid(row=0, column=2, padx=(5, 2), pady=6, sticky=tk.W)
        self.proj_var = tk.StringVar(value="Перспективная")
        projections = ["Перспективная", "Ортографическая"]
        self.proj_combo = ttk.Combobox(control_frame, textvariable=self.proj_var, values=projections, state="readonly")
        self.proj_combo.grid(row=0, column=3, padx=(0, 15), pady=6, sticky="ew")
        self.proj_combo.bind("<<ComboboxSelected>>", lambda e: self.draw())

        ttk.Label(control_frame, text="Масштаб:").grid(row=0, column=4, padx=(5, 2), pady=6, sticky=tk.W)
        self.scale_var = tk.IntVar(value=150)
        self.scale_slider = ttk.Scale(control_frame, from_=50, to=300, variable=self.scale_var, command=lambda e: self.draw())
        self.scale_slider.grid(row=0, column=5, padx=0, pady=6, sticky="ew")

        # Ряд 2 Поворот X, Поворот Y, Поворот Z
        ttk.Label(control_frame, text="Поворот X:").grid(row=1, column=0, padx=(5, 2), pady=6, sticky=tk.W)
        self.rot_x = tk.IntVar(value=30)
        self.rot_x_slider = ttk.Scale(control_frame, from_=0, to=360, variable=self.rot_x, command=lambda e: self.draw())
        self.rot_x_slider.grid(row=1, column=1, padx=(0, 15), pady=6, sticky="ew")

        ttk.Label(control_frame, text="Поворот Y:").grid(row=1, column=2, padx=(5, 2), pady=6, sticky=tk.W)
        self.rot_y = tk.IntVar(value=45)
        self.rot_y_slider = ttk.Scale(control_frame, from_=0, to=360, variable=self.rot_y, command=lambda e: self.draw())
        self.rot_y_slider.grid(row=1, column=3, padx=(0, 15), pady=6, sticky="ew")

        ttk.Label(control_frame, text="Поворот Z:").grid(row=1, column=4, padx=(5, 2), pady=6, sticky=tk.W)
        self.rot_z = tk.IntVar(value=0)
        self.rot_z_slider = ttk.Scale(control_frame, from_=0, to=360, variable=self.rot_z, command=lambda e: self.draw())
        self.rot_z_slider.grid(row=1, column=5, padx=0, pady=6, sticky="ew")

        # Холст отрисовки
        self.canvas = tk.Canvas(root, bg="#1E1E1E")
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.canvas.bind("<Configure>", lambda e: self.draw())

    # 3D Модели (Вершины и Рёбра)
    def get_mesh(self, name):
        if name == "Куб":
            vertices = [
                [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
                [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]
            ]
            edges = [
                (0, 1), (1, 2), (2, 3), (3, 0),
                (4, 5), (5, 6), (6, 7), (7, 4),
                (0, 4), (1, 5), (2, 6), (3, 7)
            ]
        elif name == "Пирамида":
            vertices = [
                [-1, -1, -1], [1, -1, -1], [1, -1, 1], [-1, -1, 1],
                [0, 1.2, 0]
            ]
            edges = [
                (0, 1), (1, 2), (2, 3), (3, 0),
                (0, 4), (1, 4), (2, 4), (3, 4)
            ]
        elif name == "Октаэдр":
            vertices = [
                [1, 0, 0], [-1, 0, 0], [0, 1, 0],
                [0, -1, 0], [0, 0, 1], [0, 0, -1]
            ]
            edges = [
                (0, 2), (2, 1), (1, 3), (3, 0),
                (0, 4), (2, 4), (1, 4), (3, 4),
                (0, 5), (2, 5), (1, 5), (3, 5)
            ]
        else:  # Треугольная призма
            vertices = [
                [-1, -1, -1], [1, -1, -1], [0, 1, -1],
                [-1, -1,  1], [1, -1,  1], [0, 1,  1]
            ]
            edges = [
                (0, 1), (1, 2), (2, 0),
                (3, 4), (4, 5), (5, 3),
                (0, 3), (1, 4), (2, 5)
            ]
        return vertices, edges

    # Преобразования и Проекция
    def transform_and_project(self, vx, vy, vz, ax, ay, az, scale, proj_type, cw, ch):
        # 1. Поворот вокруг X
        rad_x = math.radians(ax)
        y1 = vy * math.cos(rad_x) - vz * math.sin(rad_x)
        z1 = vy * math.sin(rad_x) + vz * math.cos(rad_x)
        x1 = vx

        # 2. Поворот вокруг Y
        rad_y = math.radians(ay)
        x2 = x1 * math.cos(rad_y) + z1 * math.sin(rad_y)
        z2 = -x1 * math.sin(rad_y) + z1 * math.cos(rad_y)
        y2 = y1

        # 3. Поворот вокруг Z
        rad_z = math.radians(az)
        x3 = x2 * math.cos(rad_z) - y2 * math.sin(rad_z)
        y3 = x2 * math.sin(rad_z) + y2 * math.cos(rad_z)
        z3 = z2

        # 4. Проекция на 2D экран
        ox = cw / 2
        oy = ch / 2

        if proj_type == "Перспективная":
            distance = 3.5
            factor = distance / (distance + z3)
            sx = x3 * factor * scale + ox
            sy = -y3 * factor * scale + oy
        else:  # Ортографическая
            sx = x3 * scale + ox
            sy = -y3 * scale + oy

        return sx, sy

    # Отрисовка
    def draw(self):
        self.canvas.delete("all")
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw <= 1 or ch <= 1:
            return

        vertices, edges = self.get_mesh(self.shape_var.get())
        ax = self.rot_x.get()
        ay = self.rot_y.get()
        az = self.rot_z.get()
        scale = self.scale_var.get()
        proj_type = self.proj_var.get()

        projected = []
        for v in vertices:
            pt_2d = self.transform_and_project(v[0], v[1], v[2], ax, ay, az, scale, proj_type, cw, ch)
            projected.append(pt_2d)

        # Отрисовка ребер
        for e in edges:
            x1, y1 = projected[e[0]]
            x2, y2 = projected[e[1]]
            self.canvas.create_line(x1, y1, x2, y2, fill="#00FFCC", width=2)

        # Отрисовка вершин
        for x, y in projected:
            r = 4
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="#FF4081", outline="white")


if __name__ == "__main__":
    root = tk.Tk()
    app = WireframeApp(root)
    root.mainloop()