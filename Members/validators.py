from django.forms import ValidationError
from datetime import date
from Members.models import Member


class DniValidator:
    def __init__(self):
        pass

    def __call__(self, value):
        dni = int(value)
        member = Member.objects.filter(dni__exact=dni).exists()
        if member:
            raise ValidationError('Esta cédula ya está asignada a un miembro existente.')
        return value


class PhoneNumberValidator:
    def __init__(self):
        pass

    def __call__(self, value):
        number = str(value)
        if not number.startswith('+'):
            raise ValidationError('El número debe contener el código de país.')
        return value


class BirthDateValidator:
    def __init__(self, current_year=date.today().year):
        self.current_year = current_year

    def __call__(self, value):
        birth_date_user = value.year
        if birth_date_user <= self.current_year - 5:
            return value
        else:
            raise ValidationError(f'El miembro a registrar debe tener al menos 5 años.')


class AddressValidator:
    def __init__(self):
        pass

    def __call__(self, value):
        address_user = f'{value}'
        if not address_user.startswith('Calle'):
            raise ValidationError('La dirección debe poseer el formato requerido. Calle ***** Av. ******')
        return value
