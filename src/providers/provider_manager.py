import asyncio
import logging
from abc import ABC, abstractmethod
import aiohttp

class DataProvider(ABC):
    @abstractmethod
    async def fetch_data(self):
        pass

class ProviderManager:
    def __init__(self):
        self.providers = []
        self.logger = logging.getLogger(__name__)

    def add_provider(self, provider):
        self.providers.append(provider)
        self.logger.info(f"Added provider: {provider.__class__.__name__}")

    async def fetch_all_data(self):
        tasks = [provider.fetch_data() for provider in self.providers]
        return await asyncio.gather(*tasks, return_exceptions=True)
