# -*- coding: utf-8 -*-

from progressbar import ProgressBar
import aiohttp
import asyncio
import os
import requests
import urllib.parse

from aio_pool import AsyncIOPool


class Downloader:
    def __init__(self, url, path='downloads', name='', timeout=15, bytes_per_time=1024, max_connections=8):
        self.url = url

        self.path = path
        self.name = name or urllib.parse.urlparse(self.url).path.rpartition('/')[-1]
        self._full_path = ''

        self.timeout = timeout

        self.bytes_per_time = bytes_per_time
        self.max_connections = max_connections

        self.loop = asyncio.get_event_loop()

        self.session = aiohttp.ClientSession(loop=self.loop, connector=aiohttp.TCPConnector(verify_ssl=False))

    def get_content_length(self):
        try:
            response = requests.head(self.url, timeout=self.timeout)
            return int(response.headers.get('content-length', 0))
        except TimeoutError:
            return None

    async def get_content_range(self, content_range):
        async with self.session.get(url=self.url, headers=self.build_range_header(**content_range)) as response:
            if self.validate_content_range(
                status=response.status, content_range=response.headers['Content-Range'], **content_range
            ):
                return await response.read()
            else:
                return None

    @staticmethod
    def build_range_header(start, stop):
        return {'Range': f'bytes={start}-{stop}'}

    @staticmethod
    def validate_content_range(status, content_range, start, stop):
        _start, _, _stop = content_range.rpartition(' ')[-1].partition('/')[0].partition('-')
        return status == 206 and all([int(_start) == start, int(_stop) == stop])

    def build_path(self):
        if not os.path.exists(self.path) or not os.path.isdir(self.path):
            os.makedirs(self.path, exist_ok=True)

        self._full_path = os.path.join(self.path, self.name.replace('/', '-'))

        return self._full_path

    @property
    def full_path(self):
        return self._full_path or self.build_path()

    def _start(self, tasks, progress_bar, finished):
        failed = []

        fp = open(self.full_path, mode='wb')

        pool = AsyncIOPool(loop=self.loop, workers=min(self.max_connections, len(tasks)), timeout=self.timeout)

        for i, o in pool.map(self.get_content_range, tasks):
            if not o:
                failed.append(i)
            else:
                fp.seek(i['start'])
                fp.write(o)

                finished += 1
                progress_bar.update(finished)

        fp.close()

        return failed, finished

    def start(self):
        content_length = self.get_content_length()

        if content_length:
            tasks = [
                {'start': item + 1 if item else item, 'stop': min(item + self.bytes_per_time, content_length - 1)}
                for item in range(0, content_length, self.bytes_per_time)
            ]

            finished = 0
            progress_bar = ProgressBar(max_value=len(tasks))
            while True:
                tasks, finished = self._start(tasks=tasks, progress_bar=progress_bar, finished=finished)
                if not tasks:
                    break

        self.session.close()
        self.loop.close()


def main(url, path='downloads', name='', timeout=15, bytes_per_time=1024, max_connections=8):
    downloader = Downloader(
        url=url, path=path, name=name, timeout=timeout, bytes_per_time=bytes_per_time, max_connections=max_connections
    )
    downloader.start()


if __name__ == '__main__':
    # env/bin/python downloader.py --url http://mirrors.hust.edu.cn/apache/hadoop/common/hadoop-2.8.0/hadoop-2.8.0.tar.gz --bytes-per-time 1048576
    from fire import Fire
    Fire(main)
