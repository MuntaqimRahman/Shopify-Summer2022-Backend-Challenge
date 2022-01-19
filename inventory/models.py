from django.db import models
from taggit.managers import TaggableManager

from django.core.validators import (MinValueValidator,MaxValueValidator)
from decimal import *

# ID automatically created and set as primary key
# Taggable manager does a lot of implicit checking and validation for tags https://django-taggit.readthedocs.io/en/latest/#:~:text=django-taggit%20is%20a%20reusable,commit%3DFalse
class Inventory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)]) #100000 is a reasonable limit to eliminate integer overflow errors while still being useful
    description = models.CharField(max_length=5000, blank=True)
    msrp = models.DecimalField(max_digits=12,decimal_places=2,default=0,validators=[MinValueValidator(Decimal('0.00'))]) #I am assuming here that MSRP will be placed in CAD or USD, would modify decimal places if trying to internationalize
    tags = TaggableManager()

    def __str__(self):
        return self.name