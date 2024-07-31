import random
from tempfile import NamedTemporaryFile
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password,check_password
from .forms import LivreForm
from .models import Livre, Library
from django.contrib.auth import  login, logout
from django.core.mail import send_mail
from Library import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def verify(request):
    return render(request,"lookup.html" ,{'user':request.session['_auth_user_id']})
# Authentification
def homecomm(request):
    return render(request,"Welcompage.html")


def Signin(request):
    if request.method=='POST':
        username_or_email = request.POST['credential']
        password = request.POST['password']

        library = Library.objects.filter(username = username_or_email).first()

        if library is None:
            library = Library.objects.filter(email=username_or_email).first()

        if library is not None:
            if check_password(password,library.password):
                login(request,library)
                return redirect('home')
            else:
                messages.error(request,"La librairie n'existe pas ou mot de passe incorrect.")
                return redirect('Signin')
        else:
             messages.error(request,"La librairie n'existe pas ou mot de passe incorrect.")
             return redirect('Signin')
    return render(request,'Signin.html')






def supprimer_livre(request, id_livre):
    if request.session['_auth_user_id']!=None:
        livre = get_object_or_404(Livre, Id_livre=id_livre, Id_lib=request.session['_auth_user_id'])
        if request.method == 'POST':
            livre.delete()
            messages.success(request, "Le livre a été supprimé avec succès.")
            return redirect('home')
        return render(request, 'confirmer_suppression.html', {'livre': livre})
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')


def modifier_livre(request, id_livre):
    if request.session['_auth_user_id']!=None:
        livre = get_object_or_404(Livre, Id_livre=id_livre, Id_lib=request.session['_auth_user_id'])
        if request.method == 'POST':
            form = LivreForm(request.POST, request.FILES, instance=livre)
            if form.is_valid():
                form.save()
                messages.success(request, "Le livre a été modifié avec succès.")
                return redirect('home')
            else:
                messages.error(request,"Informations Invalides")
        else:
            form = LivreForm(instance=livre)
            return render(request, 'modifier_livre.html', {'form': form, 'livre': livre})
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')

def ajouter_livre(request):
    if request.session['_auth_user_id']!=None:
        if request.method == 'POST':
            form = LivreForm(request.POST, request.FILES)
            if form.is_valid():
                livre = form.save(commit=False)
                livre.Id_lib =Library.objects.get(id=request.session['_auth_user_id']) 
                livre.save()
                messages.success(request, "Le livre a été ajouté avec succès.")
                return redirect('home')
            else:
                messages.error(request, "Verifier la validité des informations du livre.")
        else:
            form = LivreForm()
            return render(request, 'ajouter un livre.html', {'form': form , 'who':request.session['_auth_user_id']})

def home(request):
    if request.session['_auth_user_id'] !=None:
        idlib =  request.session['_auth_user_id']
        query = request.GET.get('q')
        if query:
            livres = Livre.objects.filter(Id_lib=request.session['_auth_user_id'], Name_book__icontains=query)
        else:
            livres = Livre.objects.filter(Id_lib=request.session['_auth_user_id'])
        return render(request, 'home.html', {'livres': livres, 'query': query, 'idlib':idlib})
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')




def supprimer_livre(request, id_livre):
    if request.session['_auth_user_id']!=None:
        livre = get_object_or_404(Livre, Id_livre=id_livre, Id_lib=request.session['_auth_user_id'])
        if request.method == 'POST':
            livre.delete()
            messages.success(request, "Le livre a été supprimé avec succès.")
            return redirect('home')
        return render(request, 'confirmer_suppression.html', {'livre': livre})
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')



def modifier_livre(request, id_livre):
    if request.session['_auth_user_id']!=None:
        livre = get_object_or_404(Livre, Id_livre=id_livre, Id_lib=request.session['_auth_user_id'])
        if request.method == 'POST':
            form = LivreForm(request.POST, request.FILES, instance=livre)
            if form.is_valid():
                form.save()
                messages.success(request, "Le livre a été modifié avec succès.")
                return redirect('home')
        else:
            form = LivreForm(instance=livre)
            return render(request, 'modifier_livre.html', {'form': form, 'livre': livre})
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')




def about_page(request):
    return render(request, 'about.html')



from django.shortcuts import get_object_or_404

from django.http import JsonResponse
from .models import Livre
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Livre

@require_GET
def liste_livres(request):
    query = request.GET.get('q')
    if query:
        livres = Livre.objects.filter(Name_book__icontains=query, Id_lib__champ_activation=True)
    else:
        livres = Livre.objects.filter(Id_lib__champ_activation=True)

    livres_list = []
    for livre in livres:
        livres_list.append({
            'Id_livre': livre.Id_livre,
            'Name_book': livre.Name_book,
            'Authour_name': livre.Authour_name,
            'Genre': livre.Genre,
            'Image': request.build_absolute_uri(livre.Image.url) if livre.Image else None,
            'Stock': livre.Stock,
            'Description': livre.Description,
            'Id_lib': livre.Id_lib.id,
            'Prix': livre.Prix,
            'library_name': livre.Id_lib.name_lib,
            'status': livre.status,
            'library_PHONE_NUMBER': livre.Id_lib.phone_number,
        })

    return JsonResponse(livres_list, safe=False)

def detail_livre(request, book_name):
    try:
        book = get_object_or_404(Livre, Name_book=book_name)
        book_data = {
            'Id_livre': book.Id_livre,
            'Name_book': book.Name_book,
            'Authour_name': book.Authour_name,
            'Genre': book.Genre,
            'Image': request.build_absolute_uri(book.Image.url) if book.Image else None,
            'Stock': book.Stock,
            'Id_lib': book.Id_lib.id,
            'Prix': book.Prix,
            'library_name': book.Id_lib.name_lib,
            'status':book.status,
        }
        return JsonResponse(book_data, safe=False)
    except Livre.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)






def recherche(request):
    query = request.GET.get('q')
    livres = Livre.objects.all()

    if query:
        livres = livres.filter(Name_book__icontains=query)

    return render(request, 'resultat.html', {'livres': livres, 'query': query})








##Authentication system By 23-50##
signing_up = []
def erase_all():
    global signing_up
    signing_up=[]

    return None


def confirm_library(request):
    if request.method == 'POST':
        code_value = request.POST['code']
        
        # Vérifiez que signing_up contient les éléments nécessaires
        if len(signing_up) < 2:
            messages.error(request, "Erreur de confirmation. Veuillez réessayer.")
            return redirect('Signup')
        
        if str(code_value) == str(signing_up[1]):
            try:
                print(signing_up[0])
                if isinstance(signing_up[0], Library):
                    
                    new_library = signing_up[0]
                   
                    # Save the library instance
                    new_library.save()
                    erase_all()
                    return redirect('Signin')
                
            except Exception as e:
                messages.error(request, "Erreur lors de la sauvegarde de l'utilisateur. Veuillez réessayer.")
                print(e)
                return redirect('Signup')
        else:
            messages.error(request, "Code de confirmation incorrect.")
            return redirect('confirm')
    
    return render(request, 'Confirmer.html')

digits = [0,1,2,3,4,5,6,7,8,9]
alphabet_minuscules = [chr(i) for i in range(ord('a'), ord('z')+1)]
alphabet_maj = [chr(i) for i in range(ord('A'), ord('Z')+1)]

Alphanum_chars = digits + alphabet_minuscules + alphabet_maj

def is_thereDigit(code):
    for i in digits:
        if str(i) in code:
            return True
        else:
            return False


def generator(all_em):
    code=''
    for i in range(6):
        code+=str(random.choice(all_em))
    if is_thereDigit(code) and code.isalnum():
        return code
    else:
        return generator(all_em)



from django.contrib.messages import get_messages
from django.core.files.uploadedfile import InMemoryUploadedFile

def Signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        image = request.FILES.get('image')
        secured_password = make_password(password)

        if Library.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà enregistré")
            return redirect('Signup')

        if Library.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà")
            return redirect('Signup')
       
        if len(username) < 4:
            messages.error(request, "Le nom d'utilisateur est trop court")
            return redirect('Signup')

        if len(password) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères")
            return redirect('Signup')

        if password.isnumeric():
            messages.error(request, 'Le mot de passe doit contenir des chiffres et des lettres')
            return redirect('Signup')
          
        new_library = Library(
            name_lib=name,
            username=username,
            email=email,
            phone_number=phone_number,
            password=secured_password,
        )
      

        code = generator(Alphanum_chars)

        signing_up.append(new_library)
        signing_up.append(password)
        signing_up.append(code)
        print(signing_up[0].phone_number)
        message = f"""Merci de choisir notre plateforme\nNous voudrons vérifier qu'il s'agit bien de vous\nVeuillez entrer le code de confirmation\nvotre code de confirmation est le : {code}"""

        # Send SMS instead of email
        '''
        send_sms(phone_number, message)
        '''
        return redirect('confirm')

    storage = get_messages(request)
    return render(request, 'Signup.html', {'messages': storage})



# views.py
from django.http import JsonResponse
from .utils import send_sms  # Import the send_sms function

def send_sms_view(request):
    to_number = '+1234567890'  # Replace with the recipient's phone number
    message_body = 'Your message here'

    sms_sid = send_sms(to_number, message_body)

    return JsonResponse({'message': 'SMS sent', 'sid': sms_sid})

    
def logout_lib(request):
    if request.session['_auth_user_id']!=None:
        logout(request)
        return redirect('Signin')
    else:
       return HttpResponse("Erreur de deconnexion !")


session =[]
def forgotten_password(request):
    code_recup = ''
    if request.method=='POST':
        email1 = request.POST['email']

        library = Library.objects.filter(email=email1).first()
        if library is not None:
            for k in range(6):
                code_recup+=str(random.choice(digits))

            session.append(code_recup)
            message = f"Vous avez oublié votre mot de passe \n pour le recuperer veuillez entrez le code de recupération suivant \n {code_recup}"
            from_email = settings.EMAIL_HOST_USER
            to_list = [email1]
            subject ="Code de recupération"
            send_mail(subject,message,from_email,to_list,fail_silently=False)
            try:
                url = f'/new_password/{library.id}'
                return redirect(url)
            except Exception as e:
                print(e)
    return render(request,'recuperer0.html')
    

def forgotten_password1(request,idlib):
    if request.method=='POST':
        code = request.POST['code']
        password = request.POST['pass1']
        conf_password = request.POST['pass2']
        secured_password = make_password(password)
        library = Library.objects.get(id=idlib)
        url = f'/new_password/{library.id}'

        if len(password)<8:
            messages.error(request,"Le mot de passe doit contenir au moins 8 caractères")
            return redirect(url)

        if str(password).isnumeric():
            messages.error(request,'Le mot de passe doit contenir des chiffres et des lettres')
            return redirect(url)

        if password!=conf_password:
            messages.error(request,"Le mot de passe ne correspond pas au mot de passe de confirmation!")
            return redirect(url)
        if code in session:
            if library is not None:
                library.password = secured_password
                library.save()
                return redirect('Signin')
        else:
                messages.error(request,"Le code de récupération est erroné!")
                return redirect(url)
                
            
    return render(request,'recuperer.html')
    

##Import export ##

def importCSV(request, idlib):
    print("hlaaa")

    if request.session.get('_auth_user_id') is not None:
        if request.method == 'POST' and 'file' in request.FILES:
            csvfile = request.FILES['file']
            lines = csvfile.readlines()
            real_lines = []
            for lin in lines:
                ligne = lin.strip()
                real_lines.append(ligne.decode("UTF-8"))
            
            lib = Library.objects.get(id=idlib)
            
            try:
                if lib is not None:
                    for line in real_lines:
                        bloc = line.split(":")
                        print("hiiiiiiiiiiiiiiiiiiii")
                        
                        # Gérer les champs manquants avec des valeurs par défaut
                        name_book = bloc[1] if len(bloc) > 0 else "Titre non disponible"
                        author_name = bloc[2] if len(bloc) > 1 else "Auteur non disponible"
                        genre = bloc[3] if len(bloc) > 2 else "Genre non disponible"
                        stock = bloc[4] if len(bloc) > 3 and bloc[3].isdigit() else 0
                        prix = bloc[5] if len(bloc) > 4 and bloc[4].replace('.', '', 1).isdigit() else 0.0
                        image = bloc[6] if len(bloc) > 5 else None

                        new_book = Livre(
                            Name_book=name_book,
                            Authour_name=author_name,
                            Genre=genre,
                            Stock=stock,
                            Id_lib=lib,
                            Prix=prix,
                            Image=image,
                        )
                        print(new_book)
                        new_book.save()
                    return redirect('home')
            except Exception as e:
                print(e)
        return render(request, "import.html")
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')



def exportCSV(request,idlib):
    if request.session['_auth_user_id']!=None:
        id=request.session['_auth_user_id']
        print(f"Le id hidden est: {request.session['_auth_user_id']}")
        Livres = Livre.objects.filter(Id_lib=idlib)
        f = open("exported/livres.csv",'w')
        for i in Livres:
            f.write(f"{i.Id_livre}:{i.Name_book}:{i.Authour_name}:{i.Genre}:{i.Stock}:{i.Prix}:{i.Image}"+"\n")
        f.close()

        file = open('exported/livres.csv',"rb")
        return FileResponse(file,
                    as_attachment=True,
                    filename="Livres.csv")
    else:
        messages.error(request, "Vous devez vous connectez.")
        return redirect('Signin')


##Import export ##



from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Library

@require_GET
def get_libraries(request):
    libraries = Library.objects.all()
    library_list = []
    for library in libraries:
        image_url = request.build_absolute_uri(library.image.url) if library.image else None
        library_list.append({
            'id': library.id,
            'name_lib': library.name_lib,
            'email': library.email,
            'phone_number': library.phone_number,
            'latitude': library.latitude,
            'longitude': library.longitude,
            'image': image_url,  # Ensure image URL is fully qualified
        })
    return JsonResponse(library_list, safe=False)

def books_by_library(request, library_id):
    library = get_object_or_404(Library, id=library_id, champ_activation=True)
    books = Livre.objects.filter(Id_lib=library)
    books_list = [{
        'Id_livre': book.Id_livre,
        'Name_book': book.Name_book,
        'Authour_name': book.Authour_name,
        'Genre': book.Genre,
        'Image': request.build_absolute_uri(book.Image.url) if book.Image else None,
        'Stock': book.Stock,
        'Description': book.Description,
        'Prix': book.Prix,
    } for book in books]
    return JsonResponse(books_list, safe=False)






