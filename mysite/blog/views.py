from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from blog.models import Provider, Article ,Client
from django.contrib.auth.decorators import login_required

def home(request):
    return redirect('login')

def login(request):
    return render(request, 'blog/login.html')

def provider(request):
    list_provider = Provider.objects.all().order_by('-name')
    return render(request, 'blog/provider.html', {'listprovider': list_provider})

def client(request):
    list_client = Client.objects.all().order_by('-name')
    return render(request, 'blog/client.html', {'listclient': list_client})


def article(request):
    list_article = Article.objects.all().order_by('-name')
    return render(request, 'blog/article.html', {'listarticle': list_article})



def edit_provider(request, provide_id):
    current_provider = Provider.objects.get(id=provide_id)
    if request.POST:
        if request.POST.get('name') != "":
            current_provider.name = request.POST.get('name')
        if request.POST.get('address') != "":
            current_provider.address = request.POST.get('address')
        if request.POST.get('zip_code') != "":
            current_provider.zip_code = request.POST.get('zip_code')
        if request.POST.get('phone') != "":
            current_provider.phone = request.POST.get('phone')

        current_provider.save()
        return HttpResponseRedirect("/provider")
    else:
        return render(request, 'blog/edit_provider.html', {'provider': current_provider})
    
def edit_client(request, client_id):
    current_client = Client.objects.get(id=client_id)
    if request.POST:
        if request.POST.get('name') != "":
            current_client.name = request.POST.get('name')
        if request.POST.get('address') != "":
            current_client.address = request.POST.get('address')
        if request.POST.get('zip_code') != "":
            current_client.zip_code = request.POST.get('zip_code')
        if request.POST.get('phone') != "":
            current_client.phone = request.POST.get('phone')

        current_client.save()
        return HttpResponseRedirect("/client")
    else:
        return render(request, 'blog/edit_client.html', {'client': current_client})    


def new_provider(request):
    current_provider = Provider()
    if request.POST:
        if request.POST.get('name') != "":
            current_provider.name = request.POST.get('name')
        if request.POST.get('address') != "":
            current_provider.address = request.POST.get('address')
        if request.POST.get('zip_code') != "":
            current_provider.zip_code = request.POST.get('zip_code')
        if request.POST.get('phone') != "":
            current_provider.phone = request.POST.get('phone')

        current_provider.save()
        return HttpResponseRedirect("/provider")
    else:
        return render(request, 'blog/new_provider.html', {'provider': current_provider})
    
def new_client(request):
    current_client = Client()
    if request.POST:
        if request.POST.get('name') != "":
            current_client.name = request.POST.get('name')
        if request.POST.get('address') != "":
            current_client.address = request.POST.get('address')
        if request.POST.get('zip_code') != "":
            current_client.zip_code = request.POST.get('zip_code')
        if request.POST.get('phone') != "":
            current_client.phone = request.POST.get('phone')

        current_client.save()
        return HttpResponseRedirect("/client")
    else:
        return render(request, 'blog/new_client.html', {'client': current_client})    


def new_article(request):
    current_article = Article()
    list_provider = Provider.objects.all().order_by('-name')
    if request.POST:
        if request.POST.get('name') != "":
            current_article.name = request.POST.get('name')
        if request.POST.get('price') != "":
            current_article.price = request.POST.get('price')
        if request.POST.get('barcode') != "":
            current_article.barcode = request.POST.get('barcode')
        if request.POST.get('stock') != "":
            current_article.stock = request.POST.get('stock')
        if request.POST.get('provider') != "":
            current_article.provider = Provider.objects.get(id=request.POST.get('provider'))

        current_article.save()
        return HttpResponseRedirect("/article")
    else:
        return render(request, 'blog/new_article.html', {'article': current_article, 'list_provider': list_provider})


def edit_article(request, article_id):
    current_article = Article.objects.get(id=article_id)
    list_provider = Provider.objects.all().order_by('-name')
    if request.POST:
        if request.POST.get('name') != "":
            current_article.name = request.POST.get('name')
        if request.POST.get('price') != "":
            current_article.price = request.POST.get('price')
        if request.POST.get('barcode') != "":
            current_article.barcode = request.POST.get('barcode')
        if request.POST.get('stock') != "":
            current_article.stock = request.POST.get('stock')
        if request.POST.get('provider') != "":
            current_article.provider = Provider.objects.get(id=request.POST.get('provider'))

        current_article.save()
        return HttpResponseRedirect("/article")
    else:
        return render(request, 'blog/edit_article.html', {'article': current_article, 'list_provider': list_provider})


def delete_provider(request, provide_id):
    Provider.objects.get(id=provide_id).delete()
    return HttpResponseRedirect("/provider")

def delete_client(request, client_id):
    Client.objects.get(id=client_id).delete()
    return HttpResponseRedirect("/client")


def delete_article(request, article_id):
    Article.objects.get(id=article_id).delete()
    return HttpResponseRedirect("/article")





