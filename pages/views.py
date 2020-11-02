from django.shortcuts import render

def about(request):
   index = True
   about = True
   return render(request, 'pages/about.html', locals())

def index(request):
   index=True
   return render(request, 'pages/index.html', locals())

def lk(request):

   return render(request, 'pages/lk.html', locals())
