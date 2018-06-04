from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib import admin
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(User,related_name="profile", on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=75)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='media/', null=True, blank=True)
    objects = UserManager()

    def __unicode__(self):
        return self.customer_name

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "{}".format(self.name)

class Computer(models.Model):
    PersonalComputer = 'Personal Computer'
    Monoblock = 'Monoblock'
    Laptop = 'Laptop'
    computer_types = {
        (PersonalComputer, 'Personal computer'),
        (Monoblock, 'Monoblock'),
        (Laptop, 'Laptop'),
    }
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    price = models.IntegerField(null=True, default=0)
    description = models.TextField(
        max_length=500, default='No description yet')
    type = models.CharField(
        max_length=30, choices=computer_types, default=PersonalComputer)
    # pic = models.ImageField(upload_to='media/', default='media/ts.jpg')
    quantity = models.IntegerField(null=True, default=0)
    pic = models.ImageField(upload_to='media/', null=True, blank=True)
    rating = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=timezone.now)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Answer(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    comp = models.ForeignKey(Computer, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    pub_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "{} {}".format(self.question.title, self.pub_date)


class Order(models.Model):
    date = models.DateTimeField(default=timezone.now)
    items = models.ManyToManyField(Computer, through='BelongTo')
    code = models.AutoField(max_length=6, unique=True, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.DecimalField(
        decimal_places=2, max_digits=10, unique=False, default=0.0)
    is_open = models.BooleanField(default=True)

    def orders(self, request, namekomp):
        comp = Computer.objects.get(name=namekomp)
        id = request.user.id + 1
        cust = Customer.objects.get(id=id)
        price = 1
        order = Order()
        order.customer = cust
        order.price = price
        order.total = 1
        order.save()
        order2 = BelongTO()
        order2.quantity = 1
        order2.id = id
        order2.item_id = comp
        order2.order_id = id
        order2.save()
        return {'users': cust.customer_name}

    def __str__(self):
        return str(self.code)

class Like(models.Model):
    comp_key = models.ForeignKey(Computer, on_delete=models.CASCADE)
    like_author = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.BooleanField(default=None)

    class Meta:
        unique_together= ['comp_key', 'like_author']



class BelongTO(models.Model):
    item = models.ForeignKey(Computer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    id = models.CharField(unique=True, primary_key=True, max_length=255)

    def __str__(self):
        return self.id
