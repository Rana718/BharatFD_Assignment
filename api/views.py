from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import FAQ
from .serializers import FAQSerializer
from rest_framework import generics
from translations.translate import translate_text
import asyncio


@api_view(['GET'])
def health(request):
    return Response({'status': 'ok'})


class FAQListCreateView(generics.ListCreateAPIView):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()

    def get_cache_key(self, text, target_lang):
        return f"translation:{text}:{target_lang}"

    async def translate_faq(self, faq, target_lang):
        question_cache_key = self.get_cache_key(faq['question'], target_lang)
        cached_question = cache.get(question_cache_key)
        if cached_question:
            translated_question = cached_question
        else:
            translated_question = await translate_text(faq['question'], target_lang)
            cache.set(question_cache_key, translated_question,
                      timeout=settings.CACHE_TTL)

        answer_cache_key = self.get_cache_key(faq['answer'], target_lang)
        cached_answer = cache.get(answer_cache_key)
        if cached_answer:
            translated_answer = cached_answer
        else:
            translated_answer = await translate_text(faq['answer'], target_lang)
            cache.set(answer_cache_key, translated_answer,
                      timeout=settings.CACHE_TTL)

        faq['question'] = translated_question
        faq['answer'] = translated_answer
        return faq

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        target_lang = request.query_params.get('lang')
        if target_lang:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            translation_tasks = [self.translate_faq(
                faq, target_lang) for faq in data]
            translated_data = loop.run_until_complete(
                asyncio.gather(*translation_tasks))
            loop.close()

            return Response(translated_data)

        return Response(data)


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()

    def get_cache_key(self, text, target_lang):
        return f"translation:{text}:{target_lang}"

    async def translate_faq(self, faq, target_lang):

        question_cache_key = self.get_cache_key(faq['question'], target_lang)
        cached_question = cache.get(question_cache_key)
        if cached_question:
            translated_question = cached_question
        else:
            translated_question = await translate_text(faq['question'], target_lang)
            cache.set(question_cache_key, translated_question,
                      timeout=settings.CACHE_TTL)

        answer_cache_key = self.get_cache_key(faq['answer'], target_lang)
        cached_answer = cache.get(answer_cache_key)
        if cached_answer:
            translated_answer = cached_answer
        else:
            translated_answer = await translate_text(faq['answer'], target_lang)
            cache.set(answer_cache_key, translated_answer,
                      timeout=settings.CACHE_TTL)

        faq['question'] = translated_question
        faq['answer'] = translated_answer
        return faq

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        target_lang = request.query_params.get('lang')
        if target_lang:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            translated_data = loop.run_until_complete(
                self.translate_faq(data, target_lang))
            loop.close()

            return Response(translated_data)

        return Response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)
