from django.contrib import admin
from .models import User, Recipe, Tag, RecipeTag, Comment, SavedRecipe, Subscription, Rating

# Register your models here.

admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(RecipeTag)
admin.site.register(Comment)
admin.site.register(SavedRecipe)
admin.site.register(Subscription)
admin.site.register(Rating)
