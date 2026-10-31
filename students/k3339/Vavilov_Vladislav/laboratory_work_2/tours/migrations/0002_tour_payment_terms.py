from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='payment_terms',
            field=models.TextField(default='Full payment before departure.'),
        ),
    ]
