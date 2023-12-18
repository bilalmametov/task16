from rest_framework import serializers
from .models import Product 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' 
        # exclude = ['id', 'title'] 
        
    def validate_title(self, value):
        if len(value) > 50:
            raise ValueError('title length more than 50') 
        return value