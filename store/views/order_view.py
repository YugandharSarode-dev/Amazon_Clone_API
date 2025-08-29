from django.db.models import F
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from store.model.orderItem_model import OrderItem
from utility.response import ApiResponse
from utility.utils import CreateRetrieveUpdateViewSet, get_serielizer_error
from store.model.order_model import Order

from store.serializers.order_serializer import OrderSerializer
from store.model.cart_model import Cart
from store.model.product_model import Product

class OrderView(CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = OrderSerializer
    singular_name = 'Order'
    model_class = Order.objects
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:

            cart_rows = Cart.objects.filter(user=request.user)
            if not cart_rows.exists():
                return ApiResponse.response_bad_request(self, message="Cart is empty.")

            total_amount = 0
            order_items_data = []


            for cart in cart_rows:
                for p in cart.products:  
                    product_id = p['product_id']
                    quantity = int(p.get('quantity', 1))

                    try:
                        product = Product.objects.get(id=product_id)
                    except Product.DoesNotExist:
                        return ApiResponse.response_bad_request(self, message=f"Product with id {product_id} does not exist.")

                    if product.stock < quantity:
                        return ApiResponse.response_bad_request(self, message=f"Not enough stock for product {product.name}.")

                    total_amount += product.price * quantity
                    order_items_data.append({'product': product, 'quantity': quantity})

        
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount)

            for item in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price = item['product'].price
                )
                
                Product.objects.filter(id=item['product'].id).update(
                    stock=F('stock') - item['quantity']
                )


            cart_rows.delete()

            resp_data = OrderSerializer(order).data
            return ApiResponse.response_created(self, data=resp_data, message=self.singular_name + " created successfully.")

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])
