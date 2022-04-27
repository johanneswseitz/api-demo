"""apidemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import routers, serializers, viewsets
from fleetmanagement.models import Auto


class AutoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Auto
        fields = ["id", "hersteller", "modell", "nummernschild", "status", "baujahr"]


# ViewSets define the view behavior.
class AutoViewSet(viewsets.ModelViewSet):

    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["hersteller", "modell", "nummernschild", "status", "baujahr"]
    search_fields = ["hersteller", "modell", "nummernschild"]
    @extend_schema(
        summary="Listet alle Fahrzeuge im Flottenmanagement (evtl. nach Kriterien gefiltert).",
          parameters=[
              OpenApiParameter(name='baujahr', description='Filtern nach Baujahr', required=False, type=int,
                               examples=[
                                   OpenApiExample('2011'),
                                   OpenApiExample('2022'),
                               ] ),
              OpenApiParameter(name='hersteller', description='Filtern nach Hersteller', required=False, type=str,
                               examples=[
                                   OpenApiExample('Tesla'),
                                   OpenApiExample('BMW'),
                               ] ),
              OpenApiParameter(name='modell', description='Filtern nach Modell', required=False, type=str,
                               examples=[
                                   OpenApiExample('Model 3'),
                                   OpenApiExample('3 Series')
                               ]),
              OpenApiParameter(name='nummernschild', description='Filtern nach Nummernschild', required=False, type=str,
                               examples=[
                                   OpenApiExample('ME-IQ-213'),
                                   OpenApiExample('B-IA-312')
                               ]),
              OpenApiParameter(name='search', description='Filtern nach Suchbegriff (alle Felder)', required=False, type=str),
              OpenApiParameter(name='status', description='Filtern nach Status des Fahrzeugs (z. B. BESTELLT, FAHRBEREIT, ..)', required=False),
          ],
          description='Listet alle Autos in der Flotte. Optional gefiltert nach bestimmten Kriterien.',
    )
    def list(self, request):
        # your non-standard behaviour
        return super().list(request)

    @extend_schema(
        summary="Fügt ein neues Fahrzeug zur Flotte hinzu.",
        description='Trägt ein neues Fahrzeug in die Datenbank des Flottenmanagements ein. '+
                    '<br>Precondition: Fahrzeughersteller, Modell, Baujahr und Status werden angegeben.' +
        '<br>Postcondition: Das Fahrzeug wird unter einer eindeutigen ID (==Inventarnummer) abgelegt.'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Liefert die Details eines einzelnen Fahrzeugs mit der im Pfad angegebenen ID.",
        parameters=[OpenApiParameter(name="id",description="Inventarnummer des Autos", location='path', required=True)]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Erstellt/Überschreibt ein Auto unter der angegeben ID mit den spezifizierten Attributen.",
        parameters=[OpenApiParameter(name="id",description="Inventarnummer des Autos", location='path', required=True)]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Ändert einzelne Attribute des Autos mit der im Pfad angegeben ID",
        parameters=[OpenApiParameter(name="id",description="Inventarnummer des Autos", location='path', required=True)]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Löscht das Auto mit der im Pfad angegebenen ID",
        parameters=[OpenApiParameter(name="id",description="Inventarnummer des Autos", location='path', required=True)]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)




# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'autos', AutoViewSet)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
