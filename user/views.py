from django.shortcuts import render, redirect
from user.models import User


def login_check(func):
    def inner(request, *args, **kwargs):
        ret = request.session.get('is_login')
        print(func)
        if ret == "1":
            return func(request, *args, **kwargs)
        else:
            return redirect("/")
    return inner


@login_check
def friendprofile(request, username, friendname):
    user_obj = User.objects.get(username=username)
    fri_obj = User.objects.get(username=friendname)
    data = User.objects.get(username=username)
    online = User.objects.filter(is_login=1)
    offline = User.objects.filter(is_login=0)
    return render(request, 'user/friendprofile.html', {
        'username': username,
        'data': data,
        'user_obj': user_obj,
        'fri_obj': fri_obj,
        'online': online,
        'offline': offline,
    })


def login(request):
    error_msg = ''
    if request.method == 'POST':
        input_email = request.POST.get('email')
        input_password = request.POST.get('pwd')

        try:
            user_obj = User.objects.get(email=input_email)
        except:
            error_msg = '无此账号'
            return render(request, 'user/login.html', {'error_msg': error_msg})

        if input_password == user_obj.password:
            # 修改session
            request.session['is_login'] = '1'

            user_obj.is_login = 1
            user_obj.save()
            username = user_obj.username

            online = User.objects.filter(is_login=1)
            offline = User.objects.filter(is_login=0)
            data = User.objects.get(username=username)
            return render(request, 'chat/index.html', {
                'username': username,
                'data':data,
                'online': online,
                'offline': offline
            })
        else:
            error_msg = '账号或密码错误'
    return render(request, 'user/login.html', {'error_msg': error_msg})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        username1 = User.objects.filter(username=username)
        if username1:
            if username == username1[0].username:
                error_msg = '用户名已存在'
                return render(request, 'user/register.html', {'error': error_msg})
        email = request.POST.get('email')
        email1 = User.objects.filter(email=email)
        if email1:
            if email == email1[0].email:
                error_msg = '邮箱已存在'
                return render(request, 'user/register.html', {'error': error_msg})
        password = request.POST.get('pwd')
        gender = int(request.POST.get('gender'))
        if int(gender) == 0:
            portrait = '/static/img/man.jpg'
        else:
            portrait = '/static/img/woman.jpg'
        User.objects.create(username=username, email=email, portrait=portrait, gender=gender, password=password)
        return render(request, 'user/login.html')
    return render(request, 'user/register.html')


def logout(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user_obj = User.objects.get(username=username)
        user_obj.is_login = 0
        user_obj.save()
        # 清空session
        request.session.flush()
        return render(request, 'user/login.html')


@login_check
def userprofile(request, username):
    data = User.objects.get(username=username)
    if request.method == 'POST':
        online = User.objects.filter(is_login=1)
        offline = User.objects.filter(is_login=0)
        email = request.POST.get('email')
        user_obj = User.objects.get(email=email)

        re_password = request.POST.get('re_pwd')
        re_password_2 = request.POST.get('re_pwd_2')

        if re_password == re_password_2:
            user_obj.password = re_password
            user_obj.save()
            message = '密码修改成功'
        else:
            message = '两次密码不一致，修改密码失败'
        return render(request, 'user/userprofile.html', {
            'username': username,
            'data': data,
            'user_obj': user_obj,
            'online': online,
            'offline': offline,
            'message': message,
        })
    if request.method == 'GET':
        try:
            user_obj = User.objects.get(username=username)
        except:
            return redirect('/')

        online = User.objects.filter(is_login=1)
        offline = User.objects.filter(is_login=0)
        return render(request, 'user/userprofile.html', {
            'username': username,
            'data': data,
            'user_obj': user_obj,
            'online': online,
            'offline': offline,
        })


@login_check
def back2chat(request, username):
    online = User.objects.filter(is_login=1)
    offline = User.objects.filter(is_login=0)
    data = User.objects.get(username=username)
    return render(request, 'chat/index.html', {
        'username': username,
        'data': data,
        'online': online,
        'offline': offline,
    })


