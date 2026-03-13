from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_rename_quantity_book_year_remove_book_shelf_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='author',
            new_name='authors',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='year',
            new_name='publication_year',
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(default='', max_length=255, verbose_name='Издательство'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='section',
            field=models.CharField(default='', max_length=100, verbose_name='Раздел'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='cipher',
            field=models.CharField(default='', max_length=50, verbose_name='Шифр'),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='bookcopy',
            old_name='copies',
            new_name='quantity',
        ),
        migrations.AlterField(
            model_name='bookcopy',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Количество экземпляров'),
        ),
    ]
