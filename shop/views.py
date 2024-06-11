# Create your views here.
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework import status
from rest_framework import permissions


from rest_framework import viewsets
from .models import Category, Region, Product, Cart
from .serializers import CategorySerializer, RegionSerializer, ProductSerializer, CartSerializer,ProductStockSerializer

def index(request):
    return render(request,'shop/index.html')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'], url_path='stock')
    def check_stock(self, request, pk=None):
        try:
            product = self.get_object()
            serializer = ProductStockSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        region_id = self.request.query_params.get('region')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if region_id:
            queryset = queryset.filter(region_id=region_id)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset
        

class CartViewSet(viewsets.ModelViewSet):
    """
    list:
    Return a list of all the items in the cart.

    create:
    Add a new item to the cart.

    retrieve:
    Retrieve a specific cart item by its ID.

    update:
    Update a cart item instance.

    partial_update:
    Partially update a cart item instance.

    destroy:
    Remove an item from the cart.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]


    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')

        if not product_id or not quantity:
            return Response({"error": "Product and quantity are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = Cart.objects.get_or_create(product=product, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        quantity = request.data.get('quantity')
        if not quantity:
            return Response({"error": "Quantity is required."}, status=status.HTTP_400_BAD_REQUEST)

        instance.quantity = quantity
        instance.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial) 
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def delete(self, request,product_id, *args, **kwargs):
        try:
            instance = self.get_object(id=product_id)
            self.perform_destroy(instance)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all the existing categories.

    create:
    Create a new category instance.

    retrieve:
    Retrieve a specific category by its ID.

    update:
    Update a category instance.

    partial_update:
    Partially update a category instance.

    destroy:
    Delete a category instance.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all the existing regions.

    create:
    Create a new region instance.

    retrieve:
    Retrieve a specific region by its ID.

    update:
    Update a region instance.

    partial_update:
    Partially update a region instance.

    destroy:
    Delete a region instance.
    """

    queryset = Region.objects.all()
    serializer_class = RegionSerializer

