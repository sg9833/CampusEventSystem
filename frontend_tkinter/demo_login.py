import tkinter as tk
from frontend_tkinter.widgets.modern_entry import ModernEntry
from frontend_tkinter.widgets.modern_button import ModernButton
from frontend_tkinter.styles.theme import ThemeManager


def main():
    tm = ThemeManager()
    root = tk.Tk()
    root.title('Demo Login')
    root.geometry('480x360')
    root.configure(bg=tm.colors()['bg_secondary'])

    frame = tk.Frame(root, bg=tm.colors()['bg_secondary'])
    frame.pack(expand=True)

    tk.Label(frame, text='Welcome', font=tm.fonts()['h2'], bg=tm.colors()['bg_secondary'], fg=tm.colors()['text_primary']).pack(pady=10)

    username = ModernEntry(frame, placeholder='Username')
    username.pack(pady=8)

    password = ModernEntry(frame, placeholder='Password', is_password=True)
    password.pack(pady=8)

    def do_login():
        print('login:', username.get(), password.get())

    ModernButton(frame, text='Login', command=do_login, style='primary').pack(pady=12)

    root.mainloop()


if __name__ == '__main__':
    main()
