from django.urls import re_path,path
from django.conf.urls import include 
from django.conf import settings

from store.views.cart_view import CartView
from store.views.category_view import CategoryView
from store.views.order_view import OrderView
from store.views.product_view import ProductView
from store.views.user_view import UserView
from .views.login import LoginViewSet
from .views.forget_password import ForgotPasswordView
from .views.verify_otp import VerifyPasswordView
from .views.reset_password import ResetPasswordView
from .views.logout import LogoutView
from .views.user_impersonate import ImpersonateView
from .views.login_verify_otp import LoginVerifyView

""" User login/ add/ logout profile urls"""
urlpatterns = [
    re_path(r'^login/$', LoginViewSet.as_view()),
    re_path(r'^logout/$', LogoutView.as_view()),
]

""" User forget_password/ verify_otp/ reset_password/ profile urls"""
urlpatterns += [
    re_path(r'^forget_password/$', ForgotPasswordView.as_view()),
    re_path(r'^verify_otp/$', VerifyPasswordView.as_view()),
    re_path(r'^reset_password/$', ResetPasswordView.as_view()),
]

""" User impersonate"""
urlpatterns += [
    re_path(r'^user-impersonate/(?P<id>.+)/$', ImpersonateView.as_view({'get': 'retrieve'})),
]

""" login-verify-otp"""
urlpatterns += [
    re_path(r'^login-verify-otp/$', LoginVerifyView.as_view({'get': 'retrieve'})),
]

        

from .views.student import StudentView

''' Student '''
urlpatterns += [
    re_path(r'^student/$', StudentView.as_view({'get': 'list', 'post': 'create', 'put': 'partial_update', 'delete': 'bulk_delete'})),
    re_path(r'^student/(?P<id>.+)/$', StudentView.as_view({'get': 'retrieve', 'delete': 'delete'})),
]

       
'''User'''
urlpatterns += [
    path('register/', UserView.as_view({'post': 'create'}), name='register'),
    path('update/<int:id>/', UserView.as_view({'put': 'update'}), name='update'),
    path('list/', UserView.as_view({'get': 'list'}), name='list'),
    path('delete/<int:id>/', UserView.as_view({'delete': 'delete'}), name='delete'),
]

'''Product'''
urlpatterns += [
    path('registerproduct/', ProductView.as_view({'post': 'create'}), name='register-product'),
    path('updateproduct/<int:id>/', ProductView.as_view({'put': 'update'}), name='update-product'),
    path('listproduct/', ProductView.as_view({'get': 'list'}), name='list-product'),
    path('deleteproduct/<int:id>/', ProductView.as_view({'delete': 'delete'}), name='delete-product'),
]

'''category'''
urlpatterns += [
    path('registercat/', CategoryView.as_view({'post': 'create'}), name='register-cat'),
    path('updatecat/<int:id>/', CategoryView.as_view({'put': 'update'}), name='update-cat'),
    path('listcat/', CategoryView.as_view({'get': 'list'}), name='list-cat'),
    path('deletecat/<int:id>/', CategoryView.as_view({'delete': 'delete'}), name='delete-cat'),
]
'''Cart'''
urlpatterns += [
    path('addtocart/', CartView.as_view({'post': 'create'}), name='add-to-cart'),
    path('listcart/', CartView.as_view({'get': 'list'}), name='list-cart'),
    path('deletecart/<int:id>/', CartView.as_view({'delete': 'delete'}), name='delete-cart'),
]

'''Order'''
urlpatterns += [
    path('createorder/', OrderView.as_view({'post': 'create'}), name='create-order'),
]