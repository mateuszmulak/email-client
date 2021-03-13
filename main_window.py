import tkinter as tk
import smtp_module
import imap_module
import manage_accounts

class MainWindow(tk.Frame):

    def __init__(self, args):
        tk.Frame.__init__(self, args)

        refresh_button = tk.Button(text='Refresh', width=20, command=self.refresh)
        refresh_button.grid(row=0, column=0)

        new_message_button = tk.Button(text='New Message', width=20, command=self.new_message)
        new_message_button.grid(row=0, column=1)

        if not manage_accounts.check_credentials():
            exit()
        imap = imap_module.ImapModule()
        messages = imap.fetch_mail()

        from_label = tk.Label(text='From', font=('Arial', 14, 'bold'))
        from_label.grid(column=0, row=1, sticky='w')
        subject_label = tk.Label(text='Subject', font=('Arial', 14, 'bold'))
        subject_label.grid(column=1, row=1, sticky='w')

        self.new_message_window = None
        self.arg = args
        self.opened_mails = []

        for i, message in enumerate(messages):
            detail_label = tk.Label(text=message['From'])
            detail_label.grid(column=0, row=i + 2, sticky='w')
            subject_label = tk.Label(text=message['Subject'], font=('Arial', 14, 'bold'))
            subject_label.grid(column=1, row=i + 2, sticky='w')
            open_button = tk.Button(text='open', command=lambda details=message: self.open_message(details))
            open_button.grid(column=3, row=i + 2)

    def new_message(self):
        self.new_message_window = smtp_module.NewMailWindow()

    def open_message(self, message):
        window = ReadMail(message['From'], message['Subject'], message['Body'])
        self.opened_mails.append(window)

    def refresh(self):

        if self.new_message_window is not None:
            self.new_message_window.destroy()

        for window in self.opened_mails:
            window.destroy()

        self.destroy()
        self.__init__(self.arg)


class ReadMail(tk.Toplevel):
    def __init__(self, from_mail, subject, message, **kw):
        super().__init__(**kw)

        self.wm_title("Read mail")
        self.config(padx=20, pady=20)

        from_label = tk.Label(self, text=f'From: {from_mail}')
        from_label.grid(column=0, row=0, sticky='w')

        subject_label = tk.Label(self, text=f'Subject: {subject}')
        subject_label.grid(column=0, row=1, sticky='w')

        message_label = tk.Label(self, text=f'{message}', height=20)
        message_label.grid(column=0, columnspan=2, row=3)
