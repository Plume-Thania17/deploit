from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Inscription
from .forms import InscriptionForm

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            nouveau_inscription = form.save()
            # Stocker l'ID dans la session
            request.session['derniere_inscription_id'] = nouveau_inscription.id
            return redirect(reverse('felicitation'))
    else:
        form = InscriptionForm()

    context = {'form': form}
    return render(request, 'inscription.html', context)

def felicitation(request):
    inscription_id = request.session.get('derniere_inscription_id')
    
    if inscription_id:
        try:
            inscription = Inscription.objects.get(id=inscription_id)
        except Inscription.DoesNotExist:
            return redirect('accueil')
    else:
        return redirect('accueil')

    context = {'inscription': inscription}
    return render(request, 'felicitation.html', context)

def accueil(request):
    return render(request, 'accueil.html')