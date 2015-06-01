from django.db import models


class ConfessionGroup(models.Model):
    label = models.CharField(max_length=10, null=False, blank=False)
    # positive: The automatic classification gave positive result
    # negative: The automatic classification gave positive result
    # legal: Reviewed by confession administrators (confessions which belong to this group will be posted automatically)
    # ilegal: Reviewed by confession administrators and will not be posted


class ConfessionDocument(models.Model):
    group = models.ForeignKey(ConfessionGroup, related_name='documents', null=True, blank=True, on_delete=models.SET_NULL)

    document = models.TextField(null=False, blank=False)
    submitted_date = models.TimeField(null=True, blank=True, auto_now_add=True)

    comment = models.TextField(null=True, blank=True)
    classify_score = models.FloatField(null=True, blank=True)
