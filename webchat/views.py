from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from user.models import User


def room(request, room_name, user_name):
    print('****')
    room_json = mark_safe(json.dumps(room_name))
    user_json = mark_safe(json.dumps(user_name))

    online = User.objects.filter(is_login=1)
    offline = User.objects.filter(is_login=0)
    data = User.objects.get(username=user_name)
    return render(request, 'chat/room.html', {
        'room_json': room_json,
        'user_json': user_json,
        'roomname': room_name,
        'username': user_name,
        'online': online,
        'offline': offline,
        'data':data,
    })
