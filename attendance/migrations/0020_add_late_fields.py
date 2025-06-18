from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0018_attendance_late_attendance_late_reason_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='late',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='attendance',
            name='late_reason',
            field=models.CharField(max_length=200, blank=True, null=True),
        ),
    ]
