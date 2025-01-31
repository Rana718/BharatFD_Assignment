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

    async def translate_faq(self, faq, target_lang):
        translated_question = await translate_text(faq['question'], target_lang)
        translated_answer = await translate_text(faq['answer'], target_lang)
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
            
            translation_tasks = [self.translate_faq(faq, target_lang) for faq in data]
            translated_data = loop.run_until_complete(asyncio.gather(*translation_tasks))
            loop.close()
            
            return Response(translated_data)
        
        return Response(data)