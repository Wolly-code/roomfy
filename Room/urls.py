from django.urls import path, include
from . import views
urlpatterns = [
    # Room
    path('viewall', views.RoomList.as_view()),
    path('single', views.SingleRoomView.as_view()),
    path('<int:pk>', views.RoomRetriveDestroy.as_view()),
    path('<int:pk>/report', views.ReportCreate.as_view()),
    path('booking', views.BookingList.as_view(), name='BookingList'),
    # path('booking/<int:pk>', views.BookingRetrieveDelete.as_view(),
    #      name='Booking_delete'),
    path('fav/', views.Fav.as_view()),
    path('getFav/',views.FavView.as_view())


]
