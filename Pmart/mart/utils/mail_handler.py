from django.core.mail import send_mail

from mart.settings import DEFAULT_FROM_EMAIL


class MailHandler:

    @staticmethod
    def send_custom_mail(mail_subject, message, send_to):
        try:
            return send_mail(mail_subject, message, DEFAULT_FROM_EMAIL, [send_to])
        except Exception as e:
            print(e)
            raise Exception('Mail send fail')