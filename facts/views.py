from django.shortcuts import render
from django.http import JsonResponse
import random
from .models import FunFact

def home(request):
    # Get a random fun fact for initial page load
    facts = list(FunFact.objects.all())
    if facts:
        random_fact = random.choice(facts)
    else:
        random_fact = None
    return render(request, 'facts/home.html', {'fact': random_fact})

def get_random_fact(request):
    # API endpoint to get a random fact
    facts = list(FunFact.objects.all())
    if facts:
        random_fact = random.choice(facts)
        return JsonResponse({
            'content': random_fact.content,
            'category': random_fact.category
        })
    return JsonResponse({'error': 'No facts available'}, status=404)