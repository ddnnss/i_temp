from django.shortcuts import render

def index(request):
   index=True
   return render(request, 'pages/index.html', locals())

def lk(request):

   return render(request, 'pages/lk.html', locals())
