import time
from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import telebot

last_alert = 0


@api_view(["GET"])
def Dlist(request):
    all_data = Dht11.objects.all()
    data = DHT11serialize(all_data, many=True).data
    return Response({"data": data})


@api_view(["GET"])
def Dlatest(request):
    last = Dht11.objects.order_by("-id").first()
    if last is None:
        return Response({"data": None})
    return Response({"data": DHT11serialize(last).data})


class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize

    def perform_create(self, serializer):
        global last_alert
        data = serializer.save()
        temperature = data.temp

        if temperature is not None and temperature > 25 and time.time() - last_alert > 60:
            last_alert = time.time()
            message = f"Alerte ! Temperature = {temperature} °C"

            try:
                send_mail(
                    subject="Alerte Temperature",
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["echadlihanan@gmail.com"],
                )
                print("Mail envoye")
            except Exception as e:
                print("ERREUR MAIL :", e)

            try:
                bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)
                bot.send_message(settings.TELEGRAM_CHAT_ID, message)
                print("Telegram envoye")
            except Exception as e:
                print("ERREUR TELEGRAM :", e)