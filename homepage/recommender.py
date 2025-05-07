from django.db.models import Count, Q
from .models import Product, OrderItem, Cart
import random
from collections import Counter

class ProductRecommender:
    """
    A simple recommendation system for suggesting products to users.
    This implementation uses a hybrid approach combining:
    1. Popular products (based on order history)
    2. Category-based recommendations
    3. Random recommendations for diversity
    """
    
    @staticmethod
    def get_popular_products(limit=4):
        """
        Get the most popular products based on order history.
        """
        # Get products that have been ordered the most
        popular_products = Product.objects.filter(
            orderitem__isnull=False
        ).annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:limit]
        
        return list(popular_products)
    
    @staticmethod
    def get_category_based_recommendations(product_category, limit=2, exclude_product_id=None):
        """
        Get recommendations based on product category.
        """
        query = Product.objects.filter(category=product_category)
        
        if exclude_product_id:
            query = query.exclude(id=exclude_product_id)
            
        # Get products from the same category
        category_products = list(query.order_by('?')[:limit])
        
        return category_products
    
    @staticmethod
    def get_random_recommendations(limit=2, exclude_product_ids=None):
        """
        Get random product recommendations for diversity.
        """
        query = Product.objects.all()
        
        if exclude_product_ids:
            query = query.exclude(id__in=exclude_product_ids)
            
        random_products = list(query.order_by('?')[:limit])
        
        return random_products
    
    @staticmethod
    def get_user_based_recommendations(user, limit=4):
        """
        Get personalized recommendations based on user's order history.
        """
        if not user.is_authenticated:
            # For non-authenticated users, return popular products
            return ProductRecommender.get_popular_products(limit)
        
        # Get user's order history
        user_orders = OrderItem.objects.filter(order__user=user)
        
        if not user_orders.exists():
            # If user has no orders, return popular products
            return ProductRecommender.get_popular_products(limit)
        
        # Get categories the user has purchased from
        user_categories = Counter(
            user_orders.values_list('product__category', flat=True)
        )
        
        # Get the most common category
        if user_categories:
            most_common_category = user_categories.most_common(1)[0][0]
            
            # Get products from the user's most common category
            category_products = Product.objects.filter(
                category=most_common_category
            ).exclude(
                id__in=user_orders.values_list('product_id', flat=True)
            ).order_by('?')[:limit]
            
            if len(category_products) >= limit:
                return list(category_products)
        
        # If we don't have enough category-based recommendations,
        # mix with popular products
        recommendations = list(category_products) if 'category_products' in locals() else []
        
        # Add popular products to fill the gap
        popular_products = ProductRecommender.get_popular_products(
            limit - len(recommendations)
        )
        
        recommendations.extend(popular_products)
        
        return recommendations
    
    @staticmethod
    def get_recommendations_for_product(product_id, limit=4):
        """
        Get recommendations for a specific product.
        """
        try:
            product = Product.objects.get(id=product_id)
            
            # Get products from the same category
            category_products = ProductRecommender.get_category_based_recommendations(
                product.category, 
                limit=limit//2,
                exclude_product_id=product_id
            )
            
            # Get random products for diversity
            random_products = ProductRecommender.get_random_recommendations(
                limit=limit - len(category_products),
                exclude_product_ids=[product_id] + [p.id for p in category_products]
            )
            
            # Combine recommendations
            recommendations = category_products + random_products
            
            # Shuffle the recommendations
            random.shuffle(recommendations)
            
            return recommendations
            
        except Product.DoesNotExist:
            # If product doesn't exist, return popular products
            return ProductRecommender.get_popular_products(limit)
    
    @staticmethod
    def get_recommendations(limit=4, product_id=None, user=None):
        """
        Main method to get recommendations.
        """
        if product_id:
            # If we have a product ID, get recommendations for that product
            return ProductRecommender.get_recommendations_for_product(product_id, limit)
        elif user:
            # If we have a user, get personalized recommendations
            return ProductRecommender.get_user_based_recommendations(user, limit)
        else:
            # Default to popular products
            return ProductRecommender.get_popular_products(limit) 