from django.urls import path
from . import views

urlpatterns = [
    path('index_login/', views.login, name='index_login'),
    path('', views.dashboard, name='index_dashboard'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'),
    path('busca/', views.busca, name='busca'),
    path('<int:livro_id>', views.ver_livro, name='ver_livro'),
    path('cadastrar_categoria/', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('sobre/', views.sobre, name='sobre'),
    path('editor/<int:livro_id>', views.editor, name='editor'),
    path('excluir/<int:livro_id>', views.excluir, name='excluir'),
    path('ordenar-por-titulo/', views.ordenar_por_titulo, name='ordenar_por_titulo'),
    path('ordenar-por-autor/', views.ordenar_por_autor, name='ordenar_por_autor'),
    path('ordenar-por-editora/', views.ordenar_por_editora, name='ordenar_por_editora'),
    path('ordenar-por-categoria/', views.ordenar_por_categoria, name='ordenar_por_categoria'),
    path('ordenar-por-estante/', views.ordenar_por_estante, name='ordenar_por_estante'),
    path('ordenar-por-prateleira/', views.ordenar_por_prateleira, name='ordenar_por_prateleira'),

]
