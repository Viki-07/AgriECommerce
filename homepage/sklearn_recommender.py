from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Product, Order, OrderItem
import numpy as np

class SklearnRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = None
        self.products = None
        self._fit()

    def _fit(self):
        """Fit the TF-IDF vectorizer on all products"""
        self.products = list(Product.objects.all())
        if not self.products:
            return

        # Combine product features into text
        product_features = [
            f"{p.name} {p.category} {p.description}" 
            for p in self.products
        ]

        # Create TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(product_features)

    def get_recommendations(self, product_id, n_recommendations=4):
        """Get recommendations for a specific product"""
        if not self.products or self.tfidf_matrix is None:
            return []

        try:
            # Find the index of the product
            product_idx = next(
                i for i, p in enumerate(self.products) 
                if p.id == product_id
            )

            # Calculate cosine similarity
            cosine_similarities = cosine_similarity(
                self.tfidf_matrix[product_idx:product_idx+1], 
                self.tfidf_matrix
            ).flatten()

            # Get indices of most similar products
            similar_indices = cosine_similarities.argsort()[::-1][1:n_recommendations+1]

            # Return recommended products
            return [self.products[i] for i in similar_indices]

        except (StopIteration, IndexError):
            return []

    def get_user_recommendations(self, user, n_recommendations=4):
        """Get personalized recommendations for a user"""
        if not self.products or self.tfidf_matrix is None:
            return []

        # Get user's order history through Order model
        user_orders = Order.objects.filter(user=user)
        if not user_orders.exists():
            return []

        # Calculate average similarity scores
        avg_similarities = np.zeros(len(self.products))
        order_count = 0
        
        for order in user_orders:
            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                try:
                    product_idx = next(
                        i for i, p in enumerate(self.products) 
                        if p.id == item.product.id
                    )
                    similarities = cosine_similarity(
                        self.tfidf_matrix[product_idx:product_idx+1], 
                        self.tfidf_matrix
                    ).flatten()
                    avg_similarities += similarities
                    order_count += 1
                except (StopIteration, IndexError):
                    continue

        if order_count > 0:
            avg_similarities /= order_count

        # Get indices of most similar products
        similar_indices = avg_similarities.argsort()[::-1][:n_recommendations]

        # Return recommended products
        return [self.products[i] for i in similar_indices] 