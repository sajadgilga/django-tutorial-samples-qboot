# Generated by Django 4.2.6 on 2023-11-02 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0002_comment_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="name",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
