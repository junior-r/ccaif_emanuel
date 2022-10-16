from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.core.exceptions import ValidationError

from Posts.validators import DateValidator, BirthDateValidator
from Posts.models import Event, EventParticipant
from Members.models import Member


class DateInput(forms.DateInput):
    input_type = 'date'


class EventForm(forms.ModelForm):
    image = forms.ImageField(label='Imagen del evento', required=False, widget=forms.FileInput(attrs={'class': 'inputfile inputfile-5', 'id': 'file-5', 'data-multiple-caption': '{count} archivos seleccionados'}))
    title = forms.CharField(label='Título del evento', max_length=200, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control text', 'id': 'title floatingInput title_event', 'placeholder': 'La gran boda del año'}))
    description = forms.CharField(label='Descripción', widget=forms.Textarea(
        attrs={'class': 'form-control text', 'id': 'desc', 'rows': '3', 'placeholder': 'Te invitamos a la boda de Joe y Jane...'}),
                          required=False, max_length=300)
    place = forms.CharField(label='Lugar del evento', max_length=200, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control text', 'id': 'place floatingInput', 'placeholder': 'Calle *** Av. ***, Ciudad, País'}))
    date = forms.DateField(label='Fecha del evento', widget=DateInput(attrs={'class': 'form-control text', 'id': 'floatingInput'}), required=False, validators=[DateValidator()])
    form = forms.BooleanField(label='¿Habilitar inscripciones?', widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'flexCheckDefault check_form', 'onChange': 'comprobar(this);'}), required=False)
    max_num_partp = forms.CharField(label='Máximo de participantes', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '100', 'id': 'max_num_partp'}), required=False)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')

    class Meta:
        exclude = ['user', 'created_at', 'active']
        model = Event


class EventParticipantForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombres', max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Apellidos', max_length=250, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(label='Fecha de Nacimiento', widget=DateInput(attrs={'class': 'form-control text'}), required=True, validators=[BirthDateValidator()])
    is_member = forms.BooleanField(label='¿Eres miembro?', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')

    class Meta:
        exclude = ['event', 'created_at']
        model = EventParticipant

    def clean_is_member(self):
        is_member = self.cleaned_data['is_member']
        first_name = self.cleaned_data['first_name']

        if is_member:
            member = Member.objects.filter(first_name__exact=first_name).exists()
            if not member:
                raise ValidationError(f'El nombre {first_name} no coincide con los miembros.')

        return is_member
