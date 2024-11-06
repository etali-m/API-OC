from rest_framework import serializers
from .models import Category, Product, Article

#serializer pour afficher la liste des catégories
class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product']

#serializer pour afficher la liste des products
class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'date_created', 'date_updated']

#Produire les détails d'un produit
class ProductDetailSerializer(serializers.ModelSerializer):

    articles = serializers.SerializerMethodField()
    # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où xxx est le nom de l'attribut, ici 'products'


    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'date_created', 'date_updated', 'articles']

    def get_articles(self, instance):

        query_set = instance.articles.filter(active=True)
        serializer = ArticleSerializer(query_set, many=True)

        return serializer.data

class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'description']

#serializer pour afficher les détails d'une catégorie
class CategoryDetailSerializer(serializers.ModelSerializer):
    
    products = serializers.SerializerMethodField()
    # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où xxx est le nom de l'attribut, ici 'products'

    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated', 'products']

    def get_products(self, instance):

        query_set = instance.products.filter(active=True)   
        serializer = ProductListSerializer(query_set, many=True)

        return serializer.data