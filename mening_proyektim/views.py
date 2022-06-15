# from tokenize import group
# from unittest import removeResult

from django.shortcuts import HttpResponse, render
from django.contrib.auth.models import User, Group

# from django.core.urlresolvers import reverse
# from django.views.generic.edit import CreateView

 
def users_view(request):
    # return HttpResponse("Salom bollar")
    users = User.objects.all()
    return render(request, 'users.html', {"users": users})

def groups_view(request):
    # return HttpResponse("hello world")
    groups =Group.objects.all()
    return render(request,'groups.html',{"groups":groups})



#--------------------------------------------------------

# from email.headerregistry import Group
# from django.shortcuts import HttpResponse, render
# # django user modelini  import qildim 
# from django.contrib.auth.models import User
# from django.contrib.auth.models import Group


# def users_view(request):
#     # return HttpResponse("hello world")
#     users =User.objects.all()
#     return render(request,'users.html',{"users":users})




   

