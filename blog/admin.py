from django.contrib import admin
from .models import LettersMails, temoignage, Projet, Image, articles, ArticleImage

# Register your models here.

@admin.register(temoignage)
class temoignageAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'profession')
    list_filter = ('aprouver',)
    actions = ['temoignage_aprouver']

    @admin.action(description="Aprouver les temoignage sélectionnées")
    def aprouver_temoignage(self, request, queryset):
        queryset.update(aprouver=True)


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1

@admin.register(articles)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titreArt', 'consernant' , 'heur')
    prepopulated_fields = {'slug': ('titreArt',)}
    inlines = [ArticleImageInline]

tables = [LettersMails, ArticleImage]


# Inline pour gérer les images dans la page d’un projet
class ImageInline(admin.TabularInline):  # ou StackedInline pour plus d’espace
    model = Image
    extra = 1  # nombre de champs vides par défaut
    fields = ('image', 'description', 'alt_text', 'preview')
    readonly_fields = ('preview',)  # pour afficher un aperçu
    show_change_link = True

    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="120" height="80" style="object-fit:cover;border-radius:6px;" />'
        return "(Aucune image)"
    preview.allow_tags = True
    preview.short_description = "Aperçu"

# Admin du projet
@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('libellé', 'type_pro', 'date', 'slug')
    search_fields = ('libellé', 'pour', 'detail')
    list_filter = ('type_pro', 'date')
    prepopulated_fields = {"slug": ("libellé",)}  # slug auto dans admin
    inlines = [ImageInline]  # Ajout inline des images

# Admin des images (optionnel si tu veux aussi les gérer indépendamment)
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('projet', 'description', 'alt_text', 'image_preview')
    search_fields = ('description', 'alt_text', 'Projet__libellé')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="80" height="60" style="object-fit:cover;border-radius:6px;" />'
        return "—"
    image_preview.allow_tags = True
    image_preview.short_description = "Aperçu"



admin.site.register(tables)