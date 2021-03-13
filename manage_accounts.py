import tkinter as tk
import pandas
import smtplib
import imaplib
from tkinter import messagebox


class ManageAccount(tk.Tk):
    def __init__(self, **kw):
        super().__init__(**kw)

        account = return_data()

        self.title("Manage account")
        self.config(padx=20, pady=20)

        email_label = tk.Label(self, text='E-mail:')
        email_label.grid(column=0, row=0, sticky='w')

        self.email_input = tk.Entry(self, width=50)
        self.email_input.insert(0, account['login'])
        self.email_input.grid(column=1, row=0)

        password_label = tk.Label(self, text='Password:')
        password_label.grid(column=0, row=1, sticky='w')

        self.password_input = tk.Entry(self, width=50)
        self.password_input.insert(0, account['password'])
        self.password_input.grid(column=1, row=1)

        self.var = tk.IntVar()
        gmail = tk.Radiobutton(self, text="Gmail", variable=self.var, value=1)
        gmail.grid(column=0, row=2)

        yahoo = tk.Radiobutton(self, text="Yahoo Mail", variable=self.var, value=2)
        yahoo.grid(column=1, row=2)

        gmail.select()

        submit_button = tk.Button(text='Submit', command=self.submit)
        submit_button.grid(column=0, row=3, columnspan=2)

        self.mainloop()

    def submit(self):

        login = self.email_input.get()
        password = self.password_input.get()

        if self.var.get() == 1:
            imap = 'imap.gmail.com'
            smtp = 'smtp.gmail.com'
        else:
            imap = 'imap.mail.yahoo.com'
            smtp = 'smtp.mail.yahoo.com'

        account_data = {'login': login, 'password': password, 'imap': imap, 'smtp': smtp}

        account = pandas.DataFrame(account_data, index=[0])
        account.to_csv('login_data.csv')

        if not check_credentials():
            messagebox.showerror("Error", "Wrong credentials!")
        else:
            self.destroy()


def return_data():
    try:
        data = pandas.read_csv('login_data.csv')
        account = data.to_dict(orient='records')
        account = account[0]

        login = account['login']
        password = account['password']
        imap = account['imap']
        smtp = account['smtp']

    except FileNotFoundError:
        login = ''
        password = ''
        imap = ''
        smtp = ''

    return {'login': login, 'password': password, 'imap': imap, 'smtp': smtp}


def check_credentials():
    account = return_data()

    try:
        smtp_connection = smtplib.SMTP(account['smtp'])
        smtp_connection.starttls()
        smtp_connection.login(user=account['login'], password=account['password'])

        imap_connection = imaplib.IMAP4_SSL(account['imap'])
        imap_connection.login(user=account['login'], password=account['password'])

    except:
        return False

    else:
        return True
