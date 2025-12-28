from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth & Users first
    path("api/v1/", include("apps.users.urls")),

    # Product & category APIs
    path("api/v1/", include("apps.products.urls")),
 


    # Cart
    path("api/v1/", include("apps.cart.urls")),
    path("api/v1/", include("apps.orders.urls")),


    # Swagger docs
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema")),

    path("accounts/", include("allauth.urls")),
    
]
urlpatterns += [
    path("oauth/", include("social_django.urls", namespace="social")),
]

