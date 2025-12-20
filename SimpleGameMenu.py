import tkinter as tk
from tkinter import messagebox, ttk
import random
class GameMenu:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Моя Игра - Меню")
        self.window.geometry("800*600")
        self.window.resizable(False, False)
        self.coins = 1500
        self.gems = 50
        self.create_interface()

    def create_interface(self):
        self.bg_label = tk.Label(self.window, bg="#1E3A5F", fg="white")
        self.bg_label.pack(fill="both", expand=True)
        self.title_



