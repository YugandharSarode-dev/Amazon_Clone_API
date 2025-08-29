from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from utility.response import ApiResponse
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, get_serielizer_error
from store.model.cart_model import Cart
from store.model.product_model import Product
from store.serializers.cart_serializer import CartSerializer

class CartView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = CartSerializer
    singular_name = 'Cart'
    model_class = Cart.objects
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    search_fields = ['products']

    def get_object(self):
        try:
            pk = self.kwargs.get('id')
            return self.model_class.get(pk=pk)
        except:
            return None

    def create(self, request, *args, **kwargs):
        """Add multiple products to the cart"""
        try:
            req_data = request.data.copy()
            req_data['user'] = request.user.id  

            products_list = req_data.get('products', [])
            if not isinstance(products_list, list):
                return ApiResponse.response_bad_request(self, message="Products list is required.")

            validated_products = []
            for item in products_list:
                product_id = item.get('product_id')
                quantity = int(item.get('quantity', 1))
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    return ApiResponse.response_bad_request(self, message=f"Product {product_id} does not exist.")
                validated_products.append({"product_id": product.id, "quantity": quantity})

            req_data['products'] = validated_products

            serializer = self.serializer_class(data=req_data)
            if serializer.is_valid():
                cart_item = serializer.save()  
                return ApiResponse.response_created(self, data=self.serializer_class(cart_item).data, message=self.singular_name + ' added to cart successfully.')

            error_resp = get_serielizer_error(serializer)
            return ApiResponse.response_bad_request(self, message=error_resp)

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def list(self, request, *args, **kwargs):
        """List all products in the logged-in user's cart"""
        try:
            cart_items = Cart.objects.filter(user=request.user)
            resp_list = [self.transform_single(item) for item in cart_items]
            return ApiResponse.response_ok(self, data=resp_list)

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def delete(self, request, *args, **kwargs):
        """Delete a cart row"""
        try:
            instance = self.get_object()
            if not instance:
                return ApiResponse.response_not_found(self, message=self.singular_name + ' item not found in cart.')

            instance.delete()
            return ApiResponse.response_ok(self, message=self.singular_name + ' removed from cart.')

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def transform_single(self, instance):
        """Prepare the cart response"""
        products_resp = []
        for item in instance.products:
            try:
                product = Product.objects.get(id=item['product_id'])
                products_resp.append({
                    "product_id": product.id,
                    "name": product.name,
                    "price": str(product.price),
                    "quantity": item['quantity']
                })
            except Product.DoesNotExist:
                continue

        return {
            'cart_id': instance.id,
            'products': products_resp,
            'added_at': instance.added_at,
        }
