from django.db import migrations
from django.apps import apps as global_apps
from django.contrib.auth.management import create_permissions

def create_groups_and_permissions(apps, schema_editor):
    for app_config in global_apps.get_app_configs():
        create_permissions(app_config, verbosity=0)

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    user_group, _ = Group.objects.get_or_create(name='Users')
    artisian_group, _ = Group.objects.get_or_create(name='Artisians')
 
    codenames_user = [
        # Accounts: 
        'add_address','view_address', 'change_address', 'delete_address',
        'view_profile', 'change_profile',
        # Products: apenas ver
        'view_product', 'view_productvariant', 'view_variantimage', 'view_attribute', 
        'view_variantattribute', 
        # Carts: criar, ver e mudar
        'add_cart', 'view_cart', 'change_cart',
        'add_cartitem', 'view_cartitem', 'change_cartitem', 'delete_cartitem',
        # Orders: criar e ver seus pedidos
        'add_order', 'view_order', 
        'add_orderproduct', 'view_orderproduct',
        # Reviews: avaliar e ver avaliações
        'add_productreview', 'view_productreview',
        # Favorite:
        'add_favorite', 'view_favorite', 'delete_favorite'
        # Chats: conversar
        'add_chat', 'view_chat', 'add_message', 'view_message',
        # Stores: visualizar lojas
        'view_store',
    ]
    
    perms_user = Permission.objects.filter(codename__in=codenames_user)
    user_group.permissions.set(perms_user)

    
    # Filtramos permissões completas (add, change, delete, view) por app_label
    perms_manage_products = Permission.objects.filter(content_type__app_label='products')
    perms_manage_stores = Permission.objects.filter(content_type__app_label='stores')
    
    # Permissões extras de vendas (mudar status de pedido)
    perms_sales = Permission.objects.filter(
        content_type__app_label='orders', 
        codename__startswith='change_'
    )


    all_artisian_perms = perms_user | perms_manage_products | perms_manage_stores | perms_sales
    artisian_group.permissions.set(all_artisian_perms.distinct())

def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Users', 'Artisians']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'), 
        ('products', '0001_initial'),
        ('orders', '0001_initial'),
        ('stores', '0001_initial'),
        ('chats', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions, reverse_code=remove_groups),
    ]