import tkinter as tk
import time
from frontend_tkinter.widgets.modern_button import ModernButton
from frontend_tkinter.styles.theme import ThemeManager


def on_click(name):
    print(f"{name} clicked")


def main():
    root = tk.Tk()
    root.title('ModernButton Test')
    root.geometry('480x320')

    tm = ThemeManager()

    frame = tk.Frame(root, bg=tm.colors()['bg_secondary'])
    frame.pack(fill='both', expand=True, padx=20, pady=20)

    btn1 = ModernButton(frame, text='Primary', style='primary', command=lambda: on_click('Primary'))
    btn1.pack(pady=10)

    btn2 = ModernButton(frame, text='Success', style='success', command=lambda: on_click('Success'))
    btn2.pack(pady=10)

    btn3 = ModernButton(frame, text='Danger', style='danger', command=lambda: on_click('Danger'))
    btn3.pack(pady=10)

    root.mainloop()


if __name__ == '__main__':
    main()
