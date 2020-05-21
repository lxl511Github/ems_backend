from django.conf.urls import url
# from .views import LoanMsg
from . import views
urlpatterns = [
    # url(r'show_list', EquListView.as_view(), name="equ_list"),
    url(r'LoanMsg', views.LoanMsg.as_view(), name="LoanMsg"),
    url(r'DelEqu', views.DelEqu.as_view(), name="DelEqu"),
    url(r'AddEqu', views.AddEqu.as_view(), name="AddEqu"),
    url(r'ShowEqu', views.ShowEqu.as_view(), name="ShowEqu"),
    url(r'loan_msg', views.loan_msg, name="loanMsg"),
    url(r'Repay', views.RepayMsg.as_view(), name="repay"),
    url(r'eChart', views.Echart.as_view(), name='eChart')
]
