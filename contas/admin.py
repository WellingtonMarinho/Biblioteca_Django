from django.contrib import admin
from .models import Categoria, Livro


class LivroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'editora',
                    'estante', 'prateleira', 'mostrar')
    list_display_links = ('id', 'titulo', 'autor')
    list_filter = ('estante', 'prateleira')
    list_per_page = 10
    search_fields = ('titulo', 'autor')
    list_editable = ('mostrar',)


admin.site.register(Categoria)
admin.site.register(Livro, LivroAdmin)

