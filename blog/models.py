from django.db import models
from django.utils.text import slugify
from PIL import Image as PilImage
import os
from django.urls import reverse

# Create your models here.



class Projet(models.Model):
    CHOIX = (
        ('design', 'Design'),
        ('dev', 'Développement'),
    )

    libellé = models.CharField(max_length=50)
    pour = models.CharField(max_length=50)
    detail = models.TextField()
    type_pro = models.CharField(choices=CHOIX, max_length=50, default="design")
    photo = models.ImageField(upload_to='projets/')
    date = models.DateTimeField(auto_now=True)
    projet_url = models.URLField(max_length=200, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.libellé
    
    @property
    def photo_webp(self):
        return self.photo.url.rsplit('.', 1)[0] + ".webp"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.libellé)[:150]
            slug = base
            i = 1
            while Projet.objects.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug

        super().save(*args, **kwargs)  # ✅ Toujours exécuter

        if self.photo and os.path.exists(self.photo.path):
            img = PilImage.open(self.photo.path).convert("RGB")
            webp_path = self.photo.path.rsplit('.', 1)[0] + ".webp"
            img.save(webp_path, "webp", quality=85)


class Image(models.Model):
    projet = models.ForeignKey(Projet, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projets_images/')
    description = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(default ="Alt texte", max_length=50)

    @property
    def image_webp(self):
        return self.image.url.rsplit('.', 1)[0] + ".webp"

    def __str__(self):
        return f"Image pour {self.projet.libellé}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image and os.path.exists(self.image.path):
            img = PilImage.open(self.image.path).convert("RGB")
            webp_path = self.image.path.rsplit('.', 1)[0] + ".webp"
            img.save(webp_path, "webp", quality=85)
    

class temoignage(models.Model):
    prenom = models.CharField(max_length=70)
    profession = models.CharField(max_length=50)
    commentaire = models.TextField()
    aprouver = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.prenom} - { 'Aprouver' if self.aprouver else 'Non Aprouver'}"
    


class LettersMails(models.Model):
    mail = models.EmailField(max_length=254)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.mail

class articles(models.Model):
    titreArt = models.CharField("Titre", max_length=150)
    s_titre = models.CharField("Sous-titre", max_length=200)
    slug = models.SlugField(unique=True)
    liste_points = models.TextField("Liste des points", blank=True, help_text="Une ligne par point")
    consernant = models.CharField("Concernant", max_length=100)
    descripArt = models.TextField("Description principale")
    source = models.CharField("Source", max_length=100, blank=True)
    heur = models.DateTimeField("Date de publication", auto_now=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-heur']

    def __str__(self):
        return self.titreArt

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titreArt)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail_article', kwargs={'slug': self.slug})


class ArticleImage(models.Model):
    POSITION_CHOICES = [
        ('haut', 'Haut'),
        ('milieu', 'Milieu'),
        ('bas', 'Bas'),
        ('autre', 'Autre'),
    ]

    article = models.ForeignKey(articles, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='articles/images')
    caption = models.CharField("Légende", max_length=150, blank=True)
    position = models.CharField("Position", max_length=20, choices=POSITION_CHOICES, default='autre')
    ordre = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return f"{self.article.titreArt} - {self.position}"
