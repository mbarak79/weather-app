from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.


def get_html_content(request):
    city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content


def home(request):
    result = None
    if 'city' in request.GET:
        html_content = get_html_content(request)
        soup = BeautifulSoup(html_content, 'html.parser')
        result = dict()
        result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
        result['temp_now'] = (int(soup.find("span", attrs={"id": "wob_tm"}).text) - 32) * 5/9
        result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
        result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    return render(request, 'home.html', {'result': result})


