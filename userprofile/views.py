from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import SignUpForm



def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user) # biz yaratgan userni login qiladi
            messages.success(request, 'Tizimga muvoffaqiytli kirdingiz!')
            return redirect('poll:savollar')
    return render(request, 'userprofile/register.html', {'form': SignUpForm()})
