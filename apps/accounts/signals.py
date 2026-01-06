from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User

@receiver(post_save, sender=User)
def handle_user_groups(sender, instance, created, **kwargs):
    """
    Sempre que um usuário for salvo, garantimos que ele esteja nos grupos corretos.
    """
    user_group, _ = Group.objects.get_or_create(name='Users')
    artisian_group, _ = Group.objects.get_or_create(name='Artisians')

    # Todo usuário é um cliente
    instance.groups.add(user_group)

    if instance.is_artisan:
        instance.groups.add(artisian_group)
    else:
        instance.groups.remove(artisian_group)