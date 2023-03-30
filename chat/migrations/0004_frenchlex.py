# Generated by Django 4.1.3 on 2022-11-08 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0003_chatsession_chatmessage"),
    ]

    operations = [
        migrations.CreateModel(
            name="FrenchLex",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("form", models.CharField(max_length=128)),
                ("lemma", models.CharField(max_length=128)),
                ("morph", models.CharField(max_length=16)),
            ],
        ),
    ]
