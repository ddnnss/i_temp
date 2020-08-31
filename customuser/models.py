import decimal
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string
import uuid

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    email = models.EmailField('Эл. почта', unique=True)

    email_ok = models.BooleanField(default=False)
    profile_ok = models.BooleanField(default=False)
    wallet = models.UUIDField(default=uuid.uuid4)
    balance = models.DecimalField('Баланс', decimal_places=2,max_digits=10,default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()



class Transaction(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='ОТ', related_name='from_user')
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Кому', related_name='to_user')
    amount = models.DecimalField('Сумма', decimal_places=2, max_digits=10, default=0)
    rate = models.DecimalField('Курс', decimal_places=2, max_digits=10, default=1)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f'Перевод от: {self.from_user.id} - {self.to_user.id}'

    class Meta:
        verbose_name = "Перевод"
        verbose_name_plural = "Переводы"

class History(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Пользователь', )
    amount = models.DecimalField('Сумма', decimal_places=2, max_digits=10, default=0)
    rate = models.DecimalField('Курс', decimal_places=2, max_digits=10, default=1)
    total = models.DecimalField('Итоговая сумма', decimal_places=2, max_digits=10, default=1)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f'История пользователя ID: {self.user.id}'

    class Meta:
        verbose_name = "История пользователя"
        verbose_name_plural = "Истории пользователей"