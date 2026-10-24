import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import numpy as np


class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №2 (Вариант 6)")
        self.root.geometry("950x680")

        self.img_orig = None
        self.img_proc = None

        # Панель управления
        control_frame = tk.Frame(root, padx=10, pady=5)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Ряд 1 поэлементные операции
        row1 = tk.Frame(control_frame)
        row1.pack(fill=tk.X, pady=2)

        tk.Button(row1, text="Открыть фото", command=self.load_image, bg="#d0e0f0").pack(side=tk.LEFT, padx=5)
        tk.Button(row1, text="Негатив (Инверсия)", command=self.apply_negative).pack(side=tk.LEFT, padx=5)
        tk.Button(row1, text="Гамма-коррекция", command=self.apply_gamma).pack(side=tk.LEFT, padx=5)

        tk.Label(row1, text="γ:").pack(side=tk.LEFT, padx=(5, 2))
        self.gamma_scale = tk.Scale(row1, from_=0.2, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, length=100)
        self.gamma_scale.set(1.5)
        self.gamma_scale.pack(side=tk.LEFT)

        # Ряд 2 контрастирование и пороги
        row2 = tk.Frame(control_frame)
        row2.pack(fill=tk.X, pady=4)

        tk.Button(row2, text="Линейное контрастирование", command=self.apply_contrast).pack(side=tk.LEFT, padx=5)
        tk.Button(row2, text="Порог: Итеративный", command=self.apply_iterative).pack(side=tk.LEFT, padx=5)
        tk.Button(row2, text="Порог: Оцу", command=self.apply_otsu).pack(side=tk.LEFT, padx=5)

        # Информационная плашка
        self.info_label = tk.Label(root, text="Загрузите изображение для начала работы", font=("Arial", 11, "bold"))
        self.info_label.pack(side=tk.TOP, pady=5)

        # Область отображения картинок и гистограмм
        main_display = tk.Frame(root)
        main_display.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        # Левый блок (Оригинал + Гистограмма)
        left_block = tk.Frame(main_display, bd=1, relief=tk.SOLID)
        left_block.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

        tk.Label(left_block, text="ОРИГИНАЛ", font=("Arial", 10, "bold")).pack(pady=2)
        self.lbl_orig = tk.Label(left_block, text="Нет фото", bg="#e0e0e0")
        self.lbl_orig.pack(expand=True, fill=tk.BOTH, padx=5, pady=2)

        tk.Label(left_block, text="Гистограмма оригинала:", font=("Arial", 9)).pack(pady=(5, 0))
        self.lbl_hist_orig = tk.Label(left_block, bg="#f5f5f5")
        self.lbl_hist_orig.pack(pady=5)

        # Правый блок (Результат + Гистограмма)
        right_block = tk.Frame(main_display, bd=1, relief=tk.SOLID)
        right_block.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)

        tk.Label(right_block, text="РЕЗУЛЬТАТ", font=("Arial", 10, "bold")).pack(pady=2)
        self.lbl_proc = tk.Label(right_block, text="Нет результата", bg="#e0e0e0")
        self.lbl_proc.pack(expand=True, fill=tk.BOTH, padx=5, pady=2)

        tk.Label(right_block, text="Гистограмма результата:", font=("Arial", 9)).pack(pady=(5, 0))
        self.lbl_hist_proc = tk.Label(right_block, bg="#f5f5f5")
        self.lbl_hist_proc.pack(pady=5)

    def make_histogram_image(self, pil_img, width=260, height=100):
        """Отрисовка гистограммы с отступами от краев"""
        arr = np.array(pil_img)
        hist, _ = np.histogram(arr, bins=256, range=(0, 256))
        max_val = hist.max()

        hist_img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(hist_img)

        # Рисуем внешнюю рамку
        draw.rectangle([(0, 0), (width - 1, height - 1)], outline=(180, 180, 180))

        if max_val > 0:
            margin = 5  # Отступ в пикселях от внешней рамки
            draw_w = width - 2 * margin
            for x in range(256):
                h = int((hist[x] / max_val) * (height - 8))
                if h > 0:
                    x_pos = margin + int((x / 255.0) * draw_w)
                    draw.line([(x_pos, height - 2), (x_pos, height - 2 - h)], fill=(40, 40, 40), width=2)

        return hist_img

    def show_images(self):
        """Обновление изображений и их гистограмм"""
        if self.img_orig:
            preview_orig = self.img_orig.resize((320, 320))
            self.tk_orig = ImageTk.PhotoImage(preview_orig)
            self.lbl_orig.config(image=self.tk_orig, text="")

            hist_orig = self.make_histogram_image(self.img_orig)
            self.tk_hist_orig = ImageTk.PhotoImage(hist_orig)
            self.lbl_hist_orig.config(image=self.tk_hist_orig)

        if self.img_proc:
            preview_proc = self.img_proc.resize((320, 320))
            self.tk_proc = ImageTk.PhotoImage(preview_proc)
            self.lbl_proc.config(image=self.tk_proc, text="")

            hist_proc = self.make_histogram_image(self.img_proc)
            self.tk_hist_proc = ImageTk.PhotoImage(hist_proc)
            self.lbl_hist_proc.config(image=self.tk_hist_proc)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.img_orig = Image.open(file_path).convert("L")
            self.img_proc = self.img_orig.copy()
            self.show_images()
            self.info_label.config(text=f"Файл загружен: {self.img_orig.width}x{self.img_orig.height} px")

    # 1. Поэлементные операции
    def apply_negative(self):
        if not self.img_orig: return
        arr = np.array(self.img_orig, dtype=np.uint8)
        res = 255 - arr
        self.img_proc = Image.fromarray(res)
        self.show_images()
        self.info_label.config(text="Инверсия (Негатив): s = 255 - r")

    def apply_gamma(self):
        if not self.img_orig: return
        gamma = self.gamma_scale.get()
        arr = np.array(self.img_orig, dtype=np.float32) / 255.0
        res = (arr ** gamma) * 255.0
        res = np.clip(res, 0, 255).astype(np.uint8)
        self.img_proc = Image.fromarray(res)
        self.show_images()
        self.info_label.config(text=f"Гамма-коррекция (γ = {gamma})")

    # 2. Линейное контрастирование
    def apply_contrast(self):
        if not self.img_orig: return
        arr = np.array(self.img_orig, dtype=np.float32)
        f_min, f_max = arr.min(), arr.max()

        if f_max > f_min:
            res = ((arr - f_min) / (f_max - f_min)) * 255.0
        else:
            res = arr

        res = np.clip(res, 0, 255).astype(np.uint8)
        self.img_proc = Image.fromarray(res)
        self.show_images()
        self.info_label.config(text=f"Линейное контрастирование: f_min={int(f_min)}, f_max={int(f_max)}")

    # 3. Глобальная пороговая обработка
    def apply_iterative(self):
        if not self.img_orig: return
        arr = np.array(self.img_orig, dtype=np.float32)
        T = arr.mean()

        while True:
            g1 = arr[arr > T]
            g2 = arr[arr <= T]
            m1 = g1.mean() if len(g1) > 0 else 0
            m2 = g2.mean() if len(g2) > 0 else 0
            new_T = (m1 + m2) / 2.0
            if abs(new_T - T) < 0.5:
                break
            T = new_T

        T = int(T)
        res = np.where(arr >= T, 255, 0).astype(np.uint8)
        self.img_proc = Image.fromarray(res)
        self.show_images()
        self.info_label.config(text=f"Итеративный метод (IsoData): Порог T = {T}")

    def apply_otsu(self):
        if not self.img_orig: return
        arr = np.array(self.img_orig, dtype=np.uint8)
        hist, _ = np.histogram(arr, bins=256, range=(0, 256))
        total_pixels = arr.size

        best_T = 0
        max_variance = -1.0

        for T in range(256):
            w0 = hist[:T].sum() / total_pixels
            w1 = hist[T:].sum() / total_pixels
            if w0 == 0 or w1 == 0: continue

            m0 = np.sum(np.arange(T) * hist[:T]) / (w0 * total_pixels)
            m1 = np.sum(np.arange(T, 256) * hist[T:]) / (w1 * total_pixels)
            variance = w0 * w1 * ((m0 - m1) ** 2)

            if variance > max_variance:
                max_variance = variance
                best_T = T

        res = np.where(arr >= best_T, 255, 0).astype(np.uint8)
        self.img_proc = Image.fromarray(res)
        self.show_images()
        self.info_label.config(text=f"Метод Оцу: Порог T = {best_T}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()