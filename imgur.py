import random
import imgurpython
from imgurpython import ImgurClient

IMGUR_CLIENT_ID = '2ad30c3920b3088'
IMGUR_CLIENT_SECRET = '39b39f2eb2ac4c168d0b45b291665f309cca20e6'

imgurClient = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET);

def get(query, gif=False) :
    found = ''
    if query is None:
        gallery = imgurClient.gallery_random()
        text = 'A random image'
    else:
        gallery = imgurClient.gallery_search(q=query, sort='top', window='all')
        #print(gallery)

    if gallery:
        finalGallery = []
        for image in gallery:
            if type(image) == imgurpython.imgur.models.gallery_album.GalleryAlbum:
                continue
            if (not gif) and (image.type == 'image/gif'):
                continue
            elif gif and (image.type != 'image/gif'):
                continue
            finalGallery.append(image)

        if(len(finalGallery) > 0):
            image = random.choice(finalGallery)
            found = image.link

    #print('image url: ' + found)

    return found