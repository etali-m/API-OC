from rest_framework import serializers
from .models import Category, Product, Article

#serializer pour afficher la liste des catégories
class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Le prix ne peut pas être négatif')
        return value

    def validate_name(self, value):
        if Article.objects.filter(name=value).exists():
            raise serializers.ValidationError('Le nom de l\'article existe déjà')
        return value

    def validate_product(self, value):
        if value.active is False:
            raise serializers.ValidationError('Le produit est désactivé')
        return value

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

    #fonction pour valider le nom
    def validate_name(self, value):
        #verifier que la categorie n'existe pas encore
        if Category.objects.filter(name=value).exists():
            # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError('La catégorie existe déja')
        return value

    def validate(self, data):
        #verifier que le nom apprait dans la description de la catégorie
        if data['name'] not in data['description']:
            raise serializers.ValidationError('Le nom doit appaitre dans la description')
        return data


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