import tkinter as tk
import pandas
import smtplib
import imaplib
from tkinter import messagebox


class ManageAccount(tk.Tk):
    def __init__(self, **kw):
        super().__init__(**kw)

        account_data = return_data()

        self.title("Manage account")
        self.config(padx=20, pady=20)

        login_label = tk.Label(self, text='E-mail:')
        login_label.grid(column=0, row=0, sticky='w')

        self.login_input = tk.Entry(self, width=50)
        self.login_input.insert(0, account_data['login'])
        self.login_input.grid(column=1, row=0)

        password_label = tk.Label(self, text='Password:')
        password_label.grid(column=0, row=1, sticky='w')

        self.password_input = tk.Entry(self, width=50)
        self.password_input.insert(0, account_data['password'])
        self.password_input.grid(column=1, row=1)

        self.r_button_var = tk.IntVar()
        gmail_r_button = tk.Radiobutton(self, text="Gmail", variable=self.r_button_var, value=1)
        gmail_r_button.grid(column=0, row=2)

        yahoo_r_button = tk.Radiobutton(self, text="Yahoo Mail", variable=self.r_button_var, value=2)
        yahoo_r_button.grid(column=1, row=2)

        gmail_r_button.select()

        submit_button = tk.Button(text='Submit', command=self.submit)
        submit_button.grid(column=0, row=3, columnspan=2)

        self.mainloop()

    def submit(self):

        login = self.login_input.get()
        password = self.password_input.get()

        if self.r_button_var.get() == 1:
            imap = 'imap.gmail.com'
            smtp = 'smtp.gmail.com'
        else:
            imap = 'imap.mail.yahoo.com'
            smtp = 'smtp.mail.yahoo.com'

        if len(login) > 0 and len(password) > 0:
            account_data = {'login': login, 'password': password, 'imap': imap, 'smtp': smtp}

            account = pandas.DataFrame(account_data, index=[0])
            account.to_csv('login_data.csv')

            if not check_credentials():
                messagebox.showerror("Error", "Wrong credentials!")
            else:
                self.destroy()

        else:
            messagebox.showerror("Error", "Fill all fields!")


def return_data():
    try:
        account = pandas.read_csv('login_data.csv')
        account_data = account.to_dict(orient='records')
        account_data = account_data[0]

        login = account_data['login']
        password = account_data['password']
        imap = account_data['imap']
        smtp = account_data['smtp']

    except FileNotFoundError:
        login = ''
        password = ''
        imap = ''
        smtp = ''

    return {'login': login, 'password': password, 'imap': imap, 'smtp': smtp}


def check_credentials():
    account_data = return_data()

    try:
        smtp_connection = smtplib.SMTP(account_data['smtp'])
        smtp_connection.starttls()
        smtp_connection.login(user=account_data['login'], password=account_data['password'])

        imap_connection = imaplib.IMAP4_SSL(account_data['imap'])
        imap_connection.login(user=account_data['login'], password=account_data['password'])

    except (smtplib.SMTPServerDisconnected, smtplib.SMTPAuthenticationError) as e:
        print(e)
        return False

    else:
        smtp_connection.quit()
        imap_connection.logout()
        return True
