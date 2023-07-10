from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
import jwt
from datetime import datetime,timedelta,timezone
from rest_framework import status
import json
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
import re


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

def query(q):
    with connection.cursor() as c:
        c.execute(q)
        if q[0:6].lower()=="select":
            return dictfetchall(c)
        else :
            return "success"

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class signupView(APIView):
    def post(self,req,format=None):

        print(req.data)
        
        username = req.data['username']
        password = req.data['password']
        
        if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",password) :
            return Response("Password must be atleast 8 characters and contain atleast one small case, upper case, special character and a digit.")
        
        password = make_password(password)
        
        first_name = req.data.get('first_name',"")
        last_name = req.data.get('last_name',"")
        email = req.data.get('email',"")
        
        if  len(query(f"select * from api_user where username='{username}'"))>0:
            return Response("Username already taken")
        result = query(f"insert into api_user (username,password,email,first_name,last_name) values ('{username}','{password}','{email}','{first_name}','{last_name}')")
        id = query(f"select id from api_user where username='{username}'")[0]['id']
        response = {
            "status":"Account Created Sucessfully",
            "status_code":"200",
            "id":id
        }
        return Response(response)

class loginView(APIView) : 
    def post(self,req,format=None):
        response = Response()
        username = req.data['username']
        password = req.data['password']
        preuser = query(f"select * from api_user where username='{username}'")
        if len(preuser)<=0 : 
            return Response({
                "status": "Incorrect username/password provided. Please retry",
                "status_code": 401
                })
        if not check_password(password,preuser[0]['password']) :
            return Response({
                "status": "Incorrect username/password provided. Please retry",
                "status_code": 401
                })
        
        token = jwt.encode(payload={"id":preuser[0]['id'],"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=3600),'username': username},key="my_secret_key",algorithm="HS256")

        response.set_cookie(
            key = 'jwt', 
            value = token,
            expires = timedelta(seconds=3600),
            secure = False,
            samesite = 'Lax'
        )
        preuser[0]['status'] = 'Login Succesfull'
        preuser[0]['status_code'] = '200'
        preuser[0]['access_token'] = token
        
        response.data = preuser

        return response
    
class testView(APIView):
    def get(self,req,format=None):
        
        if not req.COOKIES.get('jwt',None) :
            return Response({
                "status":"Please Login",
                "status_code":"401"
            })
        
        try :
            user_details = jwt.decode(jwt=req.COOKIES['jwt'],key="my_secret_key",algorithms="HS256")
            return Response("Hello")
        
        except:
            return Response({
                "status":"Please Login",
                "status_code":"401"
            })

class addTrainView(APIView):
    def post(self,req,format=None):

        data = req.data
        if not data.get('admin_key',None):
            return Response("you are not admin")
        if not data['admin_key'] == "my_secret_key" : 
            return Response("you are not admin")
        
        if not ( data.get('train_name',None) or data.get('source',None) or data.get('destination',None) or data.get('seat_capacity',None) or data.get('arrival_time_at_source',None) or data.get('arrival_time_at_destination',None) ):
            return Response("Please submit proper data")
        result = query(f"insert into api_train(train_name,source,destination,arrival_time_at_source,arrival_time_at_destination) values (train_name='{data['train_name']}',source='{data['source']}',destination='{data['destination']}',arrival_time_at_source='{data['arrival_time_at_source']}',arrival_time_at_destination='{data['arrival_time_at_destination']}')")
        id = query(f"select id from api_train where train_name='{data['train_name']}'")[0]['id']
        return Response({
            "message": "Train added successfully",
            "train_id": id
        })

class getTrainView(APIView):
    def get(self,req,format=None):

        source = req.query_params['source']
        destination = req.query_params['destination']
        
        result = query(f"select * from api_train where source='{source}' and destination='{destination}' ")

        return Response(result)
    
class bookSeatView(APIView):
    def post(self,req,pk,format=None):

        user_id = jwt.decode(jwt=req.COOKIES['jwt'],key="my_secret_key",algorithms="HS256")['id']
        no_of_seats = req.data['no_of_seats']
        total_seats = query(f"select seat_capacity from api_train where id='{pk}'")[0]['seat_capacity']
        booked_seats = query(f"select * from api_bookedseat cross join api_booking where train_id='{pk}'")
        if int(no_of_seats) >int(total_seats)-len(booked_seats) :
            return Response("Not enough seats")
        
        booked_seat_nos = []
        for s in booked_seats :
            booked_seat_nos.append(s['seat_no'])
        
        new_bookings = []
        seats_added = 0
        for i in range(1,total_seats) :
            if booked_seat_nos.count(i)==0 :
                new_bookings.append(i)
                seats_added += 1
            if seats_added >= int(no_of_seats) :
                break

        query(f"insert into api_booking(train_id,user_id) values ('{pk}','{user_id}')")
        booking = query(f"select * from api_booking where train_id = '{pk}' and user_id='{user_id}'")
        booking_id = booking[-1]['id']

        query(f"update api_train set seat_capacity=seat_capacity-{seats_added} where id='{pk}'")
        for b in new_bookings :
            query(f"insert into api_bookedseat(seat_no,booking_id) values ('{b}','{booking_id}')")
        return Response({
            "booking_id":booking_id,
            "booked_seats":new_bookings
        })
        return Response("hello")
        

class getBookingView(APIView) :
    def get(self,req,pk,format=None):

        user_id = jwt.decode(jwt=req.COOKIES['jwt'],key="my_secret_key",algorithms="HS256")['id']
        result = query(f"select * from api_bookedseat cross join api_booking where user_id='{user_id}' and booking_id='{pk}'")
        train_details = query(f"select * from api_train where id='{result[0]['train_id']}' ")[0]
        booked_seats = []
        for seat in result :
            booked_seats.append(seat['seat_no'])
        response = {
            "train_details" : train_details,
            "booking_id" : pk,
            "no_of_seats":len(booked_seats),
            "seats":booked_seats
        }
        return Response(response)
        

# class searchMovies(APIView):
#     def get(self,request,pk,format=None):
#         return Response(query(f"select * from api_movie where name like '%{pk}%'"))
