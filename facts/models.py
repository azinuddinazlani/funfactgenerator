from django.db import models

# Create your models here.
class FunFact(models.Model):
    content = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.content[:50]