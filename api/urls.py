from django.urls import path
from .views import signupView,loginView,testView,addTrainView,getTrainView,bookSeatView,getBookingView

urlpatterns = [
    path('login',loginView.as_view()),
    path('signup',signupView.as_view()),
    path('test',testView.as_view()),
    path('trains/create',addTrainView.as_view()),
    path('trains/availability',getTrainView.as_view()),
    path('trains/<str:pk>/book',bookSeatView.as_view()),
    path('bookings/<str:pk>',getBookingView.as_view()),
]