from datetime import date

from django.core.exceptions import ValidationError


def year_validator(year):
    """Year field validator. Year can not be negative or be in the future."""
    if year < 0 or year > date.today().year:
        raise ValidationError('Год не может приходится на будущее '
                              'либо быть отрицательным числом!')


def score_validator(score):
    """Year field validator. Score can not be negative or more than 10."""
    if not 0 <= score <= 10:
        raise ValidationError('Оценка должна быть в диапазоне от 0 до 10!')
