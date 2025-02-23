from django.urls import path
from .views import (
    survey_list, survey_detail, submit_response,
    response_list, thank_you, admin_response_list
)

urlpatterns = [
    path('', survey_list, name='survey_list'),
    path('survey/<int:survey_id>/', survey_detail, name='survey_detail'),
    path('survey/<int:survey_id>/submit/', submit_response, name='submit_response'),
    path('thank-you/', thank_you, name='thank_you'),
    path('survey/<int:survey_id>/responses/', response_list, name='response_list'),
    path('survey/<int:survey_id>/responses/admin/', admin_response_list, name='admin_response_list'),
    
]
