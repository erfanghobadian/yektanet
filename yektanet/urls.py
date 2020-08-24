"""yektanet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from User.views import SignUpPersonView, SignUpCompanyView, EditProfile
from Work.views import WorkDetail, WorkList, WorkDelete, WorkUpdate, WorkCreate, SubmitWork, ListApplications


urlpatterns = [
    path('admin/', admin.site.urls),
    path('SignUpPerson/', SignUpPersonView.as_view()),
    path('SignUpCompany/', SignUpCompanyView.as_view()),
    # path('Login/', Login.as_view()),
    path('', include('rest_framework.urls')),
    path('works/', WorkList.as_view()),
    path('works/create/', WorkCreate.as_view()),
    path('works/<pk>/', WorkDetail.as_view()),
    path('works/<pk>/delete/', WorkDelete.as_view()),
    path('works/<pk>/edit/', WorkUpdate.as_view()),
    path('profile/', EditProfile.as_view()),
    path('worksubmit/', SubmitWork.as_view()),
    path('workapplications/', ListApplications.as_view()),

]
