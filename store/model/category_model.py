from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name
