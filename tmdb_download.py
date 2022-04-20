import imdb
import os
import requests

CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key=495e2304d9d84754f516ad3e5f1e23c1'
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key=495e2304d9d84754f516ad3e5f1e23c1'
KEY = '495e2304d9d84754f516ad3e5f1e23c1'


def _get_json(url):
    r = requests.get(url)
    return r.json()


def _download_images(urls, path='.'):
    """download all images in list 'urls' to 'path' """

    for nr, url in enumerate(urls):
        if nr==0:
            r = requests.get(url)
            filetype = r.headers['content-type'].split('/')[-1]
            filename = 'poster_{0}.{1}'.format(nr, filetype)
            filepath = os.path.join(path, filename)
            with open(filepath, 'wb') as w:
             w.write(r.content)
        else :
            continue

def get_poster_urls(imdbid):
    """ return image urls of posters for IMDB id

        returns all poster images from 'themoviedb.org'. Uses the
        maximum available size.

        Args:
            imdbid (str): IMDB id of the movie

        Returns:
            list: list of urls to the images
    """
    config = _get_json(CONFIG_PATTERN.format(key=KEY))
    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']

    """
        'sizes' should be sorted in ascending order, so
            max_size = sizes[-1]
        should get the largest size as well.        
    """

    def size_str_to_int(x):
        return float("inf") if x == 'original' else int(x[1:])

    max_size = max(sizes, key=size_str_to_int)

    posters = _get_json(IMG_PATTERN.format(key=KEY, imdbid=imdbid))['posters']
    poster_urls = []
    for poster in posters:
        rel_path = poster['file_path']
        url = "{0}{1}{2}".format(base_url, max_size, rel_path)
        poster_urls.append(url)

    return poster_urls


def tmdb_posters(imdbid, count=None, outpath='.'):
    urls = get_poster_urls(imdbid)
    if count is not None:
        urls = urls[:count]
    _download_images(urls, outpath)


################################################# search movie id

#if __name__ == "__main1__":

tmdb_posters('tt0095016')
#print(path)
print(get_poster_urls("tt0095016"))

########################
import imdb

moviesDB = imdb.IMDb()

# # Help?
#print(dir(moviesDB))
# ----------------------------------------
# 1) Search for a title
movie_name=input("please enter movie name to look for : ")
movies = moviesDB.search_movie(movie_name)

print('Searching for:',movie_name)
id = movies[0].getID()
movie = moviesDB.get_movie(id)
print("tt",id,sep="")
tmdb_posters("tt"+id)