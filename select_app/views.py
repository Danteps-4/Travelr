from django.shortcuts import render

# Create your views here.
def select(request):
    return render(request, "select/select.html")