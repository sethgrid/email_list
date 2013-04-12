# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson
from lists.models import Sender, Email, List

def index(request):
    return HttpResponse("Hello world! You're at the Lists index.")

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

def _get_sender(sender_name):
    # get the first result back for the requested sender name
    try:
        sender = Sender.objects.filter(name=sender_name)[0]
    except IndexError:
        sender = None
    return sender

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
