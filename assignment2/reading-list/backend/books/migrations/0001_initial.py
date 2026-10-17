from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('to_read', 'To read'), ('reading', 'Reading'), ('finished', 'Finished')], default='to_read', max_length=10)),
                ('rating', models.PositiveSmallIntegerField(blank=True, help_text='1-5, optional', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
