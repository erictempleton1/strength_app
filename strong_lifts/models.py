from __future__ import unicode_literals

from django.db import models


class StrongLifts(models.Model):
    added_date = models.DateTimeField(auto_now_add=True, blank=True)
    exercise_name = models.CharField(max_length=200)
    exercise_set = models.IntegerField(default=0)
    exercise_rep = models.IntegerField(default=0)
    exercise_weight = models.IntegerField(default=0)

    def __str__(self):
        return self.exercise_type
