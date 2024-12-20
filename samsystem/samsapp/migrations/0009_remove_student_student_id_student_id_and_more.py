# Generated by Django 5.1.1 on 2024-12-12 22:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samsapp', '0008_student_class_name_alter_attendance_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='student_id',
        ),
        migrations.AddField(
            model_name='student',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='class_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='samsapp.class'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_email',
            field=models.EmailField(max_length=50),
        ),
    ]
