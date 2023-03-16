import email
import imaplib
import os

from dotenv import load_dotenv

from services import ReaderBarcodeTicketPdf


class ImapConfig:

    def __init__(self, email: str, password: str, server: str):
        self.email = email
        self.password = password
        self.server = server


class ImapGmailController:

    def __init__(self, config_imap: ImapConfig):
        self.config = config_imap
        self.imap = imaplib.IMAP4_SSL(config_imap.server)

    def _login_imap(self):
        self.imap.login(self.config.email, self.config.password)

    def _logout_imap(self):
        self.imap.close()
        self.imap.logout()


def email_move_to_path(imap: imaplib.IMAP4_SSL, _id, path_to_move: str):
    result, content = imap.copy(_id.decode(), path_to_move)
    if result == "OK":
        mov, data = imap.store(_id.decode(), '+FLAGS', '\\Deleted')
        imap.expunge()


def main():
    emails_account = ["no-reply@logafaturamento.com.br", "contadigitalvivo@vivo.com.br"]
    subject_text = ["conta", "fatura"]
    invoice_path = "Faturas"

    load_dotenv()

    reader_barcode = ReaderBarcodeTicketPdf()

    imap_server = os.getenv("IMAP_SERVER")
    imap_email = os.getenv('IMAP_EMAIL')
    imap_password = os.getenv('IMAP_PASSWORD')

    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(imap_email, imap_password)

    imap.select("INBOX")

    data, message_numbers = imap.search(None, "ALL")

    messages = message_numbers[0].split()
    messages.reverse()
    for message_id in messages:
        _, dados = imap.fetch(message_id, "(RFC822)")

        email_content = dados[0][1]
        content = email.message_from_bytes(email_content)

        print(f"To: {content['To']}")
        print(f"From: {content['From']}")
        print(f"Subject: {content['Subject']}")
        print(f"Content Length: {len(content.get_payload())}")
        print("==========\n")

        email_move_to_path(imap, message_id, invoice_path)

        print("Movido com Sucesso\n")

    imap.logout()
    imap.close()


if __name__ == '__main__':
    main()
