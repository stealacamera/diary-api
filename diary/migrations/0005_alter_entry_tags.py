# Generated by Django 4.1.1 on 2022-09-21 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0004_alter_entry_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='tag_entries', to='diary.tag'),
        ),
    ]