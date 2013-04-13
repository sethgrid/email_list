from django.core.management.base import BaseCommand, CommandError
from lists.models import Sender, Email, List

class Command(BaseCommand):
    args = 'drop'
    help = ''''
    $ python manage.py populate 
    Populates database with seed data of Senders A, B, C, D, and E. Populates 200 email addresses spread between them with some addresses shared and some unsubscribed.
    
    $ python manage.py populate drop
    drops data from the database prior to populating the database as normal
    '''

    def handle(self, *args, **options):
        emails_to_create = 200
        percent_chance_to_add_to_list = 75
        percent_chance_to_unsub = 25

        # if drop is set, remove all relevant data
        if args and args[0] == 'drop':
            Sender.objects.all().delete()
            Email.objects.all().delete()
            List.objects.all().delete()

            self.stdout.write("Data dropped")

        # if sender does not exist, create
        names = ['A', 'B', 'C', 'D', 'E']
        for name in names:
            sender = Sender.objects.filter(name=name)
            if not sender:
                sender = Sender()
                sender.name = name
                sender.save()

        senders = Sender.objects.all()

        self.stdout.write("Senders created")

        # create the emails and assign to senders in List
        for i in range(emails_to_create):
            import random

            # slight chance for data collision, acceptable here
            address = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range (8))
            email = Email()
            email.email_address = address + '@example.com'
            email.save()

            # go through each sender...
            for i in range(len(senders)):
                # chance to attach this email with this sender
                if int(random.randrange(100)) > percent_chance_to_add_to_list:
                    sender_list = List()
                    sender_list.sender = senders[i]
                    sender_list.recipient = email

                    # chance to have this email unsubscribed from this sender
                    if int(random.randrange(100)) < percent_chance_to_unsub:
                        sender_list.unsubscribed = 1

                    sender_list.save()

        self.stdout.write("Email addresses created and assigned to senders")

# make sure that the standard use cases are covered
