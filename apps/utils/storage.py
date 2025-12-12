import os
from datetime import datetime

def _timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def store_image_upload_path(instance, filename):
    """
    Caminho: stores/image/<timestamp>/filename
    """
    return os.path.join(
        'stores',
        'image',
        _timestamp(),
        filename
    )

def banner_upload_path(instance, filename):
    """
    Caminho: stores/banner/<timestamp>/filename
    """
    return os.path.join(
        'stores',
        'banner',
        _timestamp(),
        filename
    )

def store_gallery_upload_path(instance, filename):
    """
    Caminho: stores/gallery/<timestamp>/filename
    """
    return os.path.join(
        'stores',
        'gallery',
        _timestamp(),
        filename
    )

def product_image_upload_path(instance, filename):
    """
    Caminho: products/image/<timestamp>/filename
    """
    return os.path.join(
        'products',
        'image',
        _timestamp(),
        filename
    )

def variant_image_upload_path(instance, filename):
    """
    Caminho: products/variants/<timestamp>/filename
    """
    return os.path.join(
        'products',
        'variants',
        _timestamp(),
        filename
    )

def profile_image_upload_path(instance, filename):
    """
    Caminho: profiles/image/<timestamp>/filename
    """
    return os.path.join(
        'profiles',
        'image',
        _timestamp(),
        filename
    )
