from django.db import models


class Tag (models.Model):
    title = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.title
