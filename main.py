import tkinter as tk
from tkinter import messagebox
import time
import random
import winsound

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
class ReactionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tester sprawności psychomotorycznej")
        self.root.geometry("800x600")
        
        self.training_mode = True
        self.training_trials = 2
        self.test_trials = 5
        self.current_trial = 0
        self.current_test_type = None
        self.test_results = {
            "visual": [],
            "audio": [],
            "color": []
        }

        self.main_menu()

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Wybierz test", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="🟥 Szybka reakcja - kliknięcie", command=lambda: self.start_test_with_instruction("visual"), width=30, height=2).pack(pady=5)
        tk.Button(self.root, text="🔊 Szybka reakcja - dźwięk", command=lambda: self.start_test_with_instruction("audio"), width=30, height=2).pack(pady=5)
        tk.Button(self.root, text="🎨 Wybór koloru", command=lambda: self.start_test_with_instruction("color"), width=30, height=2).pack(pady=5)
        tk.Button(self.root, text="📊 Pokaż wyniki", command=self.show_summary, width=30, height=2).pack(pady=20)

    def start_test_with_instruction(self, test_type):
        self.current_test_type = test_type
        self.training_mode = True
        self.current_trial = 0

        for widget in self.root.winfo_children():
            widget.destroy()

        descriptions = {
            "visual": "Reaguj jak najszybciej, gdy kolor zmieni się na zielony.",
            "audio": "Reaguj jak najszybciej, gdy usłyszysz dźwięk.",
            "color": "Kliknij właściwy kolor, gdy pojawi się na ekranie."
        }

        tk.Label(self.root, text=f"INSTRUKCJA ({test_type.upper()})", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=descriptions[test_type], wraplength=350, justify="center").pack(pady=10)
        tk.Label(self.root, text="Najpierw faza szkoleniowa (bez oceny wyników)", fg="blue").pack(pady=10)
        tk.Button(self.root, text="Rozpocznij", command=self.run_test_step).pack(pady=10)

    def run_test_step(self):
        if self.current_trial == (self.training_trials + self.test_trials):
            self.main_menu()
            return

        if self.current_trial == self.training_trials:
            self.training_mode = False
            messagebox.showinfo("Test właściwy", "Zaczynamy test właściwy – wyniki będą zapisywane.")

        if self.current_test_type == "visual":
            self.visual_test()
        elif self.current_test_type == "audio":
            self.audio_test()
        elif self.current_test_type == "color":
            self.color_test()

    def visual_test(self):
        self.prepare_test_ui("Kliknij, gdy kolor się zmieni")
        delay = random.uniform(2, 5)
        self.root.after(int(delay * 1000), self.start_visual_test)

    def start_visual_test(self):
        self.start_time = time.perf_counter()
        self.label.config(text="KLIKNIJ TERAZ!", fg="green")
        self.test_button.config(text="Kliknij!", command=self.register_click, state="normal")

    def audio_test(self):
        self.prepare_test_ui("Kliknij, gdy usłyszysz dźwięk")
        delay = random.uniform(2, 5)
        self.root.after(int(delay * 1000), self.start_audio_test)

    def start_audio_test(self):
        self.start_time = time.perf_counter()
        winsound.Beep(1000, 300)
        self.label.config(text="KLIKNIJ TERAZ!", fg="blue")
        self.test_button.config(text="Kliknij!", command=self.register_click, state="normal")

    def color_test(self):
        self.prepare_test_ui("Kliknij poprawny kolor, gdy się pojawi")

        self.correct_color = random.choice(["Czerwony", "Zielony"])
        delay = random.uniform(2, 5)
        self.root.after(int(delay * 1000), self.start_color_test)

    def start_color_test(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Kliknij kolor: {self.correct_color}", font=("Arial", 16)).pack(pady=10)
        self.start_time = time.perf_counter()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Czerwony", bg="red", fg="white", width=15, height=2,
                  command=lambda: self.register_color("Czerwony")).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Zielony", bg="green", fg="white", width=15, height=2,
                  command=lambda: self.register_color("Zielony")).pack(side=tk.LEFT, padx=10)

    def register_click(self):
        reaction_time = time.perf_counter() - self.start_time
        if not self.training_mode:
            self.test_results[self.current_test_type].append(reaction_time)
        self.label.config(text=f"Czas reakcji: {reaction_time:.8f} s", fg="black")
        self.test_button.config(text="Dalej", command=self.next_trial)

    def register_color(self, selected):
        reaction_time = time.perf_counter() - self.start_time
        correct = selected == self.correct_color
        if not self.training_mode:
            if correct:
                self.test_results["color"].append(reaction_time)
            else:
                self.test_results["color"].append(None)  # błąd = brak czasu
        message = f"Czas reakcji: {reaction_time:.8f} s\n{'Poprawnie!' if correct else 'Błąd!'}"
        messagebox.showinfo("Wynik", message)
        self.next_trial()

    def next_trial(self):
        self.current_trial += 1
        self.run_test_step()

    def prepare_test_ui(self, instruction):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.label = tk.Label(self.root, text=instruction, font=("Arial", 16))
        self.label.pack(pady=20)
        self.test_button = tk.Button(self.root, text="Czekaj na sygnał...", state="disabled")
        self.test_button.pack(pady=10)

    def show_summary(self):
        for test_name, results in self.test_results.items():
            clean_results = [r for r in results if r is not None]
            if clean_results:
                plt.plot(clean_results, marker='o', label=test_name)

        plt.title("Czasy reakcji")
        plt.xlabel("Numer próby")
        plt.ylabel("Czas reakcji (s)")
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReactionApp(root)
    root.mainloop()
