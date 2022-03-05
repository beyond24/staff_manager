"""staff_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from app01.views import depart, staff, pretty, account, task, order, index

urlpatterns = [

    path('admin/', admin.site.urls),

    # 部门管理
    path('depart/list/', depart.departList),
    path('depart/add/', depart.departAdd),
    path('depart/delete/', depart.departDelete),
    #正则表达式<int:nid>
    # http://127.0.0.1:8000/depart/1/edit/
    # http://127.0.0.1:8000/depart/3/edit/
    path('depart/<int:nid>/edit/', depart.departEdit),

    # 用户管理
    path('staff/list/', staff.staffList),
    path('staff/add/', staff.staffAdd),
    path('staff/modelform/add/', staff.staffModelFormAdd),
    path('staff/<int:nid>/edit/', staff.staffEdit),
    path('staff/<int:nid>/delete/', staff.staffDelete),

    # 靓号管理
    path('pretty/list/', pretty.prettyList),
    path('pretty/add/', pretty.prettyAdd),
    path('pretty/<int:nid>/edit/', pretty.prettyEdit),
    path('pretty/<int:nid>/delete/', pretty.prettyDelete),

    # 管理员管理
    # path('admin/list/', admin.adminList),
    # path('admin/add/', admin.adminAdd),
    # path('admin/<int:nid>/edit/', admin.adminEdit),
    # path('admin/<int:nid>/delete/', admin.adminDelete),
    # path('admin/<int:nid>/reset/', admin.adminPasswordReset),

    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.imageCode),

    # 任务表
    path('task/list/', task.taskList),
    path('task/add/', task.taskAdd),

    # 订单表
    path('order/list/', order.orderList),
    path('order/add/', order.orderAdd),
    path('order/delete/', order.orderDelete),
    path('order/details/', order.orderDetails),
    path('order/edit/', order.orderEdit),

    # 自定义中间件的测试
    re_path('index/.*$', index.index)
]