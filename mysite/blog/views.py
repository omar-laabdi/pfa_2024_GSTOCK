from multiprocessing import Value
from os import name
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from blog.models import Commande, HistCommande, Provider, Article, Client, Stock
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import F
from django.db.models import Sum


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


# def stock(request):
#     stock_list = Stock.objects.all()
#     search_query = request.GET.get("search", "")
#     articles = Article.objects.all()
#     context = {
#         "search_query": search_query,
#         "articles": articles,
#         "stock_list": stock_list,
#     }
#     return render(request, "blog/stock.html", context)
def stock(request):
    search = request.GET.get("search", "")
    if search != "":
        stock_list = Stock.objects.filter(name__icontains=search)
    else:
        stock_list = Stock.objects.all()

    context = {
        "search": search,
        "stock_list": stock_list,
    }
    return render(request, "blog/stock.html", context)


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
    try:
        article = Article.objects.get(barcode=article_barcode)
        stock = Stock.objects.get(name=article)
        stock.stock -= article.quantite
        stock.save()
        article.delete()
    except Stock.DoesNotExist:
        pass
    return HttpResponseRedirect("/article")


def delete_stock(request, name):
    Stock.objects.get(name=name).delete()

    try:
        article = Article.objects.get(name=name)
        article.delete()
    except Article.DoesNotExist:
        pass

    return HttpResponseRedirect("/stock")


def vente(request):
    listeArticle = {}
    listkey = {}
    listClient = {}
    create_commande = False

    if request.method == "POST":
        name = request.POST.get("produit")
        quantite = int(request.POST.get("qty"))
        client_id = request.POST.get("client")
        if not name or not quantite or not client_id:
            # One or more required fields are missing
            messages.error(request, "Please fill in all required fields.")
        else:
            try:
                quantite = int(quantite)
                client_id = int(client_id)
                article = Article.objects.get(name=name)
                stock = Stock.objects.get(name=article.name)
                if quantite > stock.stock:
                    messages.error(request, "Depasser quantite dans stock")
                else:
                    if "listkey" in request.session:
                        listkey = request.session.get("listkey")
                        listkey[article.name] = quantite

                    request.session["listkey"] = listkey

                listClient["id"] = client_id

                request.session["listClient"] = listClient

                request.session["listkey"] = listkey

                create_commande = True

            except Article.DoesNotExist:
                messages.error(request, "Article  n'existes pas!!! (1)")

    if "listkey" not in request.session:
        request.session["listkey"] = listkey
    else:
        listkey = request.session["listkey"]

    if "listClient" not in request.session:
        request.session["listClient"] = listClient
    else:
        listClient = request.session["listClient"]

    if create_commande:
        try:
            for key, value in listkey.items():
                article = Article.objects.select_related("provider").get(name=key)
                listeArticle[article.name] = [article, value]
                Commande.objects.create(
                    article=article,
                    client=Client.objects.get(id=listClient["id"]),
                    quantite=value,
                )

        except Article.DoesNotExist:
            messages.error(request, "Article n'existes pas!!! (2)")

    clients = Client.objects.all()

    commandes = Commande.objects.all()

    articles = Article.objects.all()

    context = {
        "clients": clients,
        "commandes": commandes,
        "articles": articles,
        "listarticles": listeArticle,
        "listkey": listkey,
        "listClient": listClient,
    }
    return render(request, "blog/caisse.html", context)


def paiement(request):
    total_quantite = Commande.objects.aggregate(total=Sum("quantite"))["total"]

    commandes = Commande.objects.all()

    for commande in commandes:
        stock = Stock.objects.get(name=commande.article)
        stock.stock -= total_quantite
        stock.save()
        HistCommande.objects.create(
            article=commande.article,
            client=commande.client,
            quantite=commande.quantite,
        )

    Commande.objects.all().delete()
    return redirect("caisse")


def delete_all_articles(request, commande_id):
    Commande.objects.get(id=commande_id).delete()

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


# def historique_commande(request):
#     hist_commandes = HistCommande.objects.all()

#     context = {
#         "hist_commandes": hist_commandes,
#     }


#     return render(request, "blog/historique_commande.html", context)
def historique_commande(request):
    search = request.GET.get("search", "")
    if search != "":
        hist_commandes = HistCommande.objects.filter(article__name__icontains=search)
    else:
        hist_commandes = HistCommande.objects.all()

    context = {
        "search": search,
        "hist_commandes": hist_commandes,
    }
    return render(request, "blog/historique_commande.html", context)
