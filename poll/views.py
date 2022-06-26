from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group
# Create your views here.
from .models import Choice, Question
from .forms import ChoiceForm

def savollar(request):
    savollar = Question.objects.all()
    return render(
        request, 'questions/savollar.html', {'savollar':savollar})

def savol_detail(request, id):
    # bu yerda Question modelidan id si parameterda kelayotgan
    # variant_id ga teng bo'lgan object olinnadi
    savol = get_object_or_404(Question, id=id)
    return render(request, 'questions/savol.html', {"savol": savol})

def check_answer(request, variant_id):
    # bu yerda Choice modelidan id si parameterda kelyotgan
    # variant_id ga teng bo'lgan object olinnadi
    javob = get_object_or_404(Choice, id=variant_id)
    correct = javob.is_correct
    return render(request, "questions/checked.html", {'correct': correct})


def create_question(request):
    if request.method == "POST":
        question = request.POST.get('question')
        Question.objects.create(question=question)
        return redirect('poll:savollar')
        # print(request.POST)
    return render(request, 'questions/create_question.html')


def create_group(request):
    if request.method == "POST":
        name = request.POST.get('name')
        Group.objects.create(name=name)
        messages.add_message(request, level=messages.SUCCESS, message=f"Guruh [ {name} ] muvoffaqiyatli qo'shildi!")
        return redirect('poll:groups')

    return render(request, 'questions/group_form.html')


def groups(request):
    gruppalar = Group.objects.all()
    return render(request, 'questions/groups.html', {'gruppalar': gruppalar})


def remove_group(request, id):
    # bu yerda Question modelidan id si parameterda kelayotgan
    # variant_id ga teng bo'lgan object olinnadi
    group = get_object_or_404(Group, id=id)
    name = group.name
    group.delete()
    messages.add_message(request, level=messages.WARNING, message=f"Guruh [ {name} ] muvoffaqiyatli o'chirildi!")
    return redirect("poll:groups")


def edit_group(request, id):
    group = get_object_or_404(Group, id=id)
    if request.method == "POST":
        name = request.POST.get('name')
        group.name = name
        group.save()
        messages.add_message(request, level=messages.SUCCESS, message=f"Guruh [ {name} ] muvoffaqiyatli o'zgartirildi!")
        return redirect("poll:groups")

    return render(request, 'questions/group_form.html', {'name': group.name})


def create_variant(request, id):
    savol = get_object_or_404(Question, id=id)
    if request.method == "POST":
        choice = Choice.objects.create(name=name) # reqeust.post dan name oling
        choice.question = savol
        choice.save()

        return redirect("poll:savol", args=[id])
    return render(request, 'questions/create_choice.html', {'savol_id': savol.id})



def create_choice(request):
    form = ChoiceForm()
    if request.method == "POST":
        form = ChoiceForm(data=request.POST)
        if form.is_valid():
            choice = form.save()
            return redirect("poll:savollar")
    return render(request, 'questions/create_choice.html', {"form": form})

