from django.db import models


class ConfessionGroup(models.Model):
    label = models.CharField(max_length=10, null=False, blank=False)


class ConfessionDocument(models.Model):
    group = models.ForeignKey(ConfessionGroup, related_name='documents', null=True, blank=True, on_delete=models.SET_NULL)

    document = models.TextField(null=False, blank=False)
    date = models.TimeField(null=True, blank=True, auto_now_add=True)
