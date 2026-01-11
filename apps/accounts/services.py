def update_user_profile(user, data):
    """
    Serviço responsável por atualizar os dados pessoais do usuário.
    Recebe dados já validados pelo formulário.
    """

    user.name = data.get('name')
    user.email = data.get('email')
    user.phone_number = data.get('cell_phone')
    user.date_of_birth = data.get('date_of_birth')

    user.save()

    return user
