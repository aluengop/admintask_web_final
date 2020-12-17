# Generated by Django 3.1.1 on 2020-12-13 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_auto_20201213_0107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.FloatField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('apellido_materno', models.CharField(blank=True, max_length=50, null=True)),
                ('apellido_paterno', models.CharField(blank=True, max_length=50, null=True)),
                ('rut', models.FloatField(blank=True, null=True)),
                ('digv', models.CharField(blank=True, max_length=1, null=True)),
                ('correo', models.CharField(blank=True, max_length=50, null=True)),
                ('telefono', models.FloatField(blank=True, null=True)),
                ('activo', models.FloatField(blank=True, null=True)),
                ('clave', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'usuario',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='user',
            name='is_usuario',
            field=models.BooleanField(default=False),
        ),
    ]