from django.urls import path

from apps.csat.views import ApplyApplicationView, ApplicationFormView

urlpatterns = [
    path("apply-application", ApplyApplicationView.as_view()),
    path("application_form", ApplicationFormView.as_view())
    ]