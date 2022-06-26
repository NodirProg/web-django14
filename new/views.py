from django.shortcuts import redirect, render, get_object_or_404

from .models import New, Comment, Like, Dislike
from .forms import NewForm, NewFormMine, CommentForm


def news_list(request):
    news = New.objects.all().order_by('-created') # quaryset
    # contex dictionary bu templatega berib yuboriladigan o'zgaruvchilar to'plami
    # bu yerda New modelidagi barcha object, yani ikki yoki undan ortiq 
    # objectni oldik
    # bu narsa QUERYSET deyiladi
    # queryset uchun model method ishlamaydi


    # contex dictionery bu temlateda berib yuboriladigan o'zgaruvchilar to'plami 
    contex = {'news': news}
    return render(request, 'new/news_list.html', contex)


def news_detail(request, id):
    new = get_object_or_404(New, id=id)
    form = CommentForm()

    if request.method == "POST":
        # comment formaga postdan kelyotgan malumotlarni
        # berib validatsiyadan o'tgazamiz
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = new
            if request.user.is_authenticated:
                comment.author = request.user
            comment.save()
            # izoh yozganda formada turaverishini yoq qiladi
            return redirect("new:detail", id=id)
    # bitta newni olyapmiz New deganm modelning barcha objectlarini ichidan
    # Shu pnarsa OBJECT deyiladi
    #
    # model metodidlaridan faqat object uchun ishlaydi
    return render(request, 'new/news_detail.html', {'new':new, "form": form})


def create(request):
    form = NewForm()
    if request.method == 'POST':
        # comment formaga postda kelayotgan malumotlarni 
        # berib validatsiyadan o'tkazamiz
        form = NewForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save()
            return redirect("new:list")

    return render(request, 'new/create.html', {"form": form})

def remove(request, id):
    new = get_object_or_404(New, id=id)
    new.delete()
    return redirect("new:list")


def my_news(request):
    news = New.objects.filter(author=request.user).order_by('-created')
    return render(request, 'new/my_news.html', {'news':news})


def my_create(request):
    form = NewFormMine()
    if request.method == 'POST':
        form = NewFormMine(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            new.save()
            return redirect("new:my_news")

    return render(request, 'new/create.html', {"form": form})

def my_update(request, id):
    new = get_object_or_404(New, id=id)
    form = NewFormMine(instance=new)
    if request.method == 'POST':
        form = NewFormMine(request.POST, request.FILES, instance=new)
        if form.is_valid():
            form.save()
            return redirect("new:my_news")

    return render(request, 'new/create.html', {"form": form})   

def my_detail(request, id):
    new = get_object_or_404(New, id=id)
    return render(request, 'new/my_detail.html', {'new': new})

def like(request, id):
    new = get_object_or_404(New, id=id)
    if request.user.is_authenticated:
        if new.likes.filter(user=request.user).exists():
            new.likes.get(user=request.user).delete()
            return JsonResponse({
                "success": True,
                "messages": "Siz reaksiyangizni qaytarib oldingiz!",
                "likes": new.likes.count()
                }
            )

        Like.objects.create(user=request.user, post=new)
        return JsonResponse({
                "success": True,
                "messages": "Sizga yoqgan postlar safiga qo'shildi!",
                "likes": new.likes.count()     
                }
            )
            
    return JsonResponse({
            "success": False,
            "message": "Postga reaksiya bildirish uchun iltimos ro'yxatdan o'ting!",
            }
        )


def dislike(request, id):
    new = get_object_or_404(New, id=id)
    if request.user.is_authenticated:
        if new.dislikes.filter(user=request.user).exists():
            new.dislikes.get(user=request.user).delete()
            return JsonResponse({
                "success": True,
                "messages": "Siz reaksiyangizni qaytarib oldingiz!",
                "dislikes": new.dislikes.count()
                }
            )

        Dislike.objects.create(user=request.user, post=new)
        return JsonResponse({
                "success": True,
                "messages": "Sizga yoqmagan postlar safiga qo'shildi!",
                "dislikes": new.dislikes.count()     
                }
            )
            
    return JsonResponse({
            "success": False,
            "message": "Postga reaksiya bildirish uchun iltimos ro'yxatdan o'ting!",
            }
        )

