from django.db import models
from django.utils import timezone
from datetime import timedelta

class Book(models.Model):
    category = models.CharField(max_length=255, null=False)
    author = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)
    year_published = models.IntegerField(null=False)
    loan_type = models.IntegerField(choices=[
        (1, '10 дней'),
        (2, '5 дней'),
        (3, '2 дня')
    ], null=False)
    added_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} by {self.author}"


class Customer(models.Model):
    name = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)
    age = models.IntegerField(null=False)
    email = models.EmailField(null=False)

    def __str__(self):
        return self.name


class Loan(models.Model):
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(default=timezone.now, null=False)
    return_date = models.DateTimeField(null=True, blank=True)

    def set_return_date(self):
        # Определяем количество дней на основе типа займа книги
        loan_duration = {
            1: 10,  # 10 дней
            2: 5,   # 5 дней
            3: 2    # 2 дня
        }
        # Получаем количество дней на основе типа займа и устанавливаем return_date
        self.return_date = self.loan_date + timedelta(days=loan_duration.get(self.book_id.loan_type, 0))

    def save(self, *args, **kwargs):
        # При сохранении автоматически рассчитываем дату возврата
        self.set_return_date()  # Вызываем метод для установки даты возврата
        super(Loan, self).save(*args, **kwargs)

    def __str__(self):
        return f"Loan of {self.book_id.name} to {self.cust_id.name} from {self.loan_date.date()} to {self.return_date.date() if self.return_date else 'not set'}"
