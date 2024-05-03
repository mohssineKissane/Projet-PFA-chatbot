from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('id',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'selling_price', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_name', 'product_quantity', 'created_at')

    def product_name(self, obj):
        return obj.product.name

    def product_quantity(self, obj):
        return obj.product_qty

    product_name.admin_order_field = 'product__name'
    product_quantity.short_description = 'Quantity'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    list_display = ('user', 'ordered_items', 'total_price', 'created_at',
                    'status')

    def user(self, obj):
        return obj.user.username

    def ordered_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        items = []
        for item in order_items:
            items.append(f'{item.product.name} (Qty: {item.quantity})')
        return ', '.join(items)

    ordered_items.short_description = 'Ordered Items'


class ChatBotAdmin(admin.ModelAdmin):
    list_display = ('user', 'text_input', 'date')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ChatBot, ChatBotAdmin)
