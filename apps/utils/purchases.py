from apps.orders.models import OrderProduct

def user_bought_product(user, product):
    """
    Verifica se o usuário comprou este produto em um pedido concluído
    """
    if not user.is_authenticated:
        return False

    return OrderProduct.objects.filter(
        order__user=user,
        order__type='COMPLETED',
        product_variant__product=product
    ).exists()
