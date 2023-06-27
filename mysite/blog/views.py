from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from blog.models import Provider, Article, Client, Stock
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import F


def home(request):
    return redirect("login")


def login(request):
    return render(request, "blog/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def provider(request):
    list_provider = Provider.objects.all().order_by("-name")
    return render(request, "blog/provider.html", {"listprovider": list_provider})


def client(request):
    list_client = Client.objects.all().order_by("-name")
    return render(request, "blog/client.html", {"listclient": list_client})


def article(request):
    listarticle = Article.objects.all().order_by("-name")
    return render(request, "blog/article.html", {"listarticle": listarticle})


def stock(request):
    stock_list = Stock.objects.all()
    return render(request, "blog/stock.html", {"stock_list": stock_list})


def edit_provider(request, provide_id):
    current_provider = Provider.objects.get(id=provide_id)
    if request.POST:
        if request.POST.get("name") != "":
            current_provider.name = request.POST.get("name")
        if request.POST.get("address") != "":
            current_provider.address = request.POST.get("address")
        if request.POST.get("zip_code") != "":
            current_provider.zip_code = request.POST.get("zip_code")
        if request.POST.get("phone") != "":
            current_provider.phone = request.POST.get("phone")

        current_provider.save()
        return HttpResponseRedirect("/provider")
    else:
        return render(
            request, "blog/edit_provider.html", {"provider": current_provider}
        )


def edit_client(request, client_id):
    current_client = Client.objects.get(id=client_id)
    if request.POST:
        if request.POST.get("name") != "":
            current_client.name = request.POST.get("name")
        if request.POST.get("address") != "":
            current_client.address = request.POST.get("address")
        if request.POST.get("zip_code") != "":
            current_client.zip_code = request.POST.get("zip_code")
        if request.POST.get("phone") != "":
            current_client.phone = request.POST.get("phone")

        current_client.save()
        return HttpResponseRedirect("/client")
    else:
        return render(request, "blog/edit_client.html", {"client": current_client})


def new_provider(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")

        if not name or not address or not zip_code or not phone:
            messages.error(request, "Please fill in all fields.")
            return redirect("new_provider")

        # Check if a client with the same information already exists
        if Provider.objects.filter(
            name=name, address=address, zip_code=zip_code, phone=phone
        ).exists():
            messages.error(
                request, "A Provider with the same information already exists."
            )
            return redirect(
                "new_provider"
            )  # Redirect to the new_client page with error message
        elif Provider.objects.filter(phone=phone).exists():
            messages.error(
                request, "A Provider with the same phone number already exists."
            )
            return redirect("new_provider")
        elif Provider.objects.filter(name=name).exists():
            messages.error(request, "A Provider with the same name already exists.")
            return redirect("new_provider")
        current_provider = Provider(
            name=name, address=address, zip_code=zip_code, phone=phone
        )
        current_provider.save()
        return redirect(
            "provider"
        )  # Redirect to the clients page after successfully adding the client
    else:
        return render(request, "blog/new_provider.html")


def new_client(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")

        if not name or not address or not zip_code or not phone:
            messages.error(request, "Please fill in all fields.")
            return redirect("new_client")

        # Check if a client with the same information already exists
        if Client.objects.filter(
            name=name, address=address, zip_code=zip_code, phone=phone
        ).exists():
            messages.error(
                request, "A client with the same information already exists."
            )
            return redirect(
                "new_client"
            )  # Redirect to the new_client page with error message
        elif Client.objects.filter(phone=phone).exists():
            messages.error(
                request, "A client with the same phone number already exists."
            )
            return redirect("new_client")
        elif Client.objects.filter(name=name).exists():
            messages.error(request, "A client with the same name already exists.")
            return redirect("new_client")
        current_client = Client(
            name=name, address=address, zip_code=zip_code, phone=phone
        )
        current_client.save()
        return redirect(
            "client"
        )  # Redirect to the clients page after successfully adding the client
    else:
        return render(request, "blog/new_client.html")


def new_article(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        barcode = request.POST.get("barcode")
        quantite = request.POST.get("quantite")
        provider_id = request.POST.get("provider")

        if not name or not price or not barcode or not quantite:
            messages.error(request, "Please fill in all fields.")
            return redirect("new_article")

        # Check if an article with the same barcode already exists
        # elif Article.objects.filter(name=name).exists():
        #     messages.error(request, 'An article with the same name already exists.')
        #     return redirect('new_article')
        elif Article.objects.filter(barcode=barcode).exists():
            messages.error(request, "An article with the same barcode already exists.")
            return redirect("new_article")
        current_article = Article(
            name=name, price=price, barcode=barcode, quantite=quantite
        )
        if provider_id:
            current_article.provider_id = provider_id
        current_article.save()

        if Stock.objects.filter(name=current_article.name).exists():
            stock = Stock.objects.get(name=current_article.name)
            stock.stock = stock.stock + int(current_article.quantite)
            stock.save()
        elif not Stock.objects.filter(name=current_article.name).exists():
            Stock.objects.create(
                article=current_article,
                stock=current_article.quantite,
                name=current_article.name,
            )
        return HttpResponseRedirect("/article")
    else:
        list_provider = Provider.objects.all().order_by("-name")
        return render(
            request, "blog/new_article.html", {"list_provider": list_provider}
        )


def edit_article(request, article_id):
    current_article = Article.objects.get(id=article_id)
    list_provider = Provider.objects.all().order_by("-name")
    if request.POST:
        if request.POST.get("name") != "":
            current_article.name = request.POST.get("name")
        if request.POST.get("price") != "":
            current_article.price = request.POST.get("price")
        if request.POST.get("barcode") != "":
            current_article.barcode = request.POST.get("barcode")
        if request.POST.get("quantite") != "":
            current_article.quantite = request.POST.get("quantite")
        if request.POST.get("provider") != "":
            current_article.provider = Provider.objects.get(
                id=request.POST.get("provider")
            )

        current_article.save()
        return HttpResponseRedirect("/article")
    else:
        return render(
            request,
            "blog/edit_article.html",
            {"article": current_article, "list_provider": list_provider},
        )


def delete_provider(request, provide_id):
    Provider.objects.get(id=provide_id).delete()
    return HttpResponseRedirect("/provider")


def delete_client(request, client_id):
    Client.objects.get(id=client_id).delete()
    return HttpResponseRedirect("/client")


def delete_article(request, article_barcode):
    stock = Stock.objects.get(name=Article.objects.get(barcode=article_barcode))
    article = Article.objects.get(barcode=article_barcode)
    stock.stock = stock.stock - article.quantite
    stock.save()
    Article.objects.get(barcode=article_barcode).delete()
    return HttpResponseRedirect("/article")


def vente(request):
    pass


def paiement(request):
    list_key = request.session["listkey"]
    request.session["listkey"] = {}

    for key, value in list_key.items():
        article: Article() = Article.objects.get(barcode=int(key))
        article.quantite -= value
        article.save()

    return redirect("caisse")


def delete_all_articles(request, barcode):
    list_key = request.session.get("listkey", {})
    if barcode in list_key:
        del list_key[barcode]

    request.session["listkey"] = list_key
    return HttpResponseRedirect("/caisse")


def new_stock(request):
    if request.method == "POST":
        article_id = request.POST.get("article")
        stock_value = request.POST.get("stock")

        if not article_id or not stock_value:
            messages.error(request, "Please fill in all fields.")
            return redirect("new_stock")

        try:
            article = Article.objects.get(id=article_id)
            stock = Stock(article=article, stock=stock_value)
            stock.save()
            return redirect("stock")
        except Article.DoesNotExist:
            messages.error(request, "Article does not exist.")
            return redirect("new_stock")
    else:
        list_article = Article.objects.all().order_by("-name")
        return render(request, "blog/new_stock.html", {"list_article": list_article})
