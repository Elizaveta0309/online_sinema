from abc import ABC, abstractmethod
import sendgrid
from core.config import settings
from sendgrid.helpers.mail import Content, Email, Mail, To
import email
from datetime import datetime


class BaseMailer(ABC):
    """ Базовый сервис отправки писем. """
    @abstractmethod
    def send_message(self, email: str, content: str, subject: str) -> None:
        pass


class SendGridMailer(BaseMailer):
    """ Сервис отправки писем через Sendgrid. """
    def __init__(self, email: str, api_key: str) -> None:
        self.email = email
        self.api_key = api_key
        self._sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID)

    def send_message(self, email: str, content: str, subject: str) -> None:
        """Sends a message via SendGrid."""
        from_email = Email(self.email)
        to_email = To(email)
        subject = subject
        content = Content('text/html', content)
        mail = Mail(from_email, to_email, subject, content)

        mail_json = mail.get()

        self._sg.client.mail.send.post(request_body=mail_json)


class FakeMailer(BaseMailer):
    """ Сервис отправки писем в stdout """
    def __init__(self) -> None:
        pass

    def send_me(self, _email: str, content: str, subject: str) -> None:
        msg = email.message_from_string(content)

        print("From: test@mail.com")
        print("To:", _email)
        print("Subject:", subject)
        print("Date:", datetime.now())

        print("\nMessage:")

        if msg.is_multipart():
            for part in msg.walk():
                self._print_message(part)
        else:
            self._print_message(part)

    def _print_message(self, msg) -> None:
        content_type = msg.get_content_type()
        if content_type == "text/plain" or content_type == "text/html":
            body = msg.get_payload(decode=True).decode()
            print(body)
