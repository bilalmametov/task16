1. Создайте Django-проект:
   
   В вашем терминале выполните следующие команды:

   bash
   django-admin startproject config
   

2. Создайте приложения `product`:
   
   bash
   python3 manage.py startapp product
   

3. Определите модель Product:

   python
   class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return f'{self.title} -> {self.pk}'

   

4. Настройте приложения в `settings.py`:

   В файле config/settings.py добавьте в раздел INSTALLED_APPS ваши приложения:

   python
   INSTALLED_APPS = [
       # ...
        'rest_framework',
        'ManytoManyApp',
        'OnetoOneApp'
   ]
   

5. В `config/urls.py` пропишите маршрутизацию:
   python
   urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls'))
   ]
   

6. Определите функцию представления (view) для конкретного URL-маршрута:
   python
      @api_view(['GET'])
      def get_products(request):
         QuerySet = Product.objects.all()
         serializer = ProductSerializer(QuerySet, many=True)
         return Response(serializer.data)

      @api_view(['POST'])
      def create_product(request):
         serializer = ProductSerializer(data=request.data)
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      @api_view(['GET'])
      def get_one_product(request, pk):
         try:
            product = Product.objects.get(pk=pk)
         except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
         serializer = ProductSerializer(product)
         return Response(serializer.data)
   

7. Определите URL-маршрут для функции представления, используя функцию path:
   python
   urlpatterns = [
    path('get/', get_products),
    path('create/', create_product),
    path('get/<int:pk>/', get_one_product)
   ]
   

8. Определите класс сериализатора и определите поля:
   python
   from rest_framework import serializers
   from .models import Product

   class ProductSerializer(serializers.ModelSerializer):
      class Meta:
         model = Product
         fields = '__all__'
      
      def validate(self, value):
         if len(value) > 50:
            raise serializers.ValidationError('title length more than 50')
         return value
      def validate(self, attrs):
         return super().validate(attrs)
   
   
9. Выполните миграции:

   bash
   python manage.py makemigrations
   python manage.py migrate