from django.contrib import admin
from .models import Book, Customer, Loan

# Регистрируем модели Book, Customer и Loan в админке
admin.site.register(Book)
admin.site.register(Customer)
admin.site.register(Loan)
