# Generated by Django 4.2 on 2023-11-19 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_teachergroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalresult',
            name='exam_grade',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='finalresult',
            name='final_result2',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='srsone',
            name='result',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='srsone',
            name='week1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srsone',
            name='week2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srsone',
            name='week3',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srsone',
            name='week4',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srsone',
            name='week5',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srsone',
            name='week6',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srsone',
            name='week7',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srstwo',
            name='result2',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='srstwo',
            name='week10',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srstwo',
            name='week11',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srstwo',
            name='week12',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srstwo',
            name='week13',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srstwo',
            name='week14',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srstwo',
            name='week15',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srstwo',
            name='week8',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='srstwo',
            name='week9',
            field=models.IntegerField(default=0),
        ),
    ]
