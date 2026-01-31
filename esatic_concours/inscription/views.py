from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from .models import Inscription
from .forms import InscriptionForm
from .utils import generer_pdf_recu, generer_pdf_convocation

def accueil(request):
    return render(request, 'accueil.html')

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            nouveau_inscription = form.save()
            
            # Envoyer l'email de confirmation
            try:
                envoi_reussi = envoyer_email_confirmation(nouveau_inscription)
                if envoi_reussi:
                    messages.success(request, "Votre inscription a été enregistrée et un email de confirmation vous a été envoyé.")
                else:
                    messages.warning(request, "Votre inscription a été enregistrée mais l'envoi de l'email a échoué. Vous pouvez télécharger votre convocation sur la page suivante.")
            except Exception as e:
                print(f"Erreur lors de l'envoi de l'email: {e}")
                messages.warning(request, "Votre inscription a été enregistrée mais l'envoi de l'email a échoué. Vous pouvez télécharger votre convocation sur la page suivante.")
            
            # Stocker l'ID dans la session
            request.session['derniere_inscription_id'] = nouveau_inscription.id
            return redirect(reverse('felicitation'))
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
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

def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone', '')
        sujet = request.POST.get('sujet')
        message_text = request.POST.get('message')
        
        try:
            # Envoyer l'email de contact
            email_subject = f"ESATIC Concours - {sujet}"
            email_body = f"""
            Nouveau message de contact:
            
            Nom: {nom}
            Email: {email}
            Téléphone: {telephone}
            Sujet: {sujet}
            
            Message:
            {message_text}
            """
            
            # Vérifier si l'email est configuré
            if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
                email_message = EmailMessage(
                    subject=email_subject,
                    body=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_EMAIL],
                    reply_to=[email]
                )
                email_message.send()
                messages.success(request, "Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.")
            else:
                # Mode console - afficher le message
                print("\n" + "="*80)
                print("EMAIL DE CONTACT")
                print("="*80)
                print(email_body)
                print("="*80 + "\n")
                messages.success(request, "Votre message a été reçu. Nous vous répondrons dans les plus brefs délais.")
            
        except Exception as e:
            messages.error(request, "Une erreur s'est produite lors de l'envoi du message. Veuillez réessayer.")
            print(f"Erreur lors de l'envoi de l'email de contact: {e}")
        
        return redirect('contact')
    
    return render(request, 'contact.html')

def telecharger_recu(request, inscription_id):
    inscription = get_object_or_404(Inscription, id=inscription_id)
    
    try:
        # Générer le PDF du reçu
        pdf_buffer = generer_pdf_recu(inscription)
        
        # Créer la réponse HTTP avec le PDF
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="recu_inscription_{inscription.numero_inscription}.pdf"'
        
        return response
    except Exception as e:
        print(f"Erreur lors de la génération du reçu PDF: {e}")
        messages.error(request, "Une erreur s'est produite lors de la génération du reçu.")
        return redirect('felicitation')

def telecharger_convocation(request, inscription_id):
    inscription = get_object_or_404(Inscription, id=inscription_id)
    
    try:
        # Générer le PDF de la convocation
        pdf_buffer = generer_pdf_convocation(inscription)
        
        # Créer la réponse HTTP avec le PDF
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="convocation_{inscription.numero_inscription}.pdf"'
        
        return response
    except Exception as e:
        print(f"Erreur lors de la génération de la convocation PDF: {e}")
        messages.error(request, "Une erreur s'est produite lors de la génération de la convocation.")
        return redirect('felicitation')

def envoyer_email_confirmation(inscription):
    """Envoie un email de confirmation avec la convocation en pièce jointe"""
    
    try:
        # Préparer le contexte pour l'email
        context = {
            'inscription': inscription,
            'date_concours': '15 août 2025',
            'heure_concours': '08h00',
            'lieu_concours': 'ESATIC, Route de Bingerville, Abidjan'
        }
        
        # Générer le contenu HTML de l'email
        html_message = render_to_string('email_confirmation.html', context)
        
        # Créer l'email
        email = EmailMessage(
            subject=f'Confirmation d\'inscription au concours ESATIC - {inscription.numero_inscription}',
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[inscription.email]
        )
        email.content_subtype = 'html'
        
        # Générer et attacher le PDF de convocation
        try:
            pdf_convocation = generer_pdf_convocation(inscription)
            email.attach(
                f'convocation_{inscription.numero_inscription}.pdf',
                pdf_convocation.getvalue(),
                'application/pdf'
            )
        except Exception as e:
            print(f"Erreur lors de la génération du PDF de convocation: {e}")
            # Continuer sans la pièce jointe si erreur
        
        # Vérifier la configuration email
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
            # Mode console - juste afficher
            print("\n" + "="*80)
            print("EMAIL DE CONFIRMATION")
            print("="*80)
            print(f"To: {inscription.email}")
            print(f"Subject: {email.subject}")
            print("="*80)
            print(html_message[:500] + "...")
            print("="*80 + "\n")
            return True
        else:
            # Envoyer l'email
            email.send()
            return True
            
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email de confirmation: {e}")
        return False