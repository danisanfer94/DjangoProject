from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from pymongo import MongoClient
from . import models
from . import monguito


# Create your views here.

def index(request):
    mongui=monguito.Monguito()

    if 'error' in request.session:
        del request.session['error']

    if request.method == "POST":
        usuari = request.POST
        if request.POST['submit']=='Entra':
            if mongui.userExists(request.POST['username']):
                user = models.User(usuari['username'],usuari['password'])
                nombre=user.username
                passw=user.password
                if mongui.checkPass(nombre,passw):
                    mongui.incLogin(nombre)
                    request.session['user'] = nombre
                    return render(request , 'mongo/welcome.html',{'ok':nombre})
                else:
                    mongui.fail(usuari['username'],usuari['password'])
                    request.session['error']="Contraseña Incorrecta"
                    return redirect('/login/')
            else:
                mongui.fail(usuari['username'],usuari['password'])
                request.session['error']="El Usuari no Existeix"
                return redirect('/login/')


        elif request.POST['submit'] == "Registra'm" :
            pass1 = usuari.get('password','')
            pass2 = usuari.get('password2','')
            if pass1 == pass2 :

                if not mongui.userExists(usuari['username']) :
                    hash=mongui.hashPass(pass1)
                    user = models.User(usuari['username'],hash)
                    mongui.insertUser(user)
                    request.session['estat']="Registrat correctament siusplau Loguejat"
                    return redirect('/login/')
                else:
                    request.session['error']="El nom d'usuari no esta disponible"
                    return redirect('/registre/')
            else:
                request.session['error']="Les contraseñas no coincideixen"
                return  redirect('/registre/')

        elif request.POST['submit'] == "Eliminar usuari":
            nom = request.session['user']
            del request.session['user']
            mongui.delUser(nom)
            return redirect('/login/')

        elif request.POST['submit'] == "Tancar Sessió":
            del request.session['user']
            return redirect('/login/')


    elif 'user' in request.session:
        nombre = request.session['user']
        return render(request , 'mongo/welcome.html',{'ok':nombre})

    else:
        return  redirect('/login/')



def registre(request):
    patata=""
    if 'error' in request.session:
        patata=request.session['error']
        del request.session['error']
    return render(request , 'mongo/registre.html',{'ok':patata})


def login(request):
    patata=""
    pastanaga=""
    if 'estat' in request.session:
        patata=request.session['estat']
        del request.session['estat']
        pastanaga=True
    elif 'error' in request.session:
        patata=request.session['error']
        del request.session['error']
        pastanaga=False
    return render(request , 'mongo/login.html',{'ok':patata,'check':pastanaga})

def admin(request):
    if 'user' in request.session:
        if request.session['user']=='admin':
            mongui=monguito.Monguito()
            param=""
            if request.method == "POST":
                if request.POST['submit']=="Mostrar usuaris":
                    param="users"
                    usuaris=mongui.mostrarUsers()
                    return render(request , 'mongo/admin.html',{'param':param,'ok':usuaris})
                elif request.POST['submit']=="Mostrar fails":
                    param="fails"
                    fails=[]
                    for i in mongui.findFails():
                        fails.append(i)
                    return render(request , 'mongo/admin.html',{'param':param,'ok':fails,'len':len(fails)})
                elif request.POST['submit']=="Eliminar fails":
                    param="dropfails"
                    mongui.dropFails()
                    return render(request , 'mongo/admin.html',{'param':param,'ok':"S'ha eliminat el registre de fails"})

            else:
                return render(request , 'mongo/admin.html',{'param':param,'ok':""})
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')
