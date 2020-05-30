from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from app.forms import Amount
import requests
from ngrok_tutorial import settings
import locale


def convert_btc_to_ngn(btc):
    """
    :param btc
    :returns: naira equivalent of btc

    """
    try:
        btc_url = "https://blockchain.info/ticker"

        url = f"http://api.currencylayer.com/live?access_key={settings.API_KEY}&currencies=NGN"

        locale.setlocale(locale.LC_ALL, '')

        btc_request = requests.get(btc_url).json()
        one_btc_to_dollar = round(btc_request.get("USD").get("15m"), 2)
        print(one_btc_to_dollar, "1 btcc to dolss")

        dollar_request = requests.get(url).json()
        one_dollar_to_ngn = round(dollar_request["quotes"]["USDNGN"], 2)
        print(one_dollar_to_ngn, 'dols to nairaaaaaaaa')

        btc_dollar_value = round(btc * one_btc_to_dollar, 2)
        print(btc_dollar_value, 'final btccccccccc to dols')
        ngn_value = round(btc_dollar_value * one_dollar_to_ngn, 2)

        response = dict(status="success", BTC=btc, NGN=ngn_value)
        return response
    except Exception as e:
        print(e, "error message")
        return dict(status="error", message=e)


# Create your views here.

def homepage(request):
    """
    renders the homepage
    :param request:
    :return:
    """
    context = dict()
    if request.method == "POST":

        form = Amount(request.POST)
        if form.is_valid():
            btc = form.cleaned_data.get("btc_amount")
            naira_value = convert_btc_to_ngn(btc)
            values = dict(naira_equivalent=naira_value.get("NGN", 0), btc=naira_value.get("BTC", 0), form=form)
            context.update(values)

    else:
        form = Amount()
        context.update(form=form)

    return render(request, 'ngrok_tutorial/homepage.html', context)


def ajax_request(request):
    """

    :param request:
    :return:
    """
    if request.is_ajax and request.method == "POST":
        form = Amount(request.POST)
        if form.is_valid():
            btc = form.cleaned_data.get("btc_amount")
            naira_value = convert_btc_to_ngn(btc)
            if naira_value.get("status") == "success":
                values = {"naira_equivalent": naira_value.get("NGN", 0),
                          "btc": naira_value.get("BTC", 0),
                          }
                # serialized_instance = serializers.serialize('json', [values])
                return JsonResponse({"instance": values}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": ""}, status=400)





