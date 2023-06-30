from django.db import models

DEFAULT_ID = 1


class Provider(models.Model):
    name = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    address = models.TextField()
    zip_code = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    address = models.TextField()
    zip_code = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=500, default="")
    price = models.FloatField()
    barcode = models.IntegerField()
    quantite = models.IntegerField(default=0)
    provider = models.ForeignKey(
        "Provider", on_delete=models.CASCADE, default=DEFAULT_ID
    )

    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    name = models.CharField(default=article.name, max_length=500)
    stock = models.IntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Commande(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    quantite = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return self.article.name


class HistCommande(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    quantite = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return f"HistCommande object (id: {self.id})"
