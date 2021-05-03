# Generated by Django 3.2 on 2021-05-02 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Mensaje')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('receiver_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_set', to=settings.AUTH_USER_MODEL, verbose_name='Receptor')),
                ('sender_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_set', to=settings.AUTH_USER_MODEL, verbose_name='Emisor')),
            ],
            options={
                'verbose_name': 'Mensajes',
                'ordering': ('creation_date',),
            },
        ),
    ]
