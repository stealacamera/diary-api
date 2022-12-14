# Generated by Django 4.1.1 on 2022-09-22 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0006_alter_entry_tags'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='folder',
            name='unique_folder_per_user',
        ),
        migrations.RemoveConstraint(
            model_name='tag',
            name='unique_tag_per_user',
        ),
        migrations.RenameField(
            model_name='folder',
            old_name='folder',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='tag',
            new_name='name',
        ),
        migrations.AddConstraint(
            model_name='folder',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_folder_per_user'),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_tag_per_user'),
        ),
    ]
