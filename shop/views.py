from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

# Create your views here.
from shop.models import Category, Product, Article
from shop.serializers import CategoryListSerializer, CategoryDetailSerializer, ProductListSerializer, ProductDetailSerializer, ArticleSerializer


#Mixin pour obtenir le serializer de details pour chaque classe.
class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
    

class CategoryViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
    
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)


class ProductViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
    
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer

    
    def get_queryset(self):
        return Product.objects.filter(active=True)

