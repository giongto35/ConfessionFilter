#!/usr/bin/env python

import os
import sys

# Before importing some Django lib, we must have this
from django.core.wsgi import get_wsgi_application


if __name__ == '__main__':

    # Import Django environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurations.settings")


# Improt Django models
from Filter.models import ConfessionGroup, ConfessionDocument
from Publisher.models import PublishedConfession


if __name__ == '__main__':

    application = get_wsgi_application()

    # !!!TODO: Fetch all confessions from group labeling by 'legal' and
    # post automatically, then move them into PublishedConfession

    # Assume that the legal group has been created
    legal = ConfessionGroup.objects.filter(label='legal')[0]
