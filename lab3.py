import math
import os
import random
import string
import tkinter as tk
from tkinter import messagebox
import pygame


class ValorantKeygen:
    def __init__(self, root):
        self.root = root
        self.root.title("VALORANT Key Generator")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#0f1923')

        pygame.mixer.init()

        self.chars = string.ascii_uppercase + string.digits

        self.animation_running = True
        self.pulse_phase = 0
        self.title_glow_phase = 0
        self.particles = []

        self.setup_background()
        self.setup_music()
        self.create_widgets()
        self.animate()

    def setup_background(self):
        self.canvas = tk.Canvas(
            self.root,
            width=800,                        # холст для анимированного фона и элементов
            height=600,
            bg='#0f1923',
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.create_gradient_background()  # град фон
        self.create_particles(50)  # анимка

    def create_gradient_background(self):
        for y in range(0, 600, 2):
            r = int(15 + (y / 600) * 5)
            g = int(25 + (y / 600) * 10)
            b = int(35 + (y / 600) * 15)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, y, 800, y, fill=color, width=2)

    def create_particles(self, count):
        for _ in range(count):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.randint(1, 3)
            speed = random.uniform(0.5, 2)
            direction = random.uniform(0, 2 * math.pi)
            color = random.choice(['#ff4655', '#0f1923', '#ece8e1', '#768079'])
            self.particles.append({
                'x': x,
                'y': y,
                'size': size,
                'speed': speed,
                'direction': direction,
                'color': color,
                'id': None
            })

    def setup_music(self):
        music_file = '2019-12-11_-_Retro_Platforming_-_David_Fesliyan.mp3'

        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
            print("Музыка успешно загружена и воспроизводится")
        else:
            print(f"Файл {music_file} не найден")

    def create_widgets(self):
        self.title_label = tk.Label(
            self.canvas,
            text="VALORANT",
            font=("Arial", 36, "bold"),
            fg="#ff4655",
            bg='#0f1923'
        )
        self.canvas.create_window(400, 80, window=self.title_label)

        subtitle_label = tk.Label(
            self.canvas,
            text="KEY GENERATOR",
            font=("Arial", 18),
            fg="#ece8e1",
            bg='#0f1923'
        )
        self.canvas.create_window(400, 130, window=subtitle_label)

        dec_frame = tk.Frame(self.canvas, bg='#0f1923')
        self.canvas.create_window(400, 200, window=dec_frame)

        dec_label = tk.Label(
            dec_frame,
            text="Введите DEC-число (3 цифры):",
            font=("Arial", 12),
            fg="#ece8e1",
            bg='#0f1923'
        )
        dec_label.pack()

        self.dec_entry = tk.Entry(
            dec_frame,
            font=("Arial", 14),
            width=10,
            justify='center',
            validate="key",
            validatecommand=(self.root.register(self.validate_dec), '%P')
        )
        self.dec_entry.pack(pady=10)

        self.generate_btn = tk.Button(
            self.canvas,
            text="СГЕНЕРИРОВАТЬ КЛЮЧ",
            font=("Arial", 14, "bold"),
            fg="#0f1923",
            bg="#ff4655",
            activeforeground="#0f1923",
            activebackground="#ff4655",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.generate_key
        )
        self.canvas.create_window(400, 280, window=self.generate_btn)

        key_frame = tk.Frame(self.canvas, bg='#0f1923')
        self.canvas.create_window(400, 350, window=key_frame)

        key_label = tk.Label(
            key_frame,
            text="Сгенерированный ключ:",
            font=("Arial", 12),
            fg="#ece8e1",
            bg='#0f1923'
        )
        key_label.pack()

        self.key_var = tk.StringVar()
        self.key_var.set("XXXXX-XXXX-XXX-XX")

        self.key_display = tk.Entry(
            key_frame,
            textvariable=self.key_var,
            font=("Courier", 16, "bold"),
            fg="#ff4655",
            bg="#1a2332",
            width=25,
            justify='center',
            state='readonly',
            readonlybackground="#1a2332"
        )
        self.key_display.pack(pady=10)

        self.copy_btn = tk.Button(
            self.canvas,
            text="КОПИРОВАТЬ КЛЮЧ",
            font=("Arial", 10),
            fg="#0f1923",
            bg="#ece8e1",
            activeforeground="#0f1923",
            activebackground="#ece8e1",
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.copy_key
        )
        self.canvas.create_window(400, 420, window=self.copy_btn)

        self.pulse_circle = self.canvas.create_oval(
            700, 50, 750, 100, fill="#ff4655", outline=""
        )

    def validate_dec(self, value):
        if value == "":
            return True
        if len(value) <= 3 and value.isdigit():
            return True
        return False

    def shift_char(self, char, shift, direction):  # сдвиг символов
        idx = self.chars.index(char)
        if direction == 'right':
            new_idx = (idx + shift) % len(self.chars)
        else:  # left
            new_idx = (idx - shift) % len(self.chars)
        return self.chars[new_idx]

    def generate_key(self):
        dec_str = self.dec_entry.get()

        if len(dec_str) != 3:
            messagebox.showerror("Ошибка", "Введите ровно 3 цифры!")
            return

        self.animate_generation()
        self.root.after(1000, self.finish_generation, dec_str)

    def animate_generation(self):
        self.key_var.set("ГЕНЕРАЦИЯ...")
        self.key_display.config(fg="#ece8e1")

        for i in range(3):
            self.root.after(i * 200, lambda: self.key_display.config(
                fg="#ff4655" if i % 2 == 0 else "#ece8e1"
            ))

    def finish_generation(self, dec_str):
        block1 = ''.join(random.choices(self.chars, k=5))

        shifts = [int(d) for d in dec_str]

        block2_base = block1[:-1]
        block2 = ''.join(
            self.shift_char(c, shifts[0], 'right') for c in block2_base
        )

        block3_base = block2[:-1]
        block3 = ''.join(
            self.shift_char(c, shifts[1], 'left') for c in block3_base
        )

        block4_base = block3[:-1]
        block4 = ''.join(
            self.shift_char(c, shifts[2], 'right') for c in block4_base
        )

        key = f"{block1}-{block2}-{block3}-{block4}"
        self.key_var.set(key)
        self.key_display.config(fg="#ff4655")

        self.animate_success()

    def animate_success(self):
        for i in range(5):
            self.root.after(i * 100, lambda: self.key_display.config(
                bg="#2a3a4a" if i % 2 == 0 else "#1a2332"
            ))

    def copy_key(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.key_var.get())

        original_text = self.copy_btn.cget("text")
        self.copy_btn.config(text="СКОПИРОВАНО!")
        self.root.after(1000, lambda: self.copy_btn.config(text=original_text))

        messagebox.showinfo("Успех", "Ключ скопирован в буфер обмена!")

    def animate(self):
        if not self.animation_running:
            return

        self.pulse_phase = (self.pulse_phase + 0.05) % (2 * math.pi)
        pulse_intensity = 0.7 + 0.3 * math.sin(self.pulse_phase)
        r = int(255 * pulse_intensity)
        g = int(70 * pulse_intensity)
        b = int(85 * pulse_intensity)
        pulse_color = f'#{r:02x}{g:02x}{b:02x}'
        self.generate_btn.config(bg=pulse_color)

        self.title_glow_phase = (self.title_glow_phase + 0.03) % (2 * math.pi)
        glow_intensity = 0.8 + 0.2 * math.sin(self.title_glow_phase)
        r = int(255 * glow_intensity)
        g = int(70 * glow_intensity)
        b = int(85 * glow_intensity)
        glow_color = f'#{r:02x}{g:02x}{b:02x}'
        self.title_label.config(fg=glow_color)

        pulse_size = 5 + 3 * math.sin(self.pulse_phase)
        self.canvas.coords(
            self.pulse_circle,
            700 - pulse_size,
            50 - pulse_size,
            750 + pulse_size,
            100 + pulse_size
        )

        self.animate_particles()
        self.root.after(50, self.animate)

    def animate_particles(self):
        for particle in self.particles:
            if particle['id']:
                self.canvas.delete(particle['id'])

            particle['x'] += particle['speed'] * math.cos(particle['direction'])
            particle['y'] += particle['speed'] * math.sin(particle['direction'])

            if particle['x'] < 0:
                particle['x'] = 800
            elif particle['x'] > 800:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = 600
            elif particle['y'] > 600:
                particle['y'] = 0

            x1 = particle['x'] - particle['size']
            y1 = particle['y'] - particle['size']
            x2 = particle['x'] + particle['size']
            y2 = particle['y'] + particle['size']
            particle['id'] = self.canvas.create_oval(
                x1, y1, x2, y2, fill=particle['color'], outline=""
            )

    def on_closing(self):
        self.animation_running = False
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ValorantKeygen(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()