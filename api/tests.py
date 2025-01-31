import pytest
from rest_framework import status
from rest_framework.test import APIClient
from api.models import FAQ
from django.core.cache import cache
from django.conf import settings


@pytest.fixture
def client():
    """Fixture to get the APIClient instance"""

    return APIClient()


@pytest.fixture
def faq_data():
    """Fixture to create a sample FAQ entry"""

    return FAQ.objects.create(
        question="What is Django?",
        answer="Django is a high-level Python Web framework.",
    )


@pytest.mark.django_db
def test_health_check(client):
    """Test the health check endpoint"""

    response = client.get('/api/health/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'status': 'ok'}


@pytest.mark.django_db
def test_faq_list(client, faq_data):
    """Test listing all FAQs"""

    response = client.get('/api/faqs/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert response.data[0]['question'] == faq_data.question
    assert response.data[0]['answer'] == faq_data.answer


@pytest.mark.django_db
def test_faq_list_translation(client, faq_data):
    """Test FAQ list translation functionality"""

    target_lang = 'es'
    cache.set(f"translation:{faq_data.question}:{target_lang}",
              "¿Qué es Django?", timeout=settings.CACHE_TTL)
    cache.set(f"translation:{faq_data.answer}:{target_lang}",
              "Django es un marco web de Python de alto nivel.", timeout=settings.CACHE_TTL)

    response = client.get(f'/api/faqs/?lang={target_lang}')
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['question'] == "¿Qué es Django?"
    assert response.data[0]['answer'] == "Django es un marco web de Python de alto nivel."


@pytest.mark.django_db
def test_faq_detail(client, faq_data):
    """Test retrieving a single FAQ"""

    response = client.get(f'/api/faqs/{faq_data.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['question'] == faq_data.question
    assert response.data['answer'] == faq_data.answer


@pytest.mark.django_db
def test_faq_detail_translation(client, faq_data):
    """Test FAQ detail translation functionality"""

    target_lang = 'fr'

    cache.set(f"translation:{faq_data.question}:{target_lang}",
              "Qu'est-ce que Django?", timeout=settings.CACHE_TTL)
    cache.set(f"translation:{faq_data.answer}:{target_lang}",
              "Django est un framework web Python de haut niveau.", timeout=settings.CACHE_TTL)

    response = client.get(f'/api/faqs/{faq_data.id}/?lang={target_lang}')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['question'] == "Qu'est-ce que Django?"
    assert response.data['answer'] == "Django est un framework web Python de haut niveau."


@pytest.mark.django_db
def test_faq_create(client):
    """Test creating a new FAQ entry"""

    new_faq = {
        "question": "How do I use Django?",
        "answer": "You can use Django by following the documentation at django.org.",
    }
    response = client.post('/api/faqs/', new_faq, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['question'] == new_faq['question']
    assert response.data['answer'] == new_faq['answer']


@pytest.mark.django_db
def test_faq_update(client, faq_data):
    """Test updating an existing FAQ"""

    updated_faq = {
        "question": "What is Django Framework?",
        "answer": "Django is a popular Python framework for building web applications.",
    }
    response = client.put(
        f'/api/faqs/{faq_data.id}/', updated_faq, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['question'] == updated_faq['question']
    assert response.data['answer'] == updated_faq['answer']


@pytest.mark.django_db
def test_faq_delete(client, faq_data):
    """Test deleting an FAQ"""

    response = client.delete(f'/api/faqs/{faq_data.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    with pytest.raises(FAQ.DoesNotExist):
        FAQ.objects.get(id=faq_data.id)
