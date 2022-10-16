from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from Members.models import Member, MedicalData, AcademicData
from Members.validators import BirthDateValidator, AddressValidator, DniValidator, PhoneNumberValidator


class DateInput(forms.DateInput):
    input_type = 'date'


genders = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
]


class CreateMemberForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombres', max_length=200, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'first_name', 'placeholder': 'John'}))
    last_name = forms.CharField(label='Apellidos', max_length=200, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'last_name', 'placeholder': 'Doe'}))
    picture_profile = forms.ImageField(label='Imagen de Perfil', required=False, widget=forms.FileInput(
        attrs={'class': 'inputfile inputfile-5', 'id': 'file-5',
               'data-multiple-caption': '{count} archivos seleccionados'}))
    dni = forms.CharField(label='Número de cédula', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label='Género', required=False, choices=genders,
                               widget=forms.Select(attrs={'class': 'form-select'}))
    email = forms.CharField(label='Correo Electrónico', required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'JohnDoe@example.com'}))
    address = forms.CharField(label='Dirección de Domicilio', required=True, max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'address', 'placeholder': 'Calle **** Av. *****'}),
                              validators=[AddressValidator()])
    phone_number = forms.CharField(label='Número de Celular', required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   validators=[PhoneNumberValidator()])
    birth_date = forms.DateField(label='Fecha de Nacimiento', widget=DateInput(attrs={'class': 'form-control'}),
                                 required=True, validators=[BirthDateValidator()])
    bio = forms.CharField(label='Biografía', widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'bio', 'rows': '3', 'placeholder': 'Hola mi nombre es John ...'}),
                          required=False, max_length=300)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')

    class Meta:
        model = Member
        exclude = ['is_active', 'date_joined']


class EditMemberForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombres', max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name', 'placeholder': 'John'}))
    last_name = forms.CharField(label='Apellidos', max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name', 'placeholder': 'Doe'}))
    picture_profile = forms.ImageField(label='Imagen de Perfil', required=False, widget=forms.FileInput(attrs={'class': 'inputfile inputfile-5', 'id': 'file-5', 'data-multiple-caption': '{count} archivos seleccionados'}))
    dni = forms.CharField(label='Número de cédula', widget=forms.NumberInput(attrs={'class': 'form-control'}))


allergies = [
    ('Comida', 'Comida'),
    ('Medicamentos', 'Medicamentos'),
    ('Animales', 'Animales'),
    ('Otro', 'Otro'),
    ('Nada', 'Nada'),
]

blood_types = [
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('No lo sé', 'No lo sé'),
]


class MedicalDataForm(forms.ModelForm):
    allergies = forms.ChoiceField(required=False, choices=allergies,
                                  widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'carg(this);'}),
                                  label='¿Posee alergias?')
    allergies_description = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                            required=False, label='Describa sus alergias')
    blood_type = forms.ChoiceField(required=False, choices=blood_types,
                                   widget=forms.Select(attrs={'class': 'form-select'}),
                                   label='Indique su tipo de sangre')
    chronic_disease = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      required=False, label='¿Posee enfermedades crónicas?')
    disease_history = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      required=False, label='Historial de enfermedades')
    treatment_history = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                        required=False, label='Historial de tratamiento')
    current_medications = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                          required=False, label='Indique medicamentos que consume')
    comment = forms.CharField(max_length=800, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                              required=False, label='Observaciones')

    class Meta:
        model = MedicalData
        exclude = ['member']


class AcademicDataForm(forms.ModelForm):
    STATUS = [
        ('in_process', 'En proceso'),
        ('culminated', 'Culminado'),
        ('paralyzed', 'Paralizado'),
    ]
    LEVEL = [
        ('preschool', 'Preescolar'),
        ('primary', 'Primaria'),
        ('secondary', 'Secundaria'),
        ('technical', 'Técnico'),
        ('technology', 'Tecnología'),
        ('bachelors_degree', 'Licenciatura'),
        ('postgraduate', 'Posgrado'),
        ('doctorate', 'Doctorado'),
        ('postdoc', 'Postdoctorado'),
    ]
    level = forms.ChoiceField(choices=LEVEL, widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(choices=STATUS, widget=forms.RadioSelect())
    aspiration = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control text', 'rows': '5', }),
                                 required=False, label='Aspiraciones')

    class Meta:
        model = AcademicData
        exclude = ['member']
