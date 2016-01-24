from __future__ import unicode_literals

import datetime
from django.db import models


class StrongLifts(models.Model):
    add_at = models.DateField(default=datetime.datetime.now)
    exercise_name = models.CharField(max_length=200)
    exercise_sets = models.IntegerField(default=0)
    exercise_reps = models.IntegerField(default=0)
    exercise_weight = models.IntegerField(default=0)

    def __str__(self):
        return self.exercise_type
