from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Profil

class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = ['image_de_profil', 'adresse', 'telephone', 'date_naissance']

class UserSerializer(serializers.ModelSerializer):
    profil = ProfilSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profil']