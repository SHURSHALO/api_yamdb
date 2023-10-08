from django.core.exceptions import ValidationError
from django.utils import timezone


MIN_SCORE = 1
MAX_SCORE = 10


def check_year_availability(year):
    current_year = timezone.now().year
    if year and year >= current_year:
        raise ValidationError(
            'Год выпуска произведения не должен быть больше текущего.'
        )

def check_score(score):
    if not (MIN_SCORE <= score <= MAX_SCORE):
        raise ValidationError(
            f'Оценка должна быть от {MIN_SCORE} до {MAX_SCORE}'
        )
