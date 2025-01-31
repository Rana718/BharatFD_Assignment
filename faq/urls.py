from django.urls import path
from .views import health, FAQListCreateView, FAQDetailView

urlpatterns = [
    path('health/', health, name='health'),
    path('faqs/', FAQListCreateView.as_view(), name='faq-list-create'),
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),
]
