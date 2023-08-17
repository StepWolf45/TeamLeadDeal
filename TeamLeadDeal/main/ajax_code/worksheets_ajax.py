from ..models import *


class WorksheetsAjax:
    def __init__(self, worksheets_count, data):
        self.data = data

        if self.data:
            self.worksheets = list(
                set(Worksheet.objects.filter(tags__in=data)[:worksheets_count])
            )[::-1]
        else:
            self.worksheets = Worksheet.objects.all().order_by('-pk')[:worksheets_count]

        self.context = {
            'worksheets': []
        }

    def get_context(self):
        """
        This function gets part of worksheets.
        """
        for i in self.worksheets:
            self.context['worksheets'].append(
                {
                    'title': i.title,
                    'image': i.image.url,
                    'author': str(i.author),
                    'tags': [
                        {
                            'title': tag.title,
                            'color': tag.color
                        } for tag in i.tags.all()
                    ],
                    'likes': Like.objects.filter(worksheet=i).count(),
                    'dislikes': Dislike.objects.filter(worksheet=i).count(),
                    'comments': Comment.objects.filter(worksheet=i).count(),
                    'link': f'/worksheet{i.id}',
                    'date': i.date
                }
            )

        return self.context
