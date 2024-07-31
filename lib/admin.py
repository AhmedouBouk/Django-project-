from django.contrib import admin
from .models import Library, Livre
from django.contrib.auth.hashers import make_password

# Action to activate libraries
def activer_libraries(modeladmin, request, queryset):
    queryset.update(champ_activation=True)
activer_libraries.short_description = "Activer les librairies sélectionnées"

# Action to deactivate libraries
def desactiver_libraries(modeladmin, request, queryset):
    queryset.update(champ_activation=False)
desactiver_libraries.short_description = "Désactiver les librairies sélectionnées"

class LibraryAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name_lib', 'phone_number', 'champ_activation', 'latitude', 'longitude', 'date_joined', 'last_login')
    list_filter = ('champ_activation', 'is_active', 'is_staff', 'date_joined', 'last_login')
    search_fields = ('username', 'email', 'name_lib')
    actions = [activer_libraries, desactiver_libraries]  # Add the actions here
    def save_model(self, request, obj, form, change):
        if change:
            if 'password' in form.changed_data:
                obj.password = make_password(obj.password)
        else:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(Library, LibraryAdmin)

class LivreAdmin(admin.ModelAdmin):
    list_display = ('Name_book', 'Authour_name', 'Genre', 'Stock', 'Id_lib', 'Prix')
    list_filter = ('Genre', 'Id_lib')
    search_fields = ('Name_book', 'Authour_name')

admin.site.register(Livre, LivreAdmin)
