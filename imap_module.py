import imaplib
import email
import manage_accounts


class ImapModule:
    def __init__(self):
        account = manage_accounts.return_data()
        self.connection = imaplib.IMAP4_SSL(account['imap'])
        self.connection.login(user=account['login'], password=account['password'])

    def fetch_mail(self):
        self.connection.select('Inbox')
        tmp, data = self.connection.search(None, 'ALL')
        messages = []
        for num in data[0].split():
            tmp, data = self.connection.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    if part['Subject'] and part['From']:
                        new_message = {'Subject': part['Subject'], 'From': part['From'], 'Date': part['Date'],
                                       'Body': part.get_payload()}
                        messages.append(new_message)

        return messages
