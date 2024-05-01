from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class StreamPlatform(models.Model):
    name = models.CharField(max_length=20)
    about = models.CharField(max_length=100)
    website = models.URLField()

    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=100)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE,
                                 related_name='watchlist')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models. PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE,
                                  related_name='reviews')

    def __str__(self):
        return self.watchlist.title + " " + str(self.rating) + " " + str(self.review_user)