from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from ..models import Profil

class ProfilSerializer(serializers.ModelSerializer):
    """
    Sérializer pour le modèle Profil.
    """
    class Meta:
        model = Profil
        fields = [
            'image_de_profil',
            'adresse',
            'telephone',
            'date_naissance',
            'full_name'
        ]
        read_only_fields = ['full_name']

class UserSerializer(serializers.ModelSerializer):
    """
    Sérializer pour le modèle User.
    """
    profil = ProfilSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profil',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Sérializer pour l'inscription d'un nouvel utilisateur.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name'
        ]
    
    def validate(self, attrs):
        """Vérifie que les mots de passe correspondent."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Les mots de passe ne correspondent pas.'
            })
        return attrs
    
    def create(self, validated_data):
        """Crée un nouvel utilisateur avec le mot de passe hashé."""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        # Créer un profil vide pour l'utilisateur
        Profil.objects.create(user=user)
        return user