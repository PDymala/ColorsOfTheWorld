import io
import math
import random
from PIL import ImageColor
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
from .models import Cluster, SearchResult, Website, Quote
from django.utils import timezone
from . import color_fetcher
from PIL import Image
import base64


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


class Image_check():
    def __init__(self, site, daily, clusterss):
        self.site = site
        self.daily = daily
        self.clusterss = clusterss



def image_from_database(request):

    images = []
    sites = get_sites_to_check()
    daily = daily_as_pixel(sites)
    clusterss = clusters_as_pixels(sites)


    for x in range(len(sites)):
        images.append(Image_check(site = sites[x], daily=daily[x], clusterss=clusterss[x]))

    title = random_color_string('Colors Of The World')
    return render(request, "image.html", {'images': images, 'title': title})


def get_sites_to_check():
    websites_to_show = Website.objects.distinct().filter(show=True)
    return websites_to_show

def daily_as_pixel(websites_to_show):
    # websites_to_show = Website.objects.distinct().filter(show=True)
    # print(len(websites_to_show))

    # https://stackoverflow.com/questions/687295/how-do-i-do-a-not-equal-in-django-queryset-filtering

    final_array = []
    for website in websites_to_show:
        search_result = SearchResult.objects.filter(url=website)
        search_result_len = SearchResult.objects.filter(url=website).count()
        size = get_closest_square(search_result_len)

        array = []

        counter = 0
        for pixel in search_result:
            col = ImageColor.getcolor(pixel.average_color, "RGB")
            array.append((col[0], col[1], col[2], 255))
            counter += 1

        if len(array) < size:
            for x in range(0, size - len(array)):
                array.append((0, 0, 0, 0))

        array2d = np.array(array, np.uint8)

        # https: // stackoverflow.com / questions / 72161115 / rgb - array - to - pil - image / 72161225  # 72161225
        im_pil = Image.fromarray(obj=array2d.reshape(int(math.sqrt(size)), int(math.sqrt(size)), 4), mode='RGBA')
        data = io.BytesIO()
        im_pil.save(data, "png")
        encoded_img = base64.b64encode(data.getvalue())
        decoded_img = encoded_img.decode('utf-8')
        img_data = f"data:image/png;base64,{decoded_img}"
        final_array.append(img_data)

    return final_array


def clusters_as_pixels(websites_to_show):
    # websites_to_show = Website.objects.distinct().filter(show=True)
    # print(len(websites_to_show))

    # https://stackoverflow.com/questions/687295/how-do-i-do-a-not-equal-in-django-queryset-filtering

    final_array = []
    for website in websites_to_show:
        search_result = SearchResult.objects.filter(url=website)
        array = []
        for result in search_result:

            search_result_clusters = Cluster.objects.filter(search_result_id=result)

            counter = 0
            for pixel in search_result_clusters:
                col = ImageColor.getcolor(pixel.color, "RGB")
                array.append((col[0], col[1], col[2], 255))
                counter += 1

        size = get_closest_square(len(array))
        if len(array) < size:
            for x in range(0, size - len(array)):
                array.append((0, 0, 0, 0))
        array2d = np.array(array, np.uint8)

        # https: // stackoverflow.com / questions / 72161115 / rgb - array - to - pil - image / 72161225  # 72161225
        im_pil = Image.fromarray(obj=array2d.reshape(int(math.sqrt(size)), int(math.sqrt(size)), 4), mode='RGBA')
        data = io.BytesIO()
        im_pil.save(data, "png")
        encoded_img = base64.b64encode(data.getvalue())
        decoded_img = encoded_img.decode('utf-8')
        img_data = f"data:image/png;base64,{decoded_img}"
        final_array.append(img_data)

    return final_array


def get_closest_square(number):
    return int(math.pow(math.ceil(math.sqrt(number)), 2))


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
