from django.db import models

class ParsedResume(models.Model):
    unique_id = models.CharField(max_length=100, unique=True)
    resume_data = models.TextField()
    clean_data = models.TextField()
    entities = models.JSONField()
    extracted_keywords = models.JSONField()
    keyterms = models.JSONField()
    name = models.CharField(max_length=255, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    emails = models.JSONField()
    phones = models.JSONField()
    years = models.JSONField()
    bi_grams = models.TextField(blank=True, null=True)
    tri_grams = models.TextField(blank=True, null=True)
    pos_frequencies = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or "Parsed Resume"
from django.db import models

# Create your models here.
