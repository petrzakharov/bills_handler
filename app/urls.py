from django.urls import path

from app import views

urlpatterns = [
    path("billupload/", views.BillUploadView.as_view(), name="bill-upload"),
    path("billview/", views.BillReadView.as_view(), name="bill-view")
]
