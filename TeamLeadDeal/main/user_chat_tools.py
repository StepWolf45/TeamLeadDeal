import datetime

from django.db.models import Q

from .models import Chat, Message
from .profile import Profile


class CallUsers:
    """
    Этот класс возвращает модели получателя и отправителя
    """
    @staticmethod
    def call(user_chat):
        users = {}
        recipient = Profile.objects.get(pk=user_chat.kwargs['pk'])
        author = Profile.objects.get(user=user_chat.request.user)

        users['recipient'] = recipient
        users['author'] = author

        return users


class ChatValid:
    """
    Проверяет, существует ли пользователь в контактах у другого пользователя.
    """
    @staticmethod
    def for_author(user_chat):
        if Chat.objects.filter(profile=user_chat.author).count() == 0:
            authors_chat = Chat(
                profile=user_chat.author
            )
            authors_chat.save()

        else:
            authors_chat = Chat.objects.get(profile=user_chat.author)

        if user_chat.recipient not in authors_chat.contacts.all():
            authors_chat.contacts.add(user_chat.recipient)

    @staticmethod
    def valid_for_author(author, recipient):
        """
        This function checks that 'Has author ever chat to the recipient?'.
        """
        if Chat.objects.filter(profile=author).count() == 0:  # Has author any contacts?
            authors_chat = Chat(
                profile=author
            )
            authors_chat.save()

        else:
            authors_chat = Chat.objects.get(profile=author)

        if recipient not in authors_chat.contacts.all():  # Add recipient into author`s contacts
            authors_chat.contacts.add(recipient)

    @staticmethod
    def valid_for_recipient(author, recipient):
        """
        This function checks that 'Has recipient ever chat to the author?'.
        """
        if Chat.objects.filter(profile=recipient).count() == 0:  # Has recipient any contacts?
            recipients_chat = Chat(
                profile=recipient
            )
            recipients_chat.save()

        else:
            recipients_chat = Chat.objects.get(profile=recipient)

        if author not in recipients_chat.contacts.all():  # Add author into recipient`s contacts
            recipients_chat.contacts.add(author)

    @staticmethod
    def for_recipient(user_chat):
        if Chat.objects.filter(profile=user_chat.recipient).count() == 0:
            recipients_chat = Chat(
                profile=user_chat.recipient
            )
            recipients_chat.save()

        else:
            recipients_chat = Chat.objects.get(profile=user_chat.recipient)

        if user_chat.author not in recipients_chat.contacts.all():
            recipients_chat.contacts.add(user_chat.author)


class GetMessages:
    @staticmethod
    def get(user_chat):
        correspondence = Message.objects.filter(
            Q(recipient=user_chat.recipient, author=user_chat.author) |
            Q(recipient=user_chat.author, author=user_chat.recipient)
        ).order_by('pk')

        return correspondence


class SaveMessage:
    @staticmethod
    def save(user_chat):
        message = Message(
            message=user_chat.text,
            author=user_chat.author,
            recipient=user_chat.recipient,
            date=datetime.datetime.now()
        )
        message.save()
