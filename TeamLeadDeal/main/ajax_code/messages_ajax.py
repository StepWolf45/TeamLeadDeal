import datetime

from django.db.models import Q
from ..models import *
from ..user_chat_tools import ChatValid


class MessagesAjax:
    def __init__(self, request, user_pk):
        self.sender = Profile.objects.get(user=request.user)
        self.recipient = Profile.objects.get(pk=user_pk)
        self.context = {
            'messages': []
        }

    def get(self):
        """
        This function gets messages of users.
        """
        messages = Message.objects.filter(
                Q(author=self.sender, recipient=self.recipient) | Q(author=self.recipient, recipient=self.sender)
            ).order_by('pk')

        for message in messages:
            self.context['messages'] += [{
                    'text': str(message.message),
                    'author': str(message.author),
                    'recipient': str(message.recipient),
                    'date': str(message.date)
                }]

        return self.context

    @staticmethod
    def post(data):
        """
        This function save the message, that one of users had sent.
        """
        author = Profile.objects.get(user__username=data['author'])
        recipient = Profile.objects.get(user__username=data['recipient'])

        chat_valid = ChatValid()

        chat_valid.valid_for_author(author, recipient)
        chat_valid.valid_for_recipient(author, recipient)

        message = Message(
            message=data['text'],
            author=author,
            recipient=recipient,
            date=datetime.datetime.now().time()
        )
        message.save()
