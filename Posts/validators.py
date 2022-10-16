from django.forms import ValidationError
from datetime import date


class DateValidator:
    def __init__(self, current_date=date.today()):
        self.current_date = current_date

    def __call__(self, value):
        if value.year < self.current_date.year or value.month < self.current_date.month:
            raise ValidationError('La fecha debe ser posterior a la actual.')
        return value


class BirthDateValidator:
    def __init__(self, current_year=date.today().year):
        self.current_year = current_year

    def __call__(self, value):
        birth_date_user = value.year
        if birth_date_user <= self.current_year - 5:
            return value
        else:
            raise ValidationError(f'Debes tener al menos 5 años.')
