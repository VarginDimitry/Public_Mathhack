from django.shortcuts import render, redirect
from django.views.generic.base import View
from .forms import CreateUserForm
from .forms import SolvingVariantForm, ChangeUserForm
from django.core.paginator import Paginator

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group

from .models import Task, Variant, Customer, SolvingVariant

import os

from WebApp.settings import BASE_DIR

class VariantsView(View):
    """Список всех вариантов на главной странице"""

    def get(self, request):
        variants = Variant.objects.all()
        return render(request, 'mathhack/main.html', {'variant_list': variants})


class UserPageView(View):
    def get(self, request, pk):
        if not User.objects.filter(id=pk):
            page_title = "Пользователь не найден"
            message = 'Пользователь не найден'
            return render(request, 'mathhack/errors/Not_founded_user.html',
                          {'page_title': page_title, 'message': message, }, )
        else:
            this_user = User.objects.get(id=pk)
            page_title = str(this_user.username)

            statistics = this_user.customer.solved_variants.all()[::-1]
            paginator = Paginator(statistics, 10)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            if this_user.customer.points_num != 0:
                average_point = this_user.customer.points_sum / this_user.customer.points_num
                average_point = '{0:0.2f}'.format(average_point)
            else:
                average_point = 'No information'
            return render(request, 'mathhack/auth/user_page.html',
                          {'this_user': this_user, 'page_title': page_title, 'pk': pk, 'average_point': average_point,
                           'statistics': statistics, 'page_obj': page_obj})


def ChangeUserPage(request, pk):
    """изменить пользователя"""
    if pk != request.user.id:
        return redirect('/')
    form = ChangeUserForm()
    page_title = f'Изменить страницу'
    user = request.user

    if request.method == "POST":
        form = ChangeUserForm(request.POST, request.FILES)
        if form.is_valid():
            test_image_size = form.clean_image()
            if test_image_size == 0:
                pass
            elif test_image_size == 1:
                messages.error(request, 'Изображение больше чем 4МБ!')
                return redirect(f'/id{pk}/change')
            elif test_image_size == 2:
                messages.error(request, 'Не получается прочитать изображение!')
                return redirect(f'/id{pk}/change')
            else:
                messages.error(request, 'Неизвестная ошибка!')
                return redirect(f'/id{pk}/change')
            changes = form.save()
            context = {
                'this_user': request.user,
                'page_title': page_title,
            }

            change_username = form.cleaned_data.get('change_username')
            if change_username and not User.objects.filter(username=change_username) and len(change_username) > 3:
                User.objects.filter(id=request.user.id).update(username=change_username)
            elif request.user.username == change_username or change_username == '':
                pass
            else:
                messages.error(request, 'Имя пользователя введено не корректно или оно уже занято!')
                return redirect(f'/id{pk}/change', context)

            change_grade = form.cleaned_data.get('change_grade')
            if change_grade and change_grade.isdigit() and (0 < int(change_grade) < 12):
                Customer.objects.filter(id=request.user.customer.id).update(grade=change_grade)
            elif change_grade == '' or request.user.customer.grade == change_grade:
                pass
            else:
                messages.error(request, 'Такого класса не существует!')
                return redirect(f'/id{pk}/change', context)

            change_image = form.instance.change_user_image
            if change_image:
                if user.customer.user_image.url != 'media/user_images/None_user.jpg':
                    try:
                        os.remove(BASE_DIR + user.customer.user_image.url)
                        #messages.success(request, 'Старое фото удалено')
                    except OSError:
                        messages.error(request, 'Ошибка при удалении старого фото!')
                Customer.objects.filter(id=request.user.customer.id).update(user_image=change_image)
            # else:
                # messages.error(request, 'Фото не квадратное или что-то пошло не так при его загрузке!')
            request.user.customer.user_changes.add(changes)

            messages.success(request, 'Изменения сохранены')
            return redirect(f'/id{pk}', context)

    return render(request, 'mathhack/auth/change_user_page.html',
                  {'form': form, 'this_user': request.user, 'page_title': page_title, 'pk': pk})


class OneTaskByIdView(View):
    """Одно задание по ID"""

    def get(self, request):
        if request.method == 'GET':
            if 'q' in request.GET and request.GET['q'].isdigit():
                temp = int(request.GET['q'])
                task = Task.objects.filter(id=temp)
                if len(task) != 0:
                    task = task.get(id=temp)
                    page_title = f"Задание {temp}"
                    return render(request, 'mathhack/task_num.html',
                                  {'task': task, 'page_title': page_title, })
                else:
                    page_title = "Задание не найдено"
                    return render(request, 'mathhack/errors/task_not_found.html',
                                  {'page_title': page_title, 'message': page_title, }, )
            else:
                page_title = "Задание не найдено"
                message = 'Номер задания введен не корректно'
                return render(request, 'mathhack/errors/task_not_found.html',
                              {'page_title': page_title, 'message': message, }, )


class TypeOfTasksView(View):
    """Список заданий определенного номера/типа"""

    def get(self, request, pk):
        tasks = Task.objects.filter(type=pk)
        page_title = f"Все {str(pk)} задания"

        return render(request, 'mathhack/tasks_by_type.html',
                      {'tasks_list': tasks, 'page_title': page_title, 'pk': pk})


def MakeSovledStr(variant, array_of_solved_tasks):
    """It's used in another function for make SolvedStr with + and -.
        For example:++-+-+++-+-+2233355"""
    tmp_str = ''
    total = 0
    for task in range(1, len(array_of_solved_tasks) - 7 + 1):
        if str(variant.tasks.get(type=task).answer).lower().strip() == str(
                array_of_solved_tasks[task - 1]).lower().strip():
            tmp_str += '+'
            total += 1
        else:
            tmp_str += '-'
    for task in range(13, len(array_of_solved_tasks) + 1):
        if array_of_solved_tasks[task - 1] == '':
            array_of_solved_tasks[task - 1] = '0'
        tmp_str += str(array_of_solved_tasks[task - 1])
        total += int(array_of_solved_tasks[task - 1])
    return tmp_str, total


def SolvingOneVariant(request, pk):
    variant = Variant.objects.get(id=pk)
    tasks = variant.tasks.all()
    page_title = 'Вариант ' + str(variant.id)

    form = SolvingVariantForm()

    if request.method == "POST":
        form = SolvingVariantForm(request.POST)
        if form.is_valid():
            solved_variant = form.save()
            new_str, total = MakeSovledStr(variant,
                                           [form.cleaned_data.get('task1'), form.cleaned_data.get('task2'),
                                            form.cleaned_data.get('task3'), form.cleaned_data.get('task4'),
                                            form.cleaned_data.get('task5'), form.cleaned_data.get('task6'),
                                            form.cleaned_data.get('task7'), form.cleaned_data.get('task8'),
                                            form.cleaned_data.get('task9'), form.cleaned_data.get('task10'),
                                            form.cleaned_data.get('task11'), form.cleaned_data.get('task12'),
                                            form.cleaned_data.get('task13'), form.cleaned_data.get('task14'),
                                            form.cleaned_data.get('task15'), form.cleaned_data.get('task16'),
                                            form.cleaned_data.get('task17'), form.cleaned_data.get('task18'),
                                            form.cleaned_data.get('task19'), ])
            if request.user.is_authenticated:
                user = request.user.customer
                user.solved_variants.add(solved_variant)
                Customer.objects.filter(user=request.user).update(points_sum=user.points_sum + total)
                Customer.objects.filter(user=request.user).update(points_num=user.points_num + 1)
            SolvingVariant.objects.filter(id=solved_variant.id).update(solving_str=new_str)
            SolvingVariant.objects.filter(id=solved_variant.id).update(total=total)
            SolvingVariant.objects.get(id=solved_variant.id).variant.add(variant)
            solved_variant = SolvingVariant.objects.get(id=solved_variant.id)

            return redirect(f'/{pk}_variant_step_3', {'solved_variant': solved_variant})

    return render(request, 'mathhack/variant_solving/variant_solving_1.html',
                  {'form': form, 'variant': variant, 'tasks': tasks, 'page_title': page_title})


def TotalSolvigVariant(request, pk):
    variant = Variant.objects.get(id=pk)
    page_title = f'Вариант {variant.id}'

    if request.user.is_authenticated:
        solved_variant = request.user.customer.solved_variants.latest('date')
    else:
        solved_variant = SolvingVariant.objects.latest('date')

    context = {'variant': variant,
               'page_title': page_title,
               'solved_variant': solved_variant,
               'stask1': solved_variant.solving_str[0],
               'stask2': solved_variant.solving_str[1],
               'stask3': solved_variant.solving_str[2],
               'stask4': solved_variant.solving_str[3],
               'stask5': solved_variant.solving_str[4],
               'stask6': solved_variant.solving_str[5],
               'stask7': solved_variant.solving_str[6],
               'stask8': solved_variant.solving_str[7],
               'stask9': solved_variant.solving_str[8],
               'stask10': solved_variant.solving_str[9],
               'stask11': solved_variant.solving_str[10],
               'stask12': solved_variant.solving_str[11],
               'stask13': solved_variant.solving_str[12],
               'stask14': solved_variant.solving_str[13],
               'stask15': solved_variant.solving_str[14],
               'stask16': solved_variant.solving_str[15],
               'stask17': solved_variant.solving_str[16],
               'stask18': solved_variant.solving_str[17],
               'stask19': solved_variant.solving_str[18],
               }

    return render(request, 'mathhack/variant_solving/variant_solving_3.html', context)

def SuccessRegMessage(name):
    name = name.lower()
    '''
    if name.find('katya') != -1:
        message = f''
        return message
    '''
    message = f'Пользователь {name} успешно создан'
    return message

def registrPage(request):
    """REGISTRATION"""
    if request.user.is_authenticated:
        return redirect('/')
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user, )

            messages.success(request, SuccessRegMessage(username))
            return redirect('/login')

    return render(request, 'mathhack/auth/registration.html',
                  {'form': form})


def loginPage(request):
    """LOGIN"""

    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, "Неверный email или пароль")

    return render(request, 'mathhack/auth/login.html',
                  {})


def logoutUser(request):
    logout(request)
    return redirect('/login')
