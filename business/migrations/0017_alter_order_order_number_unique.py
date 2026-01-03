# Generated migration to add unique constraint after backfill

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("business", "0016_backfill_order_numbers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_number",
            field=models.CharField(
                help_text="Unique order tracking number for customer-facing identification",
                max_length=50,
                unique=True,
            ),
        ),
    ]
