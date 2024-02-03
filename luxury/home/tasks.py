from django.core.mail import EmailMessage
from django.conf import settings
from huey.contrib.djhuey import task


@task()
def email_notification(subject, message, recipient_list, attachments=[]):
    try:
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        for attachment in attachments:
            email.attach(
                attachment["filename"], attachment["content"], attachment["mimetype"]
            )
        email.send(fail_silently=False)
    except Exception as e:
        print(e)
