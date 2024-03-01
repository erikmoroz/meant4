from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(default=uuid.uuid4, max_length=64)),
                ('original_image', models.ImageField(upload_to='original_images/')),
                ('marked_image', models.ImageField(blank=True, default=None, null=True, upload_to='faces/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(
                    choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('FAILED', 'Failed'),
                             ('SUCCESS', 'Success')], default='PENDING', max_length=100)),
            ],
        ),
    ]
