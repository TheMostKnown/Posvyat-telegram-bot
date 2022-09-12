# Generated by Django 4.1.1 on 2022-09-12 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0004_button_config_guestschedule_issue_level_organizers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadcast',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='button',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='guest',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='guestschedule',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('N', 'Not solved'), ('P', 'In progress'), ('F', 'Fixed')], default='N', max_length=256),
        ),
        migrations.AlterField(
            model_name='level',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='organizers',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='organizerschedule',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='script',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
