from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Comment, Recipe


@receiver(post_save, sender=Comment)
def update_recipe_on_comment_save(sender, instance, created, **kwargs):
    """
    Signal to update Recipe when a Comment is created or updated.
    """
    recipe = instance.recipe
    if created:
        recipe.stars_sum += instance.rating
        recipe.number_ratings += 1
    else:
        recipe.stars_sum = sum(c.rating for c in Comment.objects.filter(recipe=recipe))

    recipe.save()


@receiver(post_delete, sender=Comment)
def update_recipe_on_comment_delete(sender, instance, **kwargs):
    """
    Signal to update Recipe when a Comment is deleted.
    """
    recipe = instance.recipe
    recipe.stars_sum -= instance.rating
    recipe.number_ratings = max(0, recipe.number_ratings - 1)

    recipe.save()
