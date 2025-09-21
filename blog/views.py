from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.core.mail import mail_admins
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from blog.forms import messageForm
from .models import Projet, Image, temoignage
from django.core.mail import send_mail
from django.contrib import messages
import json
from django.conf import settings

# Create your views here.
@require_POST
@csrf_exempt  # ⚠️ si tu utilises fetch avec CSRF token, tu peux enlever ce décorateur
def ajouter_temoignage(request):
    prenom = request.POST.get("prenom")
    profession = request.POST.get("profession")
    commentaire = request.POST.get("commentaire")

    if prenom and profession and commentaire:
        temoigne = temoignage.objects.create(
            prenom=prenom,
            profession=profession,
            commentaire=commentaire,
            aprouver=False  # par défaut
        )
        return JsonResponse({"success": True, "message": "Merci ! Votre témoignage a été soumis."})
    else:
        return JsonResponse({"success": False, "message": "Veuillez remplir tous les champs."})


def envoyer_message(request):
    if request.method == "POST":
        form = messageForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data["nom"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # Contenu du mail
            subject = f"Nouveau message de {nom}"
            body = f"""
Vous avez reçu un nouveau message via le site Civic Niger :

Nom : {nom}
Email : {email}

Message :
{message}
"""
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    ["omardodosouley@gmail.com"],
                    fail_silently=False,
                )
                return JsonResponse({"success": True, "message": "Message envoyé avec succès à l'administrateur ✅"})
            except Exception as e:
                return JsonResponse({"success": False, "errors": str(e)})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = messageForm()
    return render(request, "message_form.html", {"form": form})

def index(request):
        
        MessageF = messageForm()
        mesTemoignages = temoignage.objects.filter(aprouver=True).order_by('-id')[:5]
        mesProjets = Projet.objects.order_by('date')[:6]

        carousel_items = [
            {'image': 'robotique.jpg', 'titre': 'Robotique'},
            {'image': 'ia.jpg', 'titre': 'Intelligence Artificielle'},
            {'image': 'donnee.jpg', 'titre': 'Données numériques'},
            {'image': 'nature.jpg', 'titre': 'Technologie futuriste'},
            {'image': 'stocker.jpg', 'titre': 'Stockage'},
            {'image': 'demain0.jpg', 'titre': 'Demain'},
            {'image': 'arch.jpg', 'titre': 'Architecture'},
        ]

        context = {
            'mesTemoignages': mesTemoignages,
            'mesProjets' : mesProjets,
            'carousel_items' : carousel_items,
            'MessageF' : MessageF,
        }
        return render(request, 'blog/index.html', context)


def portfolio(request):
    mesProjets = Projet.objects.all()
    MessageF = messageForm()
    context = { 'mesProjets' : mesProjets,
                'MessageF' : MessageF,
                }

    template = loader.get_template('blog/portfolio.html')
    return HttpResponse(template.render(context, request))


def plus(request, slug):
    MonProjet = get_object_or_404(Projet, slug=slug)
    MessageF = messageForm()
    
    image_url = None
    if MonProjet.photo:
        image_url = request.build_absolute_uri(MonProjet.photo.url)

    context = { 'MonProjet' : MonProjet,
                'MessageF' : MessageF,
                "og_image_url": image_url,
                }

    template = loader.get_template('blog/plus.html')
    return HttpResponse(template.render(context, request))


def confident(request):
    template = loader.get_template('blog/confident.html')
    return HttpResponse(template.render())


@csrf_exempt
def envoyer_devis(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        organisation_type = request.POST.get('organisation_type')
        type_projet = request.POST.get('type_projet')
        email = request.POST.get('email')
        numero = request.POST.get('numero')
        delais = request.POST.get('delais')
        description = request.POST.get('description')

        message = f"""
        Nom: {nom}
        Organisation: {organisation_type}
        Type de projet: {type_projet}
        Email: {email}
        Numéro: {numero}
        Délais: {delais}
        Description: {description}
        """

        send_mail(
            subject=f"Nouvelle demande de devis de {nom}",
            message=message,
            from_email='omardodosouley@gmail.com',
            recipient_list=['omardodosouley@gmail.com'],
            fail_silently=False,
        )

        return JsonResponse({'status':'success'})

    return JsonResponse({'status':'fail'})


def client_page_not_found(request, exception):
    return render(request, "404.html", status=404)