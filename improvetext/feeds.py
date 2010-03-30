# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from models import Improvement

class LatestImprovementsFeed(Feed):
    title = "Improvement auf BundesTagger"
    link = "/"
    description = "Improvement Vorschläge auf BundesTagger"
    description_template = "improvetext/improvement_description.html"

    def items(self):
        return Improvement.objects.order_by('-date')[:5]

class LatestImprovementsFeedAtom(LatestImprovementsFeed):
    feed_type = Atom1Feed
    subtitle = LatestImprovementsFeed.description