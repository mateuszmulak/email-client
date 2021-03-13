import tkinter as tk
import main_window
import manage_accounts

if not manage_accounts.check_credentials():
    manage = manage_accounts.ManageAccount()

root = tk.Tk()
root.config(padx=50, pady=50)
main = main_window.MainWindow(root)
main.grid(row=0, column=0)
root.mainloop()

