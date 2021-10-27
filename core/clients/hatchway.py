import requests
from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class HatchwayClient:
    def __init__(self):
        self.base_url = 'https://api.hatchways.io/assessment'
        self.blog_url = f'{self.base_url}/blog/posts'
        self.blogs_db = dict()

    def _fetch_blogs(self, tag):
        """
        Requests to Hatchway api to fetch blog posts for a specific tag

        Before calling the api, checks whether the data for the tag is
        already in the cache, If yes then fetches the data from cache

        Updates the blogs dictionary

        :param tag:
        :return: List[Blog]
        """

        cache_key = f'blogs_{tag}'

        # Checks data in cache
        if cache_key in cache:
            blogs = cache.get(cache_key)
        else:
            blogs = requests.get(
                url=self.blog_url,
                params={
                    'tag': tag
                }
            ).json()['posts']

            # Update cache
            cache.set(cache_key, blogs, CACHE_TTL)

        # Update blogs dictionary
        self.blogs_db.update({
            blog['id']: blog
            for blog in blogs
        })

    # noinspection PyMethodMayBeStatic
    def _sort_blogs(self, blogs, sort_by, direction):
        """
        Sorts Blogs depending on the provided key and direction

        :param blogs:
        :param sort_by:
        :param direction:
        :return: List[Blog]
        """
        blogs = sorted(blogs, key=lambda x: x[sort_by])
        return blogs if direction == 'asc' else blogs[::-1]

    def fetch_blogs(self, tags, sort_by, direction):
        """
        Fetches list of blogs for given tags by calling _fetch_blogs(tag)
        Returns the blogs in sorted order by calling _sort_blogs()

        :param tags:
        :param sort_by:
        :param direction:
        :return: List[Blog]
        """

        if isinstance(tags, str):
            tags = tags.split(',')

        with ThreadPoolExecutor() as executor:
            executor.map(self._fetch_blogs, tags)

        return self._sort_blogs(self.blogs_db.values(), sort_by, direction)
