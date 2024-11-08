from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shop.views import CategoryViewset, ProductViewset, ArticleViewset, AdminCategoryViewset, AdminArticleViewset

# Configuration du routeur principal
router = routers.SimpleRouter()
router.register('categories', CategoryViewset, basename='category')
router.register('products', ProductViewset, basename='product')
router.register('admin/categories', AdminCategoryViewset, basename='admin-category')
router.register('admin/articles', AdminArticleViewset, basename='admin-article')

# Routeur imbriqué pour les articles sous les produits
product_article_router = nested_routers.NestedSimpleRouter(router, 'products', lookup='product')
product_article_router.register('articles', ArticleViewset, basename='product-article')

# Définition des URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/', include(product_article_router.urls)),
]
