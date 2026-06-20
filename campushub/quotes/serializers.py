from rest_framework import serializers
from .models import Quote, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class QuoteSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Quote
        fields = ['id', 'text', 'author', 'category', 'category_name', 'is_famous', 'source']
