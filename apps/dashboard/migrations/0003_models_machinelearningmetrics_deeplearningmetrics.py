# Generated by Django 4.2.6 on 2024-03-26 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_datastudent_cycle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Models',
            fields=[
                ('idModels', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MachineLearningMetrics',
            fields=[
                ('idMachineLearningMetrics', models.AutoField(primary_key=True, serialize=False)),
                ('precision', models.DecimalField(decimal_places=2, max_digits=5)),
                ('recall', models.DecimalField(decimal_places=2, max_digits=5)),
                ('accuracy', models.DecimalField(decimal_places=2, max_digits=5)),
                ('idModels', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.models')),
                ('nameYear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.schoolyear')),
            ],
        ),
        migrations.CreateModel(
            name='DeepLearningMetrics',
            fields=[
                ('idDeepLearningMetrics', models.AutoField(primary_key=True, serialize=False)),
                ('precision', models.DecimalField(decimal_places=2, max_digits=5)),
                ('accuracy', models.DecimalField(decimal_places=2, max_digits=5)),
                ('idModels', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.models')),
                ('nameYear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.schoolyear')),
            ],
        ),
    ]