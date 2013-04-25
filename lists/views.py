# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson
from lists.models import Sender, Email, List

def index(request):
    page = '''
    <html>
    <head><title>Lists</title></head>
    <body>
        Hit up the following json endpoints with sender set to 'A', 'B', 'C', 'D', or 'E':<br />
        For adding or removing email addresses, '@example.com' is automatiacally appended. So '.../add/foo/' will insert as foo@example.com.
        <ul>
            <li>/lists/getlist/{{sender}}/</li>
            <li>/lists/getlist/{{sender}}/subscribes</li>
            <li>/lists/getlist/{{sender}}/unsubscribes</li>
            <li>/lists/getlist/{{sender}}/add/{{email}}</li>
            <li>/lists/getlist/{{sender}}/delete/{{email}}</li>
            <li>/lists/getlist/{{sender}}/update_subscription/{{email}}/subscribed/{{yes|no}}</li>
            <li>/lists/getlist/{{sender}}/update_subscription/{{email}}/subscribed/ <--- will report the subscription status for sender/email</li>
    </body>
    </html>
    '''
    return HttpResponse(page)

# TOC
# get_list(request, sender_name)
# get_subscribed(request, sender_name)
# get_unsubscribed(request, sender_name)

def get_list(request, sender_name=None, unsubscribed=-1):
    sender = _get_sender(sender_name)
    if not sender:
        return _send_error("No Sender Found", 404)

    emails = _get_emails_from_sender(sender.id, unsubscribed)
    data = {"sender": sender.name,
            "emails": emails
           }
    return _send_response(data, 200)

def get_subscribed(request, sender_name=None):
    return get_list(request, sender_name, 0)

def get_unsubscribed(request, sender_name=None):
    return get_list(request, sender_name, 1)

def add_email(request, sender_name, email_address):
    sender = _get_sender(sender_name)
    if not sender:
        return _send_error("No Sender Found", 404)

    email = Email()
    email.email_address = email_address + "@example.com"
    email.save()

    list = List()
    list.sender = sender
    list.recipient = email
    list.save()

    data = {"message": "success"}
    return _send_response(data, 200)


def delete_email(request, sender_name, email_address):
    sender = _get_sender(sender_name)
    if not sender:
        return _send_error("No Sender Found", 404)

    email = _get_email(email_address)
    if not email:
        return _send_error("No Email Found", 404)

    email.delete()

    data = {"message": "success"}
    return _send_response(data, 200)

def update_subscription(request, sender_name, email_address, yes_no):
    sender = _get_sender(sender_name)
    if not sender:
        return _send_error("No Sender Found", 404)

    if yes_no == "no" or yes_no == "0":
        unsubscribed = 1
    else:
        unsubscribed = 0

    email = _get_email(email_address)
    if not email:
        return _send_error("No Email Found", 404)

    try:
        list = List.objects.filter(sender=sender.id, recipient=email.id)[0]
    except IndexError:
        return _send_error("No list contains this sender and this email address", 404)

    list.unsubscribed = unsubscribed
    list.save()

    data = {"message": "success"}
    return _send_response(data, 200)

def show_subscription(request, sender_name, email_address):
    sender = _get_sender(sender_name)
    if not sender:
        return _send_error("No Sender Found", 404)

    email = _get_email(email_address)
    if not email:
        return _send_error("No Email Found", 404)

    try:
        list = List.objects.filter(sender=sender.id, recipient=email.id)[0]
    except IndexError:
        return _send_error("No list contains this sender and this email address", 404)

    status = list.unsubscribed

    data = {"sender": sender.name,
            "email": email.email_address,
            "unsubscribed": status
    }
    return _send_response(data, 200)

def _get_sender(sender_name):
    # get the first result back for the requested sender name
    try:
        sender = Sender.objects.filter(name=sender_name)[0]
    except IndexError:
        sender = None
    return sender

def _get_email(email_address):
    # get the first result back for the requested email address
    try:
        email = Email.objects.filter(email_address=email_address + "@example.com")[0]
    except IndexError:
        email = None
    return email

def _get_emails_from_sender(sender_id, unsubscribedd=0):
    emails = []
    if unsubscribedd is -1:
        list = List.objects.filter(sender=sender_id)
    else:
        list = List.objects.filter(sender=sender_id, unsubscribed=unsubscribedd)

    for list_obj in list:
        print list_obj.unsubscribed, 'is the unsubscribed for ', list_obj.recipient.email_address
        emails.append(list_obj.recipient.email_address )

    return emails

def _send_error(message, status_code):
    data = {"error": message}
    return _send_response(data, status_code)

def _send_response(data, status_code):
    return HttpResponse(
        simplejson.dumps(data),
        status = status_code,
        content_type = 'application/javascript; charset=utf8',
    )
