from django.shortcuts import render, get_object_or_404, redirect
from .models import Flight, Reservation, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# 首页，展示所有航班信息
def home(request):
    flights = Flight.objects.all()  # 获取所有航班数据
    return render(request, 'booking/home.html', {'flights': flights})

# 预定航班
@login_required
def reserve(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)  # 获取指定航班信息
    if request.method == 'POST':
        # 获取表单数据
        passenger_name = request.POST.get('passenger_name')  # 获取乘客名称
        seat_number = request.POST.get('seat_number')  # 获取座位号
        ticket_number = request.POST.get('ticket_number')  # 获取票号
        seating = request.POST.get('seating')  # 获取座位类型
        # 创建预定记录
        Reservation.objects.create(
            user=request.user,
            flight=flight,
            seat_number=seat_number,
            ticket_number=ticket_number,
            seating=seating,  # 座位类型
            passenger_name=passenger_name  # 乘客姓名
        )
        return redirect('my_reservations')  # 重定向到我的预定页面
    return render(request, 'booking/reserve.html', {'flight': flight})

# 用户查看自己的所有预定
@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)  # 获取当前用户的所有预定
    return render(request, 'booking/my_reservations.html', {'reservations': reservations})

# 用户添加评论
@login_required
def add_comment(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)  # 获取指定航班信息
    if request.method == 'POST':
        # 获取评论内容和评分
        comment_text = request.POST['comment_text']
        rating = request.POST['rating']
        # 创建评论记录
        Comment.objects.create(user=request.user, flight=flight, comment_text=comment_text, rating=rating)
        return redirect('home')  # 重定向到首页
    return render(request, 'booking/add_comment.html', {'flight': flight})

# 取消预定
@login_required
def cancel_reservation(request, reservation_id):
    # 获取当前用户的预定记录，如果没有找到则返回404
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.delete()  # 删除该预定记录
    return redirect('my_reservations')  # 重定向到我的预定页面
