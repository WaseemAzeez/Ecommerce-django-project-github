from rest_framework.response import Response
from rest_framework.views import APIView

class HomeAPIView(APIView):
    template_name = 'home.html'

    def get(self, request, format=None):
        return Response()

    
class AboutAPIView(APIView):
    template_name = 'about.html'

    def get(self, request, format=None):
        return Response()
    
class ContactAPIView(APIView):
    template_name='contact.html'
    

    def get(self, request, format=None):
        return Response()
