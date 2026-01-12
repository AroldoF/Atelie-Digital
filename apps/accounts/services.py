from .models import Profile

def update_user_profile(user, data):
    """
    Serviço responsável por atualizar os dados pessoais do usuário.
    Recebe dados já validados pelo formulário.
    """

    user.name = data.get('name')
    user.email = data.get('email')
    user.phone_number = data.get('cell_phone')
    user.date_of_birth = data.get('date_of_birth')

    profile_image = data.get('profile_image')

    if profile_image:
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.profile_image = profile_image
        profile.save()

    user.save()
    return user
