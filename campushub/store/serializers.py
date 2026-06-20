from rest_framework import serializers
from .models import Category, Product, Cart, CartItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'category_name', 'name', 'slug',
                  'description', 'price', 'stock', 'available', 'created']


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'qty', 'subtotal']

    def get_subtotal(self, obj):
        return obj.product.price * obj.qty


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total', 'created']
        read_only_fields = ['id', 'user', 'created']

    def get_total(self, obj):
        return sum(item.product.price * item.qty for item in obj.items.all())


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'qty', 'price_at_purchase']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created', 'total', 'paid', 'items']
        read_only_fields = ['id', 'user', 'created', 'total', 'paid']


class OrderCreateSerializer(serializers.Serializer):
    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.prefetch_related('items__product').get(user=user)
        if not cart.items.exists():
            raise serializers.ValidationError("Cart is empty.")
        order = Order.objects.create(user=user, total=0)
        total = 0
        for ci in cart.items.all():
            OrderItem.objects.create(
                order=order, product=ci.product,
                product_name=ci.product.name,
                qty=ci.qty, price_at_purchase=ci.product.price
            )
            total += ci.product.price * ci.qty
        order.total = total
        order.save()
        cart.items.all().delete()
        return order
