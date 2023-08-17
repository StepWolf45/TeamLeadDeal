import datetime

from ..models import *


class NoteAjax:
    def __init__(self, request, worksheet_pk):
        self.context = {
            'comments': []
        }
        self.worksheet = Worksheet.objects.get(pk=worksheet_pk)
        self.user_profile = Profile.objects.get(user=request.user)

        self.likes = Like.objects.filter(worksheet=self.worksheet)
        self.dislikes = Dislike.objects.filter(worksheet=self.worksheet)
        self.comments = Comment.objects.filter(worksheet=self.worksheet).order_by('-pk')

        self.is_liked = self.likes.filter(user=self.user_profile).count()
        self.is_disliked = self.dislikes.filter(user=self.user_profile).count()

    def get(self):
        """
        This function loads on the page count of likes, dislikes and comments.
        """
        for comment in self.comments:
            self.context['comments'].append(
                {
                    'comment_id': comment.pk,
                    'text_message': comment.text_message,
                    'author': [comment.author.user.username, comment.author.pk],
                    'date': comment.date
                }
            )

        self.context['is_liked'] = self.is_liked
        self.context['is_disliked'] = self.is_disliked

        self.context['likes'] = self.likes.count()
        self.context['dislikes'] = self.dislikes.count()

        return self.context

    def post(self, data):
        """
        This function analyse and set current note for the worksheet.
        """
        if data['note']:
            if data['note'] == 'like':
                if self.is_liked == 0:
                    like = Like(
                        user=self.user_profile,
                        worksheet=self.worksheet
                    )
                    like.save()
                else:
                    Like.objects.get(user=self.user_profile, worksheet=self.worksheet).delete()

            if data['note'] == 'dislike':
                if self.is_disliked == 0:
                    dislike = Dislike(
                        user=self.user_profile,
                        worksheet=self.worksheet
                    )
                    dislike.save()
                else:
                    Dislike.objects.get(user=self.user_profile, worksheet=self.worksheet).delete()

        if data['comment']:
            comment = Comment(
                text_message=data['comment'],
                author=self.user_profile,
                worksheet=self.worksheet,
                date=datetime.datetime.now()
            )
            comment.save()


class CommentDelete:
    """
    This class delete comments.
    """
    def __init__(self, data):
        self.comment_on_delete = Comment.objects.get(pk=data['commentID'])

    def delete(self):
        self.comment_on_delete.delete()
