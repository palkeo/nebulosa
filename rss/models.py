from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Concept(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name

class Feed(models.Model):
    title = models.CharField(help_text="Title of the feed", max_length=255)
    url = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='feeds', null=True)

    def __str__(self):
        return "%s (%s)" % (self.title, self.url)
    
class Entry(models.Model):
    feed = models.ForeignKey(Feed, related_name='entries')

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    date = models.DateTimeField()

    concepts = models.ManyToManyField(Concept, related_name='entries')

    url = models.TextField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('date',)
        verbose_name_plural = 'entries'
