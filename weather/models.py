from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CitySearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    city_name = models.CharField(max_length=100)
    search_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-search_datetime']
        indexes = [
            models.Index(fields=['city_name']),
            models.Index(fields=['user', 'city_name']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.city_name} at {self.search_datetime}"