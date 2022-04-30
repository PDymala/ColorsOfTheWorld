from urllib.request import urlopen

import numpy as np
import requests
from PIL import Image
from bs4 import BeautifulSoup
from sklearn.cluster import MiniBatchKMeans


def fetchColor(url):
    limit = 10
    clusters = 9

    try:
        html_page = urlopen(url)
        soup = BeautifulSoup(html_page, "html.parser")
        images = []
        for img in soup.findAll('img'):
            images.append(img.get('src'))

        # array for all the image urls found on page
        megaArray = []
        counter = 0;

        # checking all the urls
        for image in images:
            # only those 'real links i.e. having http' will be parsed. Also only jpg
            if 'http' in image and ('jpg' in image or 'png' in image or 'bmp' in image):
                response = requests.get(image, stream=True)
                img = Image.open(response.raw).convert('RGB')
                if img.width > 10 and img.height > 10:
                    # print(image)
                    counter += 1
                    img.resize(size=(50, 50))
                    megaArray.extend(img.getdata())
                    if counter == limit:
                        avg_color_per_row = np.average(img, axis=0)
                        avg_color = np.average(avg_color_per_row, axis=0)
                        std_color = np.std(avg_color_per_row, axis=0)
                        break

        # straasznie dlugie
        # km = KMeans(
        #     n_clusters=10, init='random',
        #     n_init=10, max_iter=300,
        #     tol=1e-04, random_state=0
        # )

        km = MiniBatchKMeans(
            n_clusters=clusters, init='random',
            n_init=10, max_iter=300,
            tol=1e-04, random_state=0
        )

        y_km = km.fit_predict(megaArray)
        result = dir().count('avg_color')
        if len(images) == 0 or result == 0:
            avg_color = (0, 0, 0)
            std_color = (0, 0, 0)
            km.cluster_centers_ = []
            for a in range(clusters):
                km.cluster_centers_.append((0, 0, 0))

            return km.cluster_centers_, avg_color, std_color
        else:
            return km.cluster_centers_, avg_color, std_color

    except Exception:
        avg_color = (0, 0, 0)
        std_color = (0, 0, 0)
        cluster_centers_ = []
        for a in range(clusters):
            cluster_centers_.append((0, 0, 0))

        return cluster_centers_, avg_color, std_color