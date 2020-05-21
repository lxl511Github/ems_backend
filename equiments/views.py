# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from equiments.models import equ, loanMsg,Repay
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
import json
from collections import Counter
import datetime

# Create your views here.


# 出借信息
class LoanMsg(View):
    def get(self, request):
        s_name = request.GET.get('name')
        s_time = request.GET.get('s_time')
        e_time = request.GET.get('e_time')
        res = {}
        print("step0")
        try:
            list = []
            print("step1")
            if s_name is not None or s_time is not None:
                eNList = []
                json_dict = {}
                if s_time and s_name:
                    dic_loan = loanMsg.objects.filter(date__range=(s_time, e_time), loanName__contains=s_name)
                    for eN in dic_loan:
                        eNList.append(eN.equ_num)
                    dic_equ = equ.objects.filter(serialNum__in=eNList)
                elif s_time:
                    dic_loan = loanMsg.objects.filter(date__range=(s_time, e_time))
                    for eN in dic_loan:
                        eNList.append(eN.equ_num)
                    dic_equ = equ.objects.filter(serialNum__in=eNList)
                else:
                    dic_loan = loanMsg.objects.filter(loanName__contains=s_name)
                    # print(dic_loan)
                    for eN in dic_loan:
                        eNList.append(eN.equ_num)
                    dic_equ = equ.objects.filter(serialNum__in=eNList)
                for el in dic_loan:
                    json_dict["loanName"] = el.loanName
                    json_dict["jobNum"] = el.jobNum
                    json_dict["department"] = el.department
                    json_dict["date"] = el.date
                    for e2 in dic_equ:
                        if e2.serialNum == el.equ_num:
                            json_dict['serialNum'] = e2.serialNum
                            json_dict["name"] = e2.name
                            json_dict["equ_type"] = e2.equ_type
                    list.append(json_dict)
                    res['list'] = list
            else:
                dic_equ = equ.objects.filter(equ_status="3")
                dic_loan = loanMsg.objects.all()
                for e in dic_equ:
                    json_dict = {}
                    for ex in dic_loan:
                        if ex.equ_num == e.serialNum:
                            json_dict["loanName"] = ex.loanName
                            json_dict["jobNum"] = ex.jobNum
                            json_dict["department"] = ex.department
                            json_dict["date"] = ex.date
                    json_dict['serialNum'] = e.serialNum
                    json_dict["name"] = e.name
                    json_dict["equ_type"] = e.equ_type
                    list.append(json_dict)
                    res['list'] = list
            res['msg'] = 'success'
            res['error_num'] = 0
        except Exception as e:
            res['msg'] = str(e)
            res['error_num'] = 1
        print(res)
        return HttpResponse(json.dumps(res, cls=DateEncoder), content_type="application/json")
    # 对借出信息进行登记

    def post(self, request):
        print("post")
        obj = json.loads(request.body)
        loan_name = obj.get('loanName')
        job_num = obj.get('jobNum')
        department = obj.get('department')
        date = obj.get('date')
        equ_num = obj.get('equ_num')
        dic = equ.objects.filter(serialNum=obj.get('equ_num'))
        num = dic.first().equ_status
        name = dic.first().name
        try:
            if dic.exists():
                if num == "1":
                    dic.update(equ_status="3")
                    loanMsg(loanName=loan_name, jobNum=job_num, department=department, date=date,
                            category=equ_category(equ_num), equName=name, equ_num=equ_num).save()
                    res = {"code": 200}
                else:
                    res = {"code": 0}
        except Exception as e:
            print(e)
            res = {
                "code": 0
            }
        return HttpResponse(json.dumps(res), content_type="application/json")

    def fn(self, param):
        res = {}
        list = []
        dic_loan = loanMsg.objects.all()
        for e in param:
            json_dict = {}
            for ex in dic_loan:
                if ex.equ_num == e.serialNum:
                    print("OK")
                    json_dict["loanName"] = ex.loanName
                    json_dict["jobNum"] = ex.jobNum
                    json_dict["department"] = ex.department
                    json_dict["date"] = ex.date
            json_dict['serialNum'] = e.serialNum
            json_dict["name"] = e.name
            json_dict["equ_type"] = e.equ_type
            list.append(json_dict)
            res['list'] = list
        return res


# 查询根据编号某个设备的类别
def equ_category(params):
    obj = equ.objects.filter(serialNum=params)[0]
    return obj.category


# 判断此设备状态
def equ_status(params):
    obj = equ.objects.filter(serialNum=params)[0]
    status = obj.equ_status
    return status
# ==============================归还设备操作=====================================================


class RepayMsg(View):
    def post(self, request):
        obj = json.loads(request.body.decode("utf-8"))
        serialNum = obj.get('serialNum')
        name = obj.get('name')
        equ_status = obj.get('equ_status')
        descText = obj.get('descText')
        date = obj.get('date')
        admin = obj.get('admin')
        dic = equ.objects.filter(serialNum=serialNum)
        try:
            if dic.exists():
                print("存现")
                dic.update(equ_status=equ_status)
                Repay(serialNum=serialNum, equ_status=equ_status, name=name, desc=descText, date=date, admin=admin).save()
                res = {
                    "code": "200"
                }
        except Exception as e:
            res = {
                "code": 0,
                "errMsg": e
            }
        return HttpResponse(json.dumps(res), content_type="application/json")

# ==============================添加操作=====================================================


# 新增？修改
class AddEqu(View):
    def post(self, request):
        obj = json.loads(request.body.decode("utf-8"))
        # id = obj.get('id')
        serial_num = obj.get('serialNum')
        name = obj.get('name')
        equ_type = obj.get('equ_type')
        add_per = obj.get('admin_per')
        equ_status = obj.get('equ_status')
        category = obj.get('category')
        try:
            dic = equ.objects.filter(serialNum=serial_num)
            if dic.exists():
                print(dic)
                dic.update(name=name, equ_type=equ_type, add_time=timezone.now(), admin_per=add_per,
                           equ_status=equ_status, category=category)
            else:
                print("2")
                equ(serialNum=serial_num, name=name, equ_type=equ_type, add_time=timezone.now(), admin_per=add_per,
                    equ_status=equ_status, category=category).save()
            res = {
                "code": "200",
            }
        except Exception as e:
            res = {
                "code": 0,
                "errMsg": e
            }
        return HttpResponse(json.dumps(res, cls=DateEncoder), content_type="application/json")


# ==============================删除操作=====================================================


class DelEqu(View):
    def get(self, request):
        ids = request.GET.get('ids')
        ids_list = ids.split(',')
        if len(ids_list) > 0:
            res = batch_remove(ids_list)
        return HttpResponse(json.dumps(res, cls=DateEncoder), content_type="application/json")


def batch_remove(param):
    for id in param:
        print(id)
        # equ_date = equ.objects.get(id=id)
        # for item in loanMsg.objects.get(equ_num=equ_num):
        #     print(item)
        equ.objects.get(id=id).delete()
    res = {
        "code": '200',
    }

    return res


def del_equ(request):

    if(request.method == "POST"):
        obj = json.loads(request.body.decode("utf-8"))
        delete_id = obj.get('curNum')
        print(delete_id)
        try:
            equ.objects.filter(serialNum=delete_id).delete()
            res = {
                "code": 200
            }
        except Exception as e:
            res = {
                "code": 0,
                "errMsg": e
            }
    return HttpResponse(json.dumps(res), content_type="application/json")
# # ==============================查询操作=====================================================


class ShowEqu(View):
    def get(self, request):
        response = {}
        s_name = request.GET.get('name')
        s_status = request.GET.get('status')
        try:
            if s_name or s_status:
                if s_name and s_status:
                    equs = equ.objects.filter(equ_status=s_status, name__contains=s_name)
                    response = fn(equs)
                elif s_status:
                    equs = equ.objects.filter(equ_status=s_status)
                    response = fn(equs)
                    print(response)
                else:
                    equs = equ.objects.filter(name__contains=s_name)
                    response = fn(equs)
            else:
                equs = equ.objects.all()
                response = fn(equs)
        except Exception as e:
            response['msg'] = str(e)
            response['error_num'] = 1

        return HttpResponse(json.dumps(response, cls=DateEncoder), content_type="application/json")


def loan_msg(request):
    response = {}
    e_num = request.GET.get('equ_num')
    e = [x for x in loanMsg.objects.filter(equ_num=e_num)]
    list = []
    # if len(e) == 1 and e[0].equ_num == e_num:
    if len(e) != 0:
        json_dict = {}
        json_dict['loanName'] = e[-1].loanName
        json_dict['jobNum'] = e[-1].jobNum
        json_dict['department'] = e[-1].department
        json_dict['date'] = e[-1].date
        json_dict['equ_num'] = e[-1].equ_num
        list.append(json_dict)
        response['list'] = list
        response['msg'] = 'success'
        response['error_num'] = 0
    else:
        response['msg'] = 'error'
        response['error_num'] = 1
    return HttpResponse(json.dumps(response, cls=DateEncoder), content_type="application/json")


def fn(para):
    list = []
    res = {}
    for e in para:
        json_dict = {}
        json_dict['id'] = e.id
        json_dict['serialNum'] = e.serialNum
        json_dict["name"] = e.name
        json_dict["equ_type"] = e.equ_type
        json_dict["add_time"] = e.add_time
        json_dict["admin_per"] = e.admin_per
        json_dict["equ_status"] = e.equ_status
        list.append(json_dict)
        res['list'] = list
    res['msg'] = 'success'
    res['error_num'] = 0
    return res

# 权限验证
# 判断是否有删除权限

# ==============================修改操作=====================================================


# 重写序列化类
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


# ==============================数据分析操作=====================================================
class Echart(View):

    def get(self, request):
        res = {}
        category = request.GET.get('category')
        print(category)
        print(equ_type(category))
        x_data_list = equ_type(category)
        # 各型号设备状态为正常的数量
        no_use_list = list(equ_num(equ_type(category), "1").values())
        # 各型号设备状态为借出的数量
        in_use_list = list(equ_num(equ_type(category), "3").values())
        # 各型号设备状态为异常的数量
        damage_list = list(equ_num(equ_type(category), ["2" "4", "5"]).values())
        res['x_data_list'] = x_data_list
        res['no_use_list'] = no_use_list
        res['in_use_list'] = in_use_list
        res['damage_list'] = damage_list

        # data_list = usage_amount(category)
        # useable_list, damage_list, in_use_list = itemEqu(category)
        # print(useable_list, damage_list, in_use_list)
        # res['x_data'] =
        # res['y_data1'] = y_data1
        res["code"] = 200
        print("res:", res)
        return HttpResponse(json.dumps(res), content_type="application/json")

# 先查有多少种目标类的型号
# 再根据型号查询此类useable,damage,in_use的数量


# 查询有多少类
def equ_type(params):
    type_data = equ.objects.filter(category=params)
    s_type_list = set([e.name for e in type_data])
    type_list = list(s_type_list)
    return type_list


# 根据类别查询各类的数量
def equ_num(type_list, params):
    value_list = []
    for item_type in type_list:
        data_list = len(equ.objects.filter(name=item_type, equ_status__in=params))
        value_list.append(data_list)
    result = dict(zip(type_list, value_list))
    return result









# 将数据进行统计
def count_data(params):
    data_list = [x.name for x in params]
    num_count = Counter(data_list).most_common(10)
    return d_list(num_count)


# 将数据转换成列表
def d_list(params):
    x_data = []
    y_data1 = []
    for x, y in params:
        x_data.append(x)
        y_data1.append(y)
    return x_data, y_data1


# 获取选中类别的排名前10位的设备(按照使用的 数量进行排序)
def usage_amount(params):
    today = timezone.now()
    weekdelta = timezone.now()-datetime.timedelta(weeks=4)
    recent_list = loanMsg.objects.filter(date__gte=weekdelta, date__lte=today, category=params)
    # 各类设备在一个月内借出次数
    data_list = [x.equName for x in recent_list]
    num_count = Counter(data_list).most_common(10)
    return num_count


# 在库各类设备各状态的设备数量
def itemEqu(params):
    # 查询目标设备的可借用的，使用中的，损坏的数量
    useable_list = equ.objects.filter(category=params, equ_status="1")
    damage_list = equ.objects.filter(category=params, equ_status="2")
    in_use_list = equ.objects.filter(category=params, equ_status="3")
    return count_data(useable_list), count_data(damage_list), count_data(in_use_list)



