from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, Http404

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser
from .models import LED_bulb, Customer, Fingerprint_device, Mappingstation,Wallet,Transaction
from rest_framework.decorators import api_view


# for LED Buld only
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import LED_bulbSerializer,TransactionSerializer, CustomerSerializer, Fingerprint_deviceSerializer, MappingstationSerializer, CustomerSerializer_status, WalletSerializer

def index(request):
    return HttpResponse("Hello, world. You're at the index.")


class LED_bulbList(APIView):
    def get(self, request, format = None):
        led_bulb = LED_bulb.objects.all()
        serializer = LED_bulbSerializer(led_bulb, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        
        # data = JSONParser().parse(request)
        
        
        # print('date ',led_bulb)
        serializer = LED_bulbSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LED_bulb_pd(APIView):
    
    def get_object(self, id):
        try:
            return LED_bulb.objects.get(id = id)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, format = None):
        id = request.data.get('id')
        led_bulb = self.get_object(id)
        serializer = LED_bulbSerializer(led_bulb)
        return Response(serializer.data)

    def put(self, request, format = None):
        # print("Type is ", type(id), id, request.data.get('id') )
        id = request.data.get('id')
        led_bulb =self.get_object( id )
        serializer = LED_bulbSerializer(led_bulb, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, format = None):
        id = request.data.get('id')
        led_bulb = self.get_object(id)
        led_bulb.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Customer get UUID

class Customer_UUID(APIView):

    def get_object(self, uuid):
        try:
            return Customer.objects.get(uuid = uuid)
        except ObjectDoesNotExist:
            raise Http404
    
    def get(self, request, uuid, format = None):
        # uuid = request.data.get('uuid')
        customer = self.get_object(uuid)
        serializer = CustomerSerializer(customer, many = False)
        # print(serializer.data['uuid'])
        return Response(serializer.data['uuid'], status = status.HTTP_200_OK)


# Fingerprint_device get Location

class Fingerprint_device_location(APIView):
    def get_object(self):
        try:
            return Fingerprint_device.objects.get(fid = 1)
        except ObjectDoesNotExist:
            raise Http404
    
    def get(self, request, format = None):
        
        location = self.get_object()
        serializer = Fingerprint_deviceSerializer(location, many = False)
        
        return Response(serializer.data['location'], status = status.HTTP_200_OK)



class Fingerprint_device_status(APIView):
    def get_object(self):
        try:
            return Fingerprint_device.objects.get(fid = 1)
        except ObjectDoesNotExist:
            raise Http404
    
    def get(self, request, format = None):
        
        finger_print_status = self.get_object()
        serializer = Fingerprint_deviceSerializer(finger_print_status, many = False)
        
        return Response(serializer.data['finger_print_status'], status = status.HTTP_200_OK)
















# Mappingstation get price

class Mappingstation_price(APIView):
    def get_object(self, source, destination):
        try:
            return Mappingstation.objects.defer(destination).filter(all_station_name = source)
            # .values('ghatkopar')
            # return Mappingstation.objects.all()
        except ObjectDoesNotExist:
            raise Http404
    
    def get(self, request, source, destination, format = None):
        
        # print("Line 120 ",source, destination)
        price = self.get_object(source, destination)
        
        serializer = MappingstationSerializer(price, many = True)
        print(serializer.data[0][destination])
        
        return Response(serializer.data[0][destination], status = status.HTTP_200_OK)

#customer status
class Customer_status_uuid(APIView):
    def get_object(self):
        try:
            return Customer.objects.defer('uuid').filter(Q(status=3) | Q(status=7))
          
        except ObjectDoesNotExist:
            raise Http404
    def get_object_by_uuid(self, uuid):
        try:
            return Customer.objects.get(uuid=uuid)
           
        except ObjectDoesNotExist:
            raise Http404
    
    def get(self, request, format = None):
        
        # print("Line 120 ",source, destination)
        uuid = self.get_object()

        

        
        serializer = CustomerSerializer_status(uuid, many = True)
        # if not uuid:
        #      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not serializer.data:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.data)
        
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request, format = None):
        
        uuid = request.data.get('uuid')
        # cust_status = request.data.get('status')
        
        customer =self.get_object_by_uuid( uuid )
        serializer = CustomerSerializer_status(customer, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)













#wallet
class Wallet_money(APIView):
  
    def get_object_by_uuid(self, uuid):
        try:
            return Wallet.objects.get(uuid=uuid)
           
        except ObjectDoesNotExist:
            raise Http404
    
    def get(self, request, uuid, format = None):
        
        print("wallet money till here")
        wallet = self.get_object_by_uuid(uuid)

        print("Wallet is ", wallet)

        
        serializer = WalletSerializer(wallet, many = False)
        print("Serializer is ",serializer)
        
        print("data is ",serializer.data)

        if not serializer.data:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        print("data is ",serializer.data)
        
        return Response(serializer.data['money'], status = status.HTTP_200_OK)


class Wallet_PP(APIView) :
    def get_object_by_uuid(self, uuid):
        try:
            return Wallet.objects.get(uuid=uuid)
           
        except ObjectDoesNotExist:
            raise Http404
    def put(self, request, format = None):
        
        uuid= request.data.get('uuid')
        
        
        wallet =self.get_object_by_uuid( uuid )

        # wallet.money = 
        money = wallet.money - int(request.data.get('money'))
        serializer = WalletSerializer(wallet, data = {"uuid": request.data.get('uuid'), 'money': money})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format = None):
        
        
        
        
        
        serializer = WalletSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






#create transaction
class Create_Transaction(APIView):

    def post(self, request, format = None):
        
        serializer = TransactionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get status of uuid

class Get_Transaction_Status(APIView):
    
    def get_object_by_uuid(self, uuid):
        try:
            return Transaction.objects.defer('status').filter(uuid = uuid).last()
           
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, uuid, format = None):

        transaction = self.get_object_by_uuid(uuid)
        # print("Transaction object is ", transaction)
        serializer = TransactionSerializer(transaction, many = False)
        print("Transaction is ", serializer.data['status'])
        if not serializer.data:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        if serializer.data['status'] is None:
            return Response( {'status': None} , status = status.HTTP_200_OK )
        return Response(serializer.data, status = status.HTTP_200_OK)
       


class Update_Transaction(APIView):
    def get_object_by_uuid(self, uuid):
        try:
            return Transaction.objects.filter(uuid=uuid).last()
           
        except ObjectDoesNotExist:
            raise Http404
    def put(self, request, format = None):
        
        uuid= request.data.get('uuid')
        
        
        transaction = self.get_object_by_uuid( uuid )
        serializer = TransactionSerializer(transaction, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Transaction Api for Mobile App
class Get_Transaction_Details(APIView):
    
    def get_object_by_uuid(self, uuid):
        try:
            return Transaction.objects.filter(uuid = uuid)
           
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, uuid, format = None):

        transaction = self.get_object_by_uuid(uuid)
        # transaction = Transaction.objects.all()
        print("Transaction object is ", transaction)
        serializer = TransactionSerializer(transaction, many = True)
        print("Transaction is ", serializer.data)
        if not serializer.data:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status = status.HTTP_200_OK)
       

        

        
    

       






        
         
    



@api_view(['GET', 'POST'])
def led_bulb_list(request, format = None):
    if request.method == 'GET':
        led_bulb = LED_bulb.objects.all()
        serializer = LED_bulbSerializer(led_bulb, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # data = JSONParser.parse(request.data)
        data = request.data
        serializer = LED_bulbSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def led_bulb_detail(request, id, format = None):
    try:
        led_bulb = LED_bulb.objects.get(id = id)
    except led_bulb.DeosNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LED_bulbSerializer(led_bulb)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LED_bulbSerializer(led_bulb, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        led_bulb.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        

class Transaction_uuid(APIView):
    def get_object(self, uuid):
        try:
            return Transaction_uuid.objects.get(uuid = uuid)
        except ObjectDoesNotExist:
            raise Http404
    
    def get(self, request, uuid, format = None):
        
        Transaction = self.get_object(uuid)
        serializer = Fingerprint_deviceSerializer(Transaction, many = False)
        
        return Response(serializer.data['location'], status = status.HTTP_200_OK)
    
     

    
def finger_html(request):
    if request.method == 'POST':
        
      
        
        uuid= request.POST.get('c_uuid')
        status=request.POST.get('status')
        print(uuid)
        validate = saveToDB(uuid,status)
        if validate == True:
            return render(request, 'biometric_ticket/fingerprint.html', context={'scanning': 'True','status':status})
        
            
    
    return render(request, 'biometric_ticket/fingerprint.html', context={'scanning': 'False'})
def saveToDB(uuid,status ):
    try:
        customer = Customer.objects.get(uuid = uuid)
    
        customer.status = status
        customer.save()

        return True
    except ObjectDoesNotExist:
        return False
    return False
    