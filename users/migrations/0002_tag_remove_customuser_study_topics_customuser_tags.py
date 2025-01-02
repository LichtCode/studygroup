# Generated by Django 5.1.4 on 2025-01-02 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='study_topics',
        ),
        migrations.AddField(
            model_name='customuser',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='users', to='users.tag'),
        ),
    ]