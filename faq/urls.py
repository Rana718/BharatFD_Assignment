from django.urls import path
from .views import health, FAQListCreateView

urlpatterns = [
    path('health/', health, name='health'),
    path('faqs/', FAQListCreateView.as_view(), name='faq-list-create'),
]