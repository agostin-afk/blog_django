from django.core.exceptions import ValidationError


def validate_png(image):
    if not image.name.lower().endswith('.png'):
        print("\n\n\n\nimagem enviada com formato errado\n\n\n\n")
        raise ValidationError('Imagem precisa ser PNG')
