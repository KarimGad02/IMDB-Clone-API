from django.contrib import admin
from .models import WatchList, StreamPlatform, Review

# Register your models here.
class WatchListAdmin(admin.ModelAdmin):
    list_display = ['title']

class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = ['name']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['watchlist', 'rating']

admin.site.register(WatchList, WatchListAdmin)
admin.site.register(StreamPlatform, StreamPlatformAdmin)
admin.site.register(Review, ReviewAdmin)
