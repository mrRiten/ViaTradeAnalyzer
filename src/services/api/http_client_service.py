import aiohttp

class HttpClientService:
    def __init__(self, timeout: int = 60):
        self.timeout = timeout

    def create(self):
        return aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
