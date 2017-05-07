# -*- coding: utf-8 -*-


from downloader import Downloader


class ReadTheDocsDownloader(Downloader):
    def __init__(self, project, version='latest', path='downloads', timeout=15, bytes_per_time=1024, max_connections=8):
        ext = 'zip'
        name = f'{project}.{version}.{ext}'
        url = f'https://media.readthedocs.org/htmlzip/{project}/{version}/{project}.{ext}'

        super(ReadTheDocsDownloader, self).__init__(
            url=url, path=path, name=name, timeout=timeout,
            bytes_per_time=bytes_per_time, max_connections=max_connections
        )


def main(project, version='latest', path='downloads', timeout=15, bytes_per_time=1024, max_connections=8):
    read_the_docs = ReadTheDocsDownloader(
        project=project, version=version, path=path, timeout=timeout,
        bytes_per_time=bytes_per_time, max_connections=max_connections
    )
    read_the_docs.start()

if __name__ == '__main__':
    # env/bin/python read_the_docs.py --project aiohttp --bytes-per-time 102400
    from fire import Fire
    Fire(main)
