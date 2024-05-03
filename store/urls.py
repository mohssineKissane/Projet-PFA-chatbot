from django.urls import path
from . import views
from store.controller import authviews, cartviews, checkoutviews, chatbotviews

urlpatterns = [
    path('', views.home, name="home"),
    path('categories/', views.categories, name="categories"),
    path('categories/<str:slug>/', views.categoriesview, name="categoriesview"),
    path('categories/<str:cate_slug>/<str:prod_slug>/',
         views.productview, name="productview"),
    path('register/', authviews.register, name="register"),
    path('login', authviews.loginpage, name="loginpage"),
    path('logout/', authviews.logoutpage, name="logoutpage"),
    path('add-to-cart', cartviews.addtocart, name='addtocart'),
    path('cart', cartviews.viewcart, name='cart'),
    path('update-cart', cartviews.updatecart, name='updatecart'),
    path('delete-cart-item', cartviews.deletecartitem, name='deletecartitem'),
    path('checkout', checkoutviews.index, name='checkout'),
    path('place-order', checkoutviews.placeorder, name='placeorder'),
    path('list-order', checkoutviews.listorder, name='listorder'),

    path("chat", chatbotviews.chat, name="chat"),
    path("ask_question/", chatbotviews.ask_question, name="ask_question"),

]
