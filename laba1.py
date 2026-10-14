import tkinter as tk
from tkinter import colorchooser
import colorsys


class ColorApp:

    def __init__(self, window):
        self.window = window
        self.window.geometry("600x450")
        self.window.title("Лаба 1 цветовые пр-ва CMYK/RGB/HSV")

        self.change = False

        self.rgb = [tk.StringVar() for _ in range(3)]
        self.cmyk = [tk.StringVar() for _ in range(4)]
        self.hsv = [tk.StringVar() for _ in range(3)]

        self.make_window()

        self.set_color(0, 0, 0)


    def make_window(self):
        main = tk.Frame(self.window, padx=20, pady=20)
        main.pack()

        # левая часть
        left = tk.Frame(main)
        left.grid(row=0, column=0, padx=(0, 25))

        self.color = tk.Canvas(
            left,
            width=170,
            height=170,
            bg="black"
        )
        self.color.pack()

        self.hex = tk.Label(
            left,
            text="#000000",
            font=("Arial", 14)
        )
        self.hex.pack(pady=12)

        button = tk.Button(
            left,
            text="Выбрать цвет",
            command=self.pick_color,
            width=18
        )
        button.pack()


        # правая часть
        right = tk.Frame(main)
        right.grid(row=0, column=1)

        self.make_block(
            right,
            "RGB",
            ["R", "G", "B"],
            [255, 255, 255],
            self.rgb,
            self.rgb_change
        )

        self.make_block(
            right,
            "CMYK",
            ["C", "M", "Y", "K"],
            [100, 100, 100, 100],
            self.cmyk,
            self.cmyk_change
        )

        self.make_block(
            right,
            "HSV",
            ["H", "S", "V"],
            [360, 100, 100],
            self.hsv,
            self.hsv_change
        )


    def make_block(self, place, name, letters, maximum, variables, function):
        block = tk.LabelFrame(
            place,
            text=name,
            padx=8,
            pady=5
        )
        block.pack(fill="x", pady=5)

        for i in range(len(letters)):

            label = tk.Label(
                block,
                text=letters[i],
                width=2
            )
            label.grid(row=i, column=0, padx=5, pady=2)

            slider = tk.Scale(
                block,
                from_=0,
                to=maximum[i],
                orient="horizontal",
                variable=variables[i],
                showvalue=0,
                length=130
            )
            slider.grid(row=i, column=1, padx=5)

            entry = tk.Entry(
                block,
                textvariable=variables[i],
                width=5,
                justify="center"
            )
            entry.grid(row=i, column=2, padx=5)

            variables[i].trace_add("write", function)


    def rgb_to_cmyk(self, r, g, b):
        r = r / 255
        g = g / 255
        b = b / 255

        k = 1 - max(r, g, b)

        if k == 1:
            return 0, 0, 0, 100

        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)

        return round(c * 100), round(m * 100), round(y * 100), round(k * 100)


    def cmyk_to_rgb(self, c, m, y, k):
        c = c / 100
        m = m / 100
        y = y / 100
        k = k / 100

        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)

        return round(r), round(g), round(b)


    def rgb_to_hsv(self, r, g, b):
        r = r / 255
        g = g / 255
        b = b / 255

        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        return round(h * 360), round(s * 100), round(v * 100)


    def hsv_to_rgb(self, h, s, v):
        h = h / 360
        s = s / 100
        v = v / 100

        r, g, b = colorsys.hsv_to_rgb(h, s, v)

        return round(r * 255), round(g * 255), round(b * 255)


    def get_number(self, variable, maximum):
        try:
            number = int(variable.get())

            if number < 0:
                number = 0

            if number > maximum:
                number = maximum

            return number

        except:
            return 0


    def rgb_change(self, *args):
        if self.change:
            return

        r = self.get_number(self.rgb[0], 255)
        g = self.get_number(self.rgb[1], 255)
        b = self.get_number(self.rgb[2], 255)

        self.change = True

        color = "#{:02X}{:02X}{:02X}".format(r, g, b)

        self.color.config(bg=color)
        self.hex.config(text=color)

        self.rgb[0].set(r)
        self.rgb[1].set(g)
        self.rgb[2].set(b)

        c, m, y, k = self.rgb_to_cmyk(r, g, b)

        self.cmyk[0].set(c)
        self.cmyk[1].set(m)
        self.cmyk[2].set(y)
        self.cmyk[3].set(k)

        h, s, v = self.rgb_to_hsv(r, g, b)

        self.hsv[0].set(h)
        self.hsv[1].set(s)
        self.hsv[2].set(v)

        self.change = False


    def cmyk_change(self, *args):
        if self.change:
            return

        c = self.get_number(self.cmyk[0], 100)
        m = self.get_number(self.cmyk[1], 100)
        y = self.get_number(self.cmyk[2], 100)
        k = self.get_number(self.cmyk[3], 100)

        r, g, b = self.cmyk_to_rgb(c, m, y, k)

        self.change = True

        color = "#{:02X}{:02X}{:02X}".format(r, g, b)

        self.color.config(bg=color)
        self.hex.config(text=color)

        self.rgb[0].set(r)
        self.rgb[1].set(g)
        self.rgb[2].set(b)

        h, s, v = self.rgb_to_hsv(r, g, b)

        self.hsv[0].set(h)
        self.hsv[1].set(s)
        self.hsv[2].set(v)

        self.change = False


    def hsv_change(self, *args):
        if self.change:
            return

        h = self.get_number(self.hsv[0], 360)
        s = self.get_number(self.hsv[1], 100)
        v = self.get_number(self.hsv[2], 100)

        r, g, b = self.hsv_to_rgb(h, s, v)

        self.change = True

        color = "#{:02X}{:02X}{:02X}".format(r, g, b)

        self.color.config(bg=color)
        self.hex.config(text=color)

        self.rgb[0].set(r)
        self.rgb[1].set(g)
        self.rgb[2].set(b)

        c, m, y, k = self.rgb_to_cmyk(r, g, b)

        self.cmyk[0].set(c)
        self.cmyk[1].set(m)
        self.cmyk[2].set(y)
        self.cmyk[3].set(k)

        self.change = False


    def set_color(self, r, g, b):
        self.change = True

        color = "#{:02X}{:02X}{:02X}".format(r, g, b)

        self.color.config(bg=color)
        self.hex.config(text=color)

        self.rgb[0].set(r)
        self.rgb[1].set(g)
        self.rgb[2].set(b)

        c, m, y, k = self.rgb_to_cmyk(r, g, b)

        self.cmyk[0].set(c)
        self.cmyk[1].set(m)
        self.cmyk[2].set(y)
        self.cmyk[3].set(k)

        h, s, v = self.rgb_to_hsv(r, g, b)

        self.hsv[0].set(h)
        self.hsv[1].set(s)
        self.hsv[2].set(v)

        self.change = False


    def pick_color(self):
        result = colorchooser.askcolor()

        if result[0]:
            r = int(result[0][0])
            g = int(result[0][1])
            b = int(result[0][2])

            self.set_color(r, g, b)


window = tk.Tk()
app = ColorApp(window)

window.mainloop()