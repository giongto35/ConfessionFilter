from django.db import models

class PublishedConfession(models.Model):

    document = models.TextField(null=False, blank=False)
    submitted_date = models.TimeField(null=True, blank=True, auto_now_add=True)

    classify_score = models.FloatField(null=True, blank=True)

    published_id = models.IntegerField(null=False, default=0)
    published_date = models.TimeField(null=False, auto_now_add=True)
    confession_url = models.CharField(max_length=1024, blank=True, null=True)
