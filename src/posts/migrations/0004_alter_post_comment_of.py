# Generated by Django 4.1.7 on 2023-06-07 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_comment_of_delete_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comment_of',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='posts.post'),
        ),
    ]