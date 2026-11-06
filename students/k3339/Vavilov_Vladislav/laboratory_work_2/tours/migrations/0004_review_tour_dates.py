from django.db import migrations, models


def populate_review_dates(apps, schema_editor):
    Review = apps.get_model("tours", "Review")
    for review in Review.objects.select_related("tour").iterator():
        review.tour_start_date = review.tour.start_date
        review.tour_end_date = review.tour.end_date
        review.save(update_fields=["tour_start_date", "tour_end_date"])


class Migration(migrations.Migration):
    dependencies = [("tours", "0003_alter_tour_price")]

    operations = [
        migrations.AddField(
            model_name="review",
            name="tour_start_date",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="review",
            name="tour_end_date",
            field=models.DateField(null=True),
        ),
        migrations.RunPython(populate_review_dates, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="review",
            name="tour_start_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="review",
            name="tour_end_date",
            field=models.DateField(),
        ),
    ]
