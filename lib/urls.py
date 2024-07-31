from django.urls import include, path
from django.contrib import admin


from Library import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from .views import books_by_library, get_libraries


from . import views

urlpatterns = [
     # Ajout de la route pour l'admin
    path('accounts/', include('django.contrib.auth.urls')),
    path('',views.homecomm, name='homecomm'),


    path('ajouter-un-livre/', views.ajouter_livre, name='ajouter_un_livre'),
    path('home/', views.home, name='home'),
    path('about/', views.about_page,name = 'about'),
    path('api/livres/', views.liste_livres,name = 'Liste des livres'),
    path('api/livres/<str:book_name>/',views.detail_livre, name='detail_livre'),
    path('recherche/', views.recherche, name='recherche'),
    path('n/',views.Signup, name='Signup'),
    path('Signin/',views.Signin, name='Signin'),
    path('Signin/forgot_password/',views.forgotten_password,name='fpassword'),
    path('new_password/<int:idlib>/',views.forgotten_password1,name='newPassword'),
    path('Signup/confirm',views.confirm_library,name='confirm'),
    path('logout/', views.logout_lib, name='logout'),
    path('supprimer-livre/<int:id_livre>/', views.supprimer_livre, name='supprimer_livre'),
    path('modifier-livre/<int:id_livre>/', views.modifier_livre, name='modifier_livre'),
    path('importBook/<int:idlib>/',views.importCSV,name='Importer'),
    path('exportBook/<int:idlib>/',views.exportCSV, name='export'),
    path('lookup/',views.verify , name='verify'),
    path('api/libraries/', get_libraries, name='get_libraries'),
    path('api/libraries/<int:library_id>/books/', books_by_library, name='books_by_library'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)