# -*- coding: utf-8 -*-

import asyncio
import async_timeout


class AsyncIOPool:
    def __init__(self, loop, workers, timeout, default=None):
        self.loop = loop
        self.workers = workers
        self.timeout = timeout
        self.default = default

    async def _worker(self, queue, coroutine, sequence):
        while True:
            try:
                item = sequence.pop(0)
            except IndexError:
                return

            try:
                with async_timeout.timeout(self.timeout):
                    result = await coroutine(item)
                    queue.put_nowait((item, result))
            except asyncio.TimeoutError:
                queue.put_nowait((item, self.default))

    def map(self, coroutine, sequence):
        if not isinstance(sequence, (list, set)):
            sequence = list(sequence)

        queue = asyncio.Queue()

        workers = [
            asyncio.Task(self._worker(queue=queue, coroutine=coroutine, sequence=sequence))
            for _ in range(0, self.workers)
        ]
        while True:
            if queue.empty() and all(w.done() for w in workers):
                break

            while True:
                try:
                    yield self.loop.run_until_complete(asyncio.wait_for(queue.get(), timeout=0.001))
                except (asyncio.QueueEmpty, asyncio.TimeoutError):
                    break
