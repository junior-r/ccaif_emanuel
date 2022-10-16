from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from Users.forms import SignupForm
from django.contrib import messages


@permission_required('Users.add_user')
def sign_up(request):
    data = {
        'form': SignupForm()
    }

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            # login(user)

            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('homepage')
        else:
            messages.error(request, 'Algún dato es inválido. Intente de nuevo!')
            data['form'] = form

    return render(request, 'registration/signup.html', data)
