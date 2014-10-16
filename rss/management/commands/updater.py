import logging

from django.core.management.base import BaseCommand
import feedparser
import requests
import dateutil.parser
from django.db.models import Q

from readability import Document
from rss import models

feedparser.SANITIZE_HTML = 0

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_concepts(html_document):
    calais_response = requests.post(
        "http://api.opencalais.com/tag/rs/enrich",
        headers={'x-calais-licenseID': '34x76urpaybdcdwwen7qkx9e', 'content-type': 'text/html', 'accept': 'application/json'},
        data=html_document.encode('utf-8')
    ).json()

    for value in calais_response.values():
        if 'name' in value:
            obj, created = models.Concept.objects.get_or_create(name=value['name'])
            yield obj

def update_feed(feed):
    logger.info("Updating %s" % feed)

    rss = feedparser.parse(feed.url)
    
    for entry in rss.entries:
        if models.Entry.objects.filter(url=entry.link).exists():
            logger.debug("Skipping entry: %s" % entry.title)
            continue

        logger.info("Adding entry: %s" % entry.title)

        date = dateutil.parser.parse(entry.published if hasattr(entry, 'published') else entry.updated)
        content = Document(requests.get(entry.link).text).summary()

        concepts = set(get_concepts(content))
        logger.debug("Entry contains concepts: %s" % ', '.join(c.name for c in concepts))
        
        e = models.Entry(feed=feed, title=entry.title, content=content, date=date, url=entry.link)
        e.save()
        e.concepts = concepts
        e.save()

class Command(BaseCommand):
    help = "Update everything"

    def handle(self, feed_id=None, **kwargs):
        if feed_id is None:
            feeds = models.Feed.objects.all()
        else:
            feeds = [models.Feed.objects.get(id=int(feed_id))]

        for feed in feeds:
            update_feed(feed)

