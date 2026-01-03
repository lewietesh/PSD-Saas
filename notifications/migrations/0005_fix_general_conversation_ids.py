# notifications/migrations/0005_fix_general_conversation_ids.py
# Data migration to fix existing general messages with scattered conversation_ids

from django.db import migrations


def fix_general_conversation_ids(apps, schema_editor):
    """
    Fix existing general messages to use consistent conversation_id per user.
    Format: 'general-{user_id}'
    """
    Message = apps.get_model('notifications', 'Message')
    
    # Get all general messages
    general_messages = Message.objects.filter(message_type='general')
    
    # Update each message to use the consistent conversation_id format
    for message in general_messages:
        if message.user_id:
            new_conversation_id = f'general-{message.user_id}'
            if message.conversation_id != new_conversation_id:
                message.conversation_id = new_conversation_id
                message.save(update_fields=['conversation_id'])


def reverse_migration(apps, schema_editor):
    """
    Reverse migration - no action needed as we can't restore original UUIDs
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_message_conversation_id_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_general_conversation_ids, reverse_migration),
    ]
