from unicodedata import name
from django.urls import path, include
from .views import TenantList, TenantRetrieveDestroy, TenantReportCreate, ViewAllReport, TenantAppointment, Fav, FavView
urlpatterns = [
    # tenant
    path('viewall', TenantList.as_view()),
    path('<int:pk>', TenantRetrieveDestroy.as_view()),
    path('<int:pk>/report', TenantReportCreate.as_view()),
    path('reports', ViewAllReport.as_view()),
    path('booking', TenantAppointment.as_view()),
    path('fav/', Fav.as_view()),
    path('getFav/', FavView.as_view()),
]
