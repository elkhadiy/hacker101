import asyncio
from aiohttp_client_cache import CachedSession, SQLiteBackend


class Worker:
    def __init__(self, url, session):
        self.session = session
        self.url = url
    
    async def fetch(self, data):
        async with self.session.get(self.url, params={'post': data}) as response:
            content = await response.text(encoding='utf-8')
            return 'Something' not in content
    
    async def work(self):
        futures = {self.fetch(str(i)): i for i in range(256)}
        for f in asyncio.as_completed(futures):
            result = await asyncio.shield(f)
            if result:
                for other_future in futures:
                    other_future.close()
                return futures[f]


async def main(url):
    cache = SQLiteBackend(f'cache.db')
    async with CachedSession(cache=cache) as session:
        d = Worker(url, session)
        print(await d.work())
    await cache.close()


if __name__ == '__main__':
    url = 'https://example.com'
    asyncio.run(main(url))