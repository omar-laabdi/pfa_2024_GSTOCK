from django.shortcuts import render, redirect
from blog.models import Article
from django.http.response import HttpResponseRedirect


def caisse(request):
    list_article = {}
    list_key = {}

    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        qty = int(request.POST.get('qty'))

        try:
            article = Article.objects.get(barcode=barcode)
            if 'listkey' in request.session:
                list_key = request.session.get('listkey')

            if str(article.barcode) in list_key:
                list_key[str(article.barcode)] += qty
            else:
                list_key[str(article.barcode)] = qty


            request.session['listkey'] = list_key
        except Article.DoesNotExist:
            # Handle the case when the article doesn't exist
            pass

    if 'listkey' not in request.session:
        request.session['listkey'] = list_key
    else:
        list_key = request.session['listkey']

    try:
        for key, value in list_key.items():
            article = Article.objects.get(barcode=int(key))
            list_article[article.barcode] = [article, value]
    except Article.DoesNotExist:
        # Handle the case when the article doesn't exist
        pass

    return render(request, 'caisse/caisse.html', {'listarticles': list_article, 'listkeys': list_key})

def paiement(request):
    list_key = request.session['listkey']
    request.session['listkey'] = {}
    
    for key, value in list_key.items():
        article : Article() = Article.objects.get(barcode=int(key))
        article.stock -= value
        article.save()
        
    return redirect('caisse')


def retour(request):
    if request.POST:
        #codebar = 0 
        #nbrarticle = 0
        
        codebar = request.POST.get('barcode')
        nbrarticle = request.POST.get('nbr')
        
        article : Article() = Article.objects.get(barcode=int(codebar))
        article.stock += int(nbrarticle)
        article.save()
        return redirect('caisse')
    return render(request, 'caisse/retour.html', {})

def delete_all_articles(request, barcode):
    list_key = request.session.get('listkey', {})
    if barcode in list_key:
       del list_key[barcode] 

    request.session['listkey'] = list_key
    return HttpResponseRedirect('/caisse')






def delete_article(request, article_id):
    list_key = request.session['listkey']
    article = Article.objects.get(id=article_id)
    barcode = str(article.barcode)
    
    if barcode in list_key:
        if list_key[barcode] > 1:
            list_key[barcode] -= 1
        else:
             list_key[barcode] = 0
    
    request.session['listkey'] = list_key
    return HttpResponseRedirect('/caisse')