from django.db import models

from apps.models import BaseModel


class Area(BaseModel):
    HEALTH = "Physical and Health"
    FINANCE = "Financial and Cash Flow"
    HOBBY = "Recreational, Hobbies and Vacations"
    WORK = "Work, Vocational and Volunteer Involvement"
    ROMANCE = "Relational Romance and significant Other"
    FAMILY = "Family and Inner Circle"
    FRIEND = "Friends and Social Circle"
    SPIRITUAL = "Spiritual and Personal Growth"

    AREA_CHOICES = [
        ("Health", HEALTH),
        ("Finance", FINANCE),
        ("Hobby", HOBBY),
        ("Work", WORK),
        ("Romance", ROMANCE),
        ("Family", FAMILY),
        ("Friend", FRIEND),
        ("Spiritual", SPIRITUAL),
    ]

    name = models.CharField(max_length=10, choices=AREA_CHOICES, verbose_name="Areas of Life")

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        ordering = ['name']

    def __str__(self):
        return self.name
