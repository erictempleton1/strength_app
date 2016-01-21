from __future__ import unicode_literals

from django.db import models


class StrongLifts(models.Model):
    updated_date = models.DateTimeField()
    exercise_type = models.CharField(max_length=200)
    exercise_set = models.IntegerField(default=0)
    exercise_rep = models.IntegerField(default=0)

    def __str__(self):
        return self.exercise_type
