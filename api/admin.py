from django.contrib import admin

# from api.models import RazorpayPayment,BookedSeat, Movie, UpcomingMovie, User

from api.models import User,Train,BookedSeat,Booking
# # Register your models here.
# admin.site.register(Movie)
# admin.site.register(UpcomingMovie)
admin.site.register(User)
admin.site.register(Train)
admin.site.register(BookedSeat)
admin.site.register(Booking)
# admin.site.register(BookedSeat)
# admin.site.register(RazorpayPayment)