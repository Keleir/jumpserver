# Generated by Django 2.1.7 on 2019-06-28 11:47

from django.db import migrations, models
from functools import reduce


def migrate_old_actions(apps, schema_editor):
    from orgs.utils import set_to_root_org
    set_to_root_org()
    perm_model = apps.get_model('perms', 'AssetPermission')
    db_alias = schema_editor.connection.alias
    perms = perm_model.objects.using(db_alias).all()
    actions_map = {
        "all": 0b11111111,
        "connect": 0b00000001,
        "upload_file": 0b00000010,
        "download_file": 0b00000100,
    }

    for perm in perms:
        actions = perm.actions.all()
        if not actions:
            continue
        new_actions = [actions_map.get(action.name, 0b11111111) for action in actions]
        new_action = reduce(lambda x, y: x | y, new_actions)
        perm.action = new_action
        perm.save()


class Migration(migrations.Migration):

    dependencies = [
        ('perms', '0005_auto_20190521_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetpermission',
            name='action',
            field=models.IntegerField(choices=[(255, 'All'), (1, 'Connect'), (2, 'Upload file'), (4, 'Download file'), (6, 'Upload download')], default=255, verbose_name='Actions'),
        ),
        migrations.RunPython(migrate_old_actions),
    ]
