from django.shortcuts import render
from .models import store
# sales page
def sales(request):
    context = {
        'sales': store.objects.filter(type_store="sales")
    }
    return render(request, 'store/sales.html', context)
# collaborations page
def collaborations(request):
    context = {
        'collaborations': store.objects.filter(type_store="collaborations")
    }
    return render(request, 'store/collaborations.html', context)