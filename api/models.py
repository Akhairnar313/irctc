# from distutils.command.upload import upload
# from email.policy import default
# from this import d
from django.db import models

# class Movie(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='images/')
#     year = models.CharField(max_length=5,blank=True)
#     description = models.TextField(blank=True)
#     time = models.CharField(max_length=20,blank=True)
#     trailer = models.FileField(upload_to='trailers/',null=True)

#     def __str__(self):
#         return self.name

# class UpcomingMovie(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='images/')

#     def __str__(self):
#         return self.name

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    email = models.EmailField(max_length=200,blank=True)
    
    def __str__(self):
        return self.username

class Train(models.Model):
    train_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    seat_capacity = models.IntegerField()
    arrival_time_at_source = models.DateTimeField()
    arrival_time_at_destination = models.DateTimeField()

    def __str__(self):
        return self.train_name

class Booking(models.Model):
    train = models.ForeignKey(Train,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class BookedSeat(models.Model):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
    seat_no = models.IntegerField()

# class Booking(models.Model):
#     booking_id = models.CharField(max_length=100)
#     train_id = models.ForeignKey()
#     train
    # "booking_id": "5432109876",
    # "train_id": "9876543210",
    # "train_name": "Express Train",
    # "user_id": "1234567890",
    # "no_of_seats": 1
    # "seat_numbers": [7],
    # "arrival_time_at_source": "2023-01-01 14:00:00",
    # "arrival_time_at_destination": "2023-01-01 20:30:00" 


# class BookedSeat(models.Model):
#     seat = models.IntegerField()
#     userId = models.IntegerField()
#     movieId = models.IntegerField()

# class RazorpayPayment(models.Model):
#     name = models.CharField(max_length=100)
#     amount = models.IntegerField(default=100)
#     provider_order_id = models.CharField(max_length=100)
 