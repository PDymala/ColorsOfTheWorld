import random

from django.shortcuts import render
from django.http import HttpResponse
from .models import Cluster, SearchResult, Website, Quote
from django.utils import timezone
from . import color_fetcher


# Trzeba jakos aby pokazywało ostatnie dobre z datą. ? Aby nie wrzucało do bazy pustych najlepiej
# TODO pobieranie quote losowo z calej grupy
def index(request):
    # return HttpResponse('new checker')

    #  for website in websites:
    websites_to_show = Website.objects.distinct().filter(show=True)
    # print(len(websites_to_show))

    # https://stackoverflow.com/questions/687295/how-do-i-do-a-not-equal-in-django-queryset-filtering

    final_array = []
    for website in websites_to_show:
        # search_website = Website.objects.get(url=website.url)
        # search_result = SearchResult.objects.get(url=search_website)
        search_result = SearchResult.objects.filter(url=website).latest('search_date')
        search_result_clusters = Cluster.objects.filter(search_result_id=search_result).all

        if search_result.average_color == '#000000':
            continue

        temp_array = {
            'date': search_result.search_date,
            'url': website.url,
            'average_color': search_result.average_color,
            'std': search_result.std_color,
            'clusters': search_result_clusters}

        final_array.append(temp_array)

    title = random_color_string('Colors Of The World')

    quote_database = Quote.objects.all()
    random_quote = random.choice(quote_database)


    return render(request, 'index.html', {
        'final_array': final_array,
        'title': title,
        'quote': random_quote
    })


# TODO zmienic z GET na poST lub innne? Sprawdac czy danego dnia juz bylo. Jezeli tak, to nic nie robic
# TODO cyz mozna jakos zabezpieczeczyc starter?

def starter(request):
    if request.method == 'GET':

        websites_to_search = Website.objects.distinct().filter(search=True)
        # print(len(websites_to_show))

        for website in websites_to_search:

            # string = 'https://www.nbcnews.com/'
            colors = color_fetcher.fetchColor(website.url)
            # temp = [[0,1,5],[5,5,5],[7,5,6]]
            # colors = [temp, [4, 4, 3], [3, 1, 5]]

            # website_to_search = Website()
            # website_to_search.url = string
            # website_to_search.show = True
            # website_to_search.search = True
            # website_to_search.save()

            # to jest klasa,zmienna bo inaczje nie mogl bym jej w kolejcnych funkcach odwolac
            search_result = SearchResult()
            search_result.search_date = timezone.now()
            search_result.url = website
            search_result.average_color = rgb2hex(int(colors[1][0]), int(colors[1][1]), int(colors[1][2]))
            search_result.std_color = rgb2hex(int(colors[2][0]), int(colors[2][1]), int(colors[2][2]))
            search_result.save()

            # Website.objects.create(
            #     search_results=search_result,
            #     url=string,
            #     show=True,
            #     search=True
            # )

            # TODO Zmienic cluster number na number +1
            counter = 0
            for color in colors[0]:
                Cluster.objects.create(
                    cluster_number=counter,  # cluster number
                    color=rgb2hex(int(color[0]), int(color[1]), int(color[2])),  # color
                    search_result_id=search_result  # url
                )

                counter += 1

        return HttpResponse('Sucess')
    else:
        return HttpResponse("not good")


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def hex2rgb(hexcode):
    return tuple(map(ord, hexcode[1:].decode('hex')))


def random_color_string(string):
    local_map = []
    for letter in string:
        color = rgb2hex(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        local_map.append((letter, color))
    return local_map
