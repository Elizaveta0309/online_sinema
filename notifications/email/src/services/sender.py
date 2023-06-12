import sendgrid
from core.config import settings
from sendgrid.helpers.mail import Content, Email, Mail, To


def send_message(email: str, content: str) -> None:
    """Sends a message via SendGrid."""
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID)
    from_email = Email(settings.email_from)
    to_email = To(email)
    subject = 'Памагите'
    content = Content('text/html', content)
    mail = Mail(from_email, to_email, subject, content)
    mail_json = mail.get()
    sg.client.mail.send.post(request_body=mail_json)
