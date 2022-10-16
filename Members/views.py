from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from Members.forms import CreateMemberForm, MedicalDataForm, AcademicDataForm
from Members.models import Member, MedicalData, AcademicData
from Users.models import User
import requests
from CCVAE.settings import GOOGLE_MAPS_API_KEY
from django.db.models import Q


@login_required
@permission_required('Members.add_member')
def create(request):
    data = {
        'form': CreateMemberForm()
    }

    if request.method == 'POST':
        form = CreateMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Miembro guardado con éxito.')
            return redirect('create_member')
        else:
            messages.error(request, 'Algún dato ingresado es inválido. ¡Intente de nuevo!')
            data['form'] = form

    return render(request, 'members/create_members.html', data)


@login_required
@permission_required('Members.view_member')
def view_members(request):
    members = Member.objects.all()

    data = {
        'members': members
    }
    return render(request, 'members/members.html', data)


@login_required
@permission_required('Members.view_member')
def view_member(request, id, *args, **kwargs):
    member = Member.objects.get(id=id)

    data = {
        'member': member
    }
    params = {
        'key': GOOGLE_MAPS_API_KEY,
        'address': member.address
    }
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(base_url, params=params).json()
    if response['status'] == 'OK':
        geometry = response['results'][0]
        lat = geometry['geometry']['location']['lat']
        lon = geometry['geometry']['location']['lng']
        real_address_user = f"{geometry['formatted_address']}/{lat},{lon}"
        data['real_address_user'] = real_address_user

    return render(request, 'members/view_member.html', data)


@login_required
@permission_required('Members.add_medicaldata')
def create_medical_data(request, member_id):
    member = Member.objects.get(id=member_id)
    user = User.objects.get(id=request.user.id)

    data = {
        'form': MedicalDataForm(),
        'member': member
    }

    if request.method == 'POST':
        form = MedicalDataForm(request.POST, request.FILES)
        if form.is_valid():
            allergies = form.cleaned_data['allergies']
            blood_type = form.cleaned_data['blood_type']
            allergies_description = form.cleaned_data['allergies_description']
            chronic_disease = form.cleaned_data['chronic_disease']
            disease_history = form.cleaned_data['disease_history']
            treatment_history = form.cleaned_data['treatment_history']
            current_medications = form.cleaned_data['current_medications']
            comment = form.cleaned_data['comment']

            try:
                query = MedicalData.objects.create(
                    member_id=member.id,
                    allergies=allergies,
                    blood_type=blood_type,
                    allergies_description=allergies_description,
                    chronic_disease=chronic_disease,
                    disease_history=disease_history,
                    treatment_history=treatment_history,
                    current_medications=current_medications,
                    comment=comment
                )

                query.save()
                messages.success(request, f'Datos medicos de {member.get_full_name()} registrados con éxito.')
                return redirect('view_member', member_id)
            except IntegrityError as unique:
                messages.error(request, f'Este usuario ya posee datos médicos registrados.')
                data['form'] = form
            except Exception as e:
                messages.error(request, f'Ocurrió un error.')
                print(e)
                data['form'] = form

    return render(request, 'medical_data/create_data.html', data)


@login_required
def create_academic_data(request, member_id):
    member = Member.objects.get(id=member_id)

    data = {
        'form': AcademicDataForm(),
        'member': member
    }

    if request.method == 'POST':
        form = AcademicDataForm(request.POST, request.FILES)
        if form.is_valid():
            level = form.cleaned_data['level']
            status = form.cleaned_data['status']
            aspiration = form.cleaned_data['aspiration']

            try:
                academic_data = AcademicData.objects.create(member=member, level=level, status=status,
                                                            aspiration=aspiration)
                academic_data.save()
                messages.success(request, 'Datos académicos registrados exitosamente.')
                return redirect('view_member', member_id, member.get_full_name())
            except IntegrityError:
                messages.error(request, 'Este miembro ya posee datos registrados.')
                return redirect('view_member', member_id, member.get_full_name())
        else:
            data['form'] = form
            messages.error(request, 'Ocurrió algún error.')

    return render(request, 'academic_data/create_data.html', data)



@login_required
@permission_required('Members.change_member')
def edit_member(request, member_id, *args, **kwargs):
    member = Member.objects.get(id=member_id)
    birth_date = member.get_birth_date()

    data = {
        'form': CreateMemberForm(instance=member),
        'member': member,
        'signal': 'info_member',
        'title': 'Información de'
    }

    if request.method == 'POST':
        form = CreateMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            print('valid 2')
            picture_profile = form.cleaned_data['picture_profile']
            birth_date = form.cleaned_data['birth_date']
            form.save()
            messages.success(request, 'Información actualizada exitosamente.')
            return redirect('view_member', member_id, member.get_full_name())
        else:
            data['form'] = form
            messages.error(request, 'Ocurrió algún error.')

    return render(request, 'common/edit_data_member.html', data)


@login_required
@permission_required('Members.change_medicaldata')
def edit_medical_data(request, member_id, *args, **kwargs):
    member = Member.objects.get(id=member_id)

    data = {
        'member': member,
        'form': MedicalDataForm(instance=member.medicaldata),
        'signal': 'medical_data',
        'title': 'Datos médicos de'
    }

    if request.method == 'POST':
        form = MedicalDataForm(request.POST, request.FILES, instance=member.medicaldata)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información actualizada exitosamente.')
            return redirect('view_member', member_id, member.get_full_name())
        else:
            data['form'] = form
            messages.error(request, 'Ocurrió algún error.')

    return render(request, 'common/edit_data_member.html', data)


@login_required
@permission_required('Members.change_academicdata')
def edit_academic_data(request, member_id, *args, **kwargs):
    member = Member.objects.get(id=member_id)

    data = {
        'member': member,
        'form': AcademicDataForm(instance=member.academicdata),
        'signal': 'academic_data',
        'title': 'Datos académicos de'
    }

    if request.method == 'POST':
        form = AcademicDataForm(request.POST, request.FILES, instance=member.academicdata)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información actualizada exitosamente.')
            return redirect('view_member', member_id, member.get_full_name())
        else:
            data['form'] = form
            messages.error(request, 'Ocurrió algún error.')

    return render(request, 'common/edit_data_member.html', data)
