# Generated manually on 2025-09-27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('building_mgmt', '0001_initial'),
        ('equipment_mgmt', '0007_alter_equipment_maintenance_frequency_and_more'),
    ]

    operations = [
        # Step 1: Add the new building_id field (nullable temporarily)
        migrations.AddField(
            model_name='equipment',
            name='building_id',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='equipment',
                to='building_mgmt.building'
            ),
        ),
        # Step 2: Remove the old condominium field
        migrations.RemoveField(
            model_name='equipment',
            name='condominium',
        ),
        # Step 3: Make building_id non-nullable
        migrations.AlterField(
            model_name='equipment',
            name='building_id',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='equipment',
                to='building_mgmt.building'
            ),
        ),
    ]