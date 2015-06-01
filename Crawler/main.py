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


if __name__ == '__main__':

    application = get_wsgi_application()

    # !!!TODO: Crawl all confessions from Google drive, save them to database in
    # group labeling by 'raw'
    # ??? Marking crawled confessions in Google drive (Put something into the sheet ?)

    raw = ConfessionGroup.objects.filter(label='raw')
    if len(raw) == 0:
        raw = ConfessionGroup.objects.create(label='raw')
        raw.save()
    else:
        raw = raw[0]
