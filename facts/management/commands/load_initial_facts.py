from django.core.management.base import BaseCommand
from facts.models import FunFact

class Command(BaseCommand):
    help = 'Loads initial fun facts into the database'

    def handle(self, *args, **kwargs):
        initial_facts = [
            {"content": "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat.", "category": "Food"},
            {"content": "A day on Venus is longer than a year on Venus. It takes 243 Earth days to rotate once on its axis.", "category": "Astronomy"},
            {"content": "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.", "category": "History"},
            {"content": "Octopuses have three hearts, nine brains, and blue blood.", "category": "Animals"},
            {"content": "The average person will spend six months of their life waiting for red lights to turn green.", "category": "Lifestyle"},
            # Add more facts here
        ]
        
        for fact_data in initial_facts:
            FunFact.objects.get_or_create(
                content=fact_data["content"],
                defaults={"category": fact_data["category"]}
            )
            
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(initial_facts)} fun facts'))