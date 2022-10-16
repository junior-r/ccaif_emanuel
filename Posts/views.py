from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from Posts.models import Event, EventParticipant
from Posts.forms import EventForm, EventParticipantForm
from Users.models import User
from Members.models import Member
from datetime import date


def events(request):
    events = Event.objects.filter(active=True)

    for event in events:
        print(date.today() > event.date)
        if date.today() > event.date:
            event.active = False
            event.save()

    data = {
        'events': events
    }

    return render(request, 'Events/events.html', data)


@login_required
@permission_required('Events.add_event')
def create_event(request, user_id):
    user = User.objects.get(id=user_id)
    data = {
        'form': EventForm()
    }

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            place = form.cleaned_data['place']
            date = form.cleaned_data['date']
            form_event = form.cleaned_data['form']
            max_part = form.cleaned_data['max_num_partp']

            regist_event = Event.objects.create(user=user, image=image, title=title, description=description, place=place, date=date, form=form_event, max_num_partp=max_part)
            regist_event.save()
            messages.success(request, 'Evento registrado exitosamente.')
            return redirect('create_event', user_id)
        else:
            data['form'] = form

            messages.error(request, f'Ocurrió un error. Revise la información e intente de nuevo.')

    return render(request, 'Events/create_event.html', data)


def register_form_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if not event.active:
        messages.info(request, 'Este evento ya no está disponible.')
        return redirect('events')

    participants = EventParticipant.objects.filter(event=event).order_by('-created_at')
    num_participants = participants.count()

    for part in participants:
        member = Member.objects.filter(first_name__iexact=part.first_name, last_name__iexact=part.last_name, birth_date=part.birth_date).exists()
        if member:
            part.is_member = True
            part.save()

    data = {
        'event': event,
        'form': EventParticipantForm(),
        'rest': event.max_num_partp - num_participants,
        'participants': participants
    }

    if request.method == 'POST':
        form = EventParticipantForm(request.POST, request.FILES)

        if num_participants >= event.max_num_partp:
            event.active = False
            event.save()
            messages.info(request, 'Este evento está al máximo, contactanos para mayor información')
            return redirect('events')

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            birth_date = form.cleaned_data['birth_date']
            is_member = form.cleaned_data['is_member']

            if EventParticipant.objects.filter(first_name__iexact=first_name, last_name__iexact=last_name, birth_date=birth_date, event=event).exists():
                messages.error(request, 'Ya estas registrado(a)')
                return redirect('register_event', event_id)

            participant = EventParticipant.objects.create(first_name=first_name, last_name=last_name, birth_date=birth_date, is_member=is_member)
            participant.save()
            participant.event.add(event)
            messages.success(request, 'Fuiste registrado exitosamente.')
            return redirect('events')
        else:
            data['form'] = form
            messages.error(request, f'Ocurrió un error.')

    return render(request, 'Events/form_event.html', data)
