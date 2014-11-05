from collections import Counter
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.template.loader import render_to_string
from rss.models import Concept, Entry, Category
import json

def home(request):
    return render(request, 'index.html', {'categories': Category.objects.all()})

@csrf_exempt
def concepts(request):
    q = request.POST['query']

    concepts = Concept.objects.filter(name__icontains=q) \
        .annotate(num_entries=Count('entries')) \
        .order_by('-num_entries')[:100]

    concepts = [{'id': c.id, 'name': c.name} for c in concepts]

    return HttpResponse(json.dumps(concepts), content_type='application/json')

def related(request):
    entries = Entry.objects.all()
    concept = None
    if request.GET.get('name', '').strip():
        concept = get_object_or_404(Concept, name=request.GET['name'].strip())
        entries = concept.entries.all()
    if request.GET.get('category', '').strip():
        category = get_object_or_404(Category, name=request.GET['category'].strip())
        entries = entries.filter(feed__category=category)

    related_concepts = Counter()

    for entry in entries.select_related('concepts'):
        related_concepts.update(entry.concepts.all())

    j = {
            'related': [c.name for c, count in related_concepts.most_common(12)], # related_concepts.most_common(12),
            'last_articles': render_to_string('articles.html', {'articles': concept.entries.all().order_by('-date')[:10] if concept else []}),
    }

    return HttpResponse(json.dumps(j), content_type='application/json')
