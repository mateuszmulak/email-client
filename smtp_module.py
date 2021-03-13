import smtplib
import tkinter as tk
import manage_accounts


class NewMailWindow(tk.Toplevel):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.account = manage_accounts.return_data()

        self.wm_title("New Message")
        self.config(padx=20, pady=20)

        to_label = tk.Label(self, text='To:')
        to_label.grid(column=0, row=0, sticky='w')

        self.to_input = tk.Entry(self, width=50)
        self.to_input.grid(column=1, row=0)

        subject_label = tk.Label(self, text='Subject:')
        subject_label.grid(column=0, row=1, sticky='w')

        self.subject_input = tk.Entry(self, width=50)
        self.subject_input.grid(column=1, row=1)

        self.message_input = tk.Text(self, height=20, highlightthickness=1)
        self.message_input.grid(column=0, row=2, columnspan=2)

        send_button = tk.Button(self, text='Send', width=60, command=self.send_email)
        send_button.grid(column=0, row=3, columnspan=2)

    def send_email(self):
        to_address = self.to_input.get()
        subject = self.subject_input.get()
        message = self.message_input.get("1.0", "end-1c")

        if to_address and subject and message:
            connection = smtplib.SMTP(self.account['smtp'])
            connection.starttls()
            connection.login(user=self.account['login'], password=self.account['password'])
            connection.sendmail(from_addr=self.account['login'], to_addrs=to_address, msg=f'Subject:{subject}\n\n{message}')
            self.destroy()
            self.update()