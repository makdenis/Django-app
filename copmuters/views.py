from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import View
from django.views.generic import ListView
from .models import *
from .form import *
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView

from django.http import JsonResponse
from copmuters.paginator import paginate


class CustomerView(ListView):
    model = Customer
    template_name = 'customer_list.html'


# форма регистрации
def check(request):

    data={
       'is_true' :request.GET.get("data").isdigit()
    }
    return  JsonResponse(data)


# регистрация
def add(request):
    if request.method == 'POST':

        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        type1 = request.POST.get('type')
        quantity1 = request.POST.get('quantity')
        description1 = request.POST.get('description')
        pic1 = request.FILES.get('pic')

        try:
            int(price1)
            int(quantity1)
        except:
            return render(request, 'add.html', {'error': "Ошибка, возможны только числовые значения"})

        else:
            comp = Computer(name=name1, price=price1, type=type1, quantity=quantity1, description=description1,
                            pic=pic1)
            comp.save()
        return HttpResponseRedirect('/item-' + name1)
    return render(request, 'add.html', locals())


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # print(form)
        is_val = form.is_valid()

        data = form.cleaned_data
        # print(data)
        #  avatar1 = request.FILES.get('avatar')
        #  print(avatar1)
        print(is_val)
        if data['password'] != data['password2']:
            is_val = False
            form.add_error('password2', ['Пароли должны совпадать'])
        if User.objects.filter(username=data['username']).exists():
            form.add_error('username', ['Такой логин уже занят'])
            is_val = False

        if is_val:
            cust = Customer()
            cust.user = User.objects.create_user(data['username'], data['email'], data['password'])
            # print(user)

            cust.first_name = data['first_name']
            cust.last_name = data['last_name']
            a = request.FILES.get('avatar')
            print("ff")
            print(a)
            cust.avatar = a
            print(cust.avatar)
            cust.save()
            return HttpResponseRedirect('/authorization/')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


# авторизация django
def authorization(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        print(form)
        data = form.cleaned_data
        if form.is_valid():
            user = authenticate(request, username=data['username'], password=data['password'])
            # user = authenticate(request, username='petrov',password='12345678')
            print(len(data['username']), len(data['password']))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/success_authorization')
            else:
                form.add_error('username', ['Неверный логин или пароль'])
                # raise forms.ValidationError('Имя пользователя и пароль не подходят')
    else:
        form = AuthorizationForm()
    return render(request, 'authorization.html', {'form': form})


# успешная авторизация django
@login_required(login_url='/authorization')
def success_authorization(request):
    return HttpResponseRedirect('/')


# class ItemsView(AjaxListView):
#     template_name = 'labApp/templates/list.html'
#     context_object_name = "list_object"
#     page_template = 'labApp/templates/list_object.html'


def tag(request):
    tagg = request.GET.get('tag')
    # print(Tag.objects.all())
    data = Computer.objects.filter(tag__name=tagg)
    print(data)
    page = request.GET.get('page')
    # for i in Question.objects.all().filter(tag=tagg):
    # data.append(i)
    return render(request, 'list.html', {'data': paginate(data, page)})


def ListingByTag(request):
    comp = Computer.objects.all()

    page = request.GET.get('page')
    return render(request, 'list.html', {'comp': comp, 'data': paginate(comp, page)})


def fresh(request):
    data = Computer.objects.filter(pub_date__gte='2018-03-31 19:51')
    print(data)
    page = request.GET.get('page')
    # for i in Question.objects.all().filter(tag=tagg):
    # data.append(i)
    return render(request, 'list.html', {'data': paginate(data, page)})


def ItemsView(request):
    # dict_customers = {}  # код компа - массив покупателей
    data = Computer.objects.get_queryset().order_by('name')
    # form = forms.ComputerForm()

    page = request.GET.get('page')
    # page = 1
    comps = paginate(data, page)

    return render(request, 'list.html',
                  context={'page': page,
                           'data': comps,
                           })


def Settings(request):
    if request.user.is_authenticated:
        us = request.user
        if request.method == 'POST':
            form = SettingForm(request.POST)
            is_val = form.is_valid()
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            avatar = request.FILES.get('file')
            if password != us.password:
                form.add_error('old_password', ['Incorrect password'])
                is_val = False

            us.password = password2
            us.profile.avatar = avatar
            us.save()
            us.profile.save()
            return HttpResponseRedirect('/')
        else:
            form = SettingForm()
    else:
        return HttpResponseRedirect('/sign_in/')

    return render(request, 'settings.html', {'form': form})


def OneItem(request, pk):
    print(pk)
    ans = Answer.objects.filter(comp=pk)
    # print(t)
    comp = Computer.objects.get(name=pk)
    if request.user.is_authenticated:
        us = request.user.id
        t = Customer.objects.get(user_id=us)

        c = Computer.objects.get(name=pk)
        a = request.POST.get('comment')

        if (a):
            answer = Answer.objects.create(
                user=t,
                comp=c,
                text=a,
            )
            answer.save()

    return render(request, 'object.html', {'computer': comp, 'answer': ans})


def like(request):
    if request.method == 'POST':
        user = request.user
        quest = Question.objects.get(id=int(request.POST.get('question')))
        if request.POST.get('positive') == 'true':
            print('positive')
            try:
                lk = Like(question_key=quest, like_author=user, rate=True)
                lk.save()
                quest.counter()
                quest.save()
                return JsonResponse({'rating': quest.rating}, status=200)
            except:
                lkk = Like.objects.get(question_key=quest, like_author=user, rate=True)
                lkk.delete()
                quest.counter()
                quest.save()
                return JsonResponse({'rating': quest.rating}, status=200)


        else:
            try:
                lk = Like(question_key=quest, like_author=user, rate=False)
                lk.save()
                quest.counter()
                quest.save()
                return JsonResponse({'rating': quest.rating}, status=200)
            except:
                lkk = Like.objects.get(question_key=quest, like_author=user, rate=False)
                lkk.delete()
                quest.counter()
                quest.save()
                return JsonResponse({'rating': quest.rating}, status=200)
    return HttpResponse()


def ord(request, namekomp):
    if request.method == "GET":
        return JsonResponse(Order.orders(request, namekomp), status=200)


class OrdersView(View):
    def get(self, request):
        empty_orders = []
        computers_in_order = BelongTO.objects.all()  # код заказа - компы
        prices = {}  # цены
        data = Order.objects.filter(
            customer_id=request.user.id - 1).all()  # заказы пользователя
        for o in data:
            computers = BelongTO.objects.filter(
                order_id=o.code).all()  # компьютеры заказа
            if len(computers) == 0:
                empty_orders.append(o.code)
            total = 0
            for c in computers:
                cur_comp = Computer.objects.get(name=c.item_id)
                if c.item_id not in prices.keys():
                    prices[c.item_id] = cur_comp.price
                total = total + cur_comp.price * c.quantity
            o.total = total
            o.save()

        return render(request, 'orders.html',
                      context={"data": data,
                               "computers": computers_in_order,
                               "prices": prices,
                               'empty_orders': empty_orders})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
