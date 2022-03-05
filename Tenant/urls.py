from unicodedata import name
from django.urls import path, include
from .views import TenantList, TenantRetrieveDestroy,TenantReportCreate,ViewAllReport
urlpatterns = [
    # tenant
    path('viewall', TenantList.as_view()),
    path('<int:pk>', TenantRetrieveDestroy.as_view()),
    path('<int:pk>/report', TenantReportCreate.as_view()),
    path('reports',ViewAllReport.as_view()),
]
