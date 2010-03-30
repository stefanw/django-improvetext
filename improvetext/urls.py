from django.conf.urls.defaults import *
from django.conf import settings
from feeds import LatestImprovementsFeed, LatestImprovementsFeedAtom

private_feed = getattr(settings,"IMPROVEMENT_PRIVATE_FEED", "latest")

urlpatterns = patterns('',
    (r'^%s/rss/$' % private_feed, LatestImprovementsFeed()),
    (r'^%s/atom/$' % private_feed, LatestImprovementsFeedAtom()),
    (r'^apply/$', "improvetext.views.apply_improvement" , {}, 'improvetext-improvement-apply'),
)