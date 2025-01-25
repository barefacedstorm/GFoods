from .provider_manager import DataProvider
import aiohttp
import logging
import os
from datetime import datetime


class BloombergAgProvider(DataProvider):
    def __init__(self):
        self.base_url = "https://bba.bloomberg.com/api/v1/agriculture"
        self.api_key = os.getenv('BLOOMBERG_API_KEY')
        self.logger = logging.getLogger(__name__)

    async def fetch_data(self):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }

        async with aiohttp.ClientSession() as session:
            commodity_data = await self.fetch_commodities(session, headers)
            return commodity_data

    async def fetch_commodities(self, session, headers):
        endpoint = f"{self.base_url}/commodities"
        params = {
            'symbols': 'C 1:COM,W 1:COM,S 1:COM,O 1:COM,RR1:COM,SM1:COM,BO1:COM,RS1:COM,CC1:COM,KC1:COM,SB1:COM,CT1:COM,OJ1:COM,LC1:COM,FC1:COM,LH1:COM',
            'fields': 'name,Price,Units,Change,%Change,Contract,Time (EDT)'
        }

        try:
            async with session.get(endpoint, headers=headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return self.get_default_commodity_data()
        except Exception as e:
            self.logger.error(f"Error fetching commodity data: {e}")
            return self.get_default_commodity_data()

    def get_default_commodity_data(self):
        return {
            "C 1:COM": {
                "name": "Corn (CBOT)",
                "Units": "USd/bu.",
                "Price": "485.00",
                "Change": "+1.00",
                "%Change": "+0.21%",
                "Contract": "Dec 2023",
                "Time (EDT)": "3:52 AM"
            },
            "W 1:COM": {
                "name": "Wheat (CBOT)",
                "Units": "USd/bu.",
                "Price": "583.25",
                "Change": "+2.75",
                "%Change": "+0.47%",
                "Contract": "Dec 2023",
                "Time (EDT)": "3:52 AM"
            },
            "S 1:COM": {
                "name": "Soybean (CBOT)",
                "Units": "USd/bu.",
                "Price": "1,316.25",
                "Change": "+1.75",
                "%Change": "+0.13%",
                "Contract": "Jan 2024",
                "Time (EDT)": "3:52 AM"
            },
            "O 1:COM": {
                "name": "Oats (CBOT)",
                "Units": "USd/bu.",
                "Price": "389.25",
                "Change": "-0.50",
                "%Change": "-0.13%",
                "Contract": "Dec 2023",
                "Time (EDT)": "3:50 AM"
            },
            "RR1:COM": {
                "name": "Rough Rice (CBOT)",
                "Units": "USD/cwt",
                "Price": "16.34",
                "Change": "-0.02",
                "%Change": "-0.15%",
                "Contract": "Jan 2024",
                "Time (EDT)": "10/24/2023"
            },
            "SM1:COM": {
                "name": "Soybean Meal (CBOT)",
                "Units": "USD/T.",
                "Price": "438.40",
                "Change": "+4.20",
                "%Change": "+0.97%",
                "Contract": "Dec 2023",
                "Time (EDT)": "3:52 AM"
            },
            "BO1:COM": {
                "name": "Soybean Oil (CBOT)",
                "Units": "USd/lb.",
                "Price": "51.35",
                "Change": "+0.03",
                "%Change": "+0.06%",
                "Contract": "Dec 2023",
                "Time (EDT)": "3:52 AM"
            },
            "RS1:COM": {
                "name": "Canola (ICE)",
                "Units": "CAD/MT",
                "Price": "695.70",
                "Change": "+5.90",
                "%Change": "+0.86%",
                "Contract": "Jan 2024",
                "Time (EDT)": "3:51 AM"
            },
            "CC1:COM": {
                "name": "Cocoa (ICE)",
                "Units": "USD/MT",
                "Price": "3,729.00",
                "Change": "-30.00",
                "%Change": "-0.80%",
                "Contract": "Dec 2023",
                "Time (EDT)": "10/24/2023"
            },
            "KC1:COM": {
                "name": "Coffee 'C' (ICE)",
                "Units": "USd/lb.",
                "Price": "168.15",
                "Change": "+2.30",
                "%Change": "+1.39%",
                "Contract": "Dec 2023",
                "Time (EDT)": "10/24/2023"
            },
            "SB1:COM": {
                "name": "Sugar #11 (ICE)",
                "Units": "USd/lb.",
                "Price": "27.62",
                "Change": "+0.09",
                "%Change": "+0.33%",
                "Contract": "Mar 2024",
                "Time (EDT)": "3:51 AM"
            },
            "CT1:COM": {
                "name": "Cotton #2 (ICE)",
                "Units": "USd/lb.",
                "Price": "82.93",
                "Change": "0.00",
                "%Change": "0.00%",
                "Contract": "Dec 2023",
                "Time (EDT)": "3:50 AM"
            },
            "OJ1:COM": {
                "name": "Orange Juice (ICE)",
                "Units": "USd/lb.",
                "Price": "384.60",
                "Change": "+1.15",
                "%Change": "+0.30%",
                "Contract": "Jan 2024",
                "Time (EDT)": "10/24/2023"
            },
            "LC1:COM": {
                "name": "Live Cattle (CME)",
                "Units": "USd/lb.",
                "Price": "178.63",
                "Change": "+0.28",
                "%Change": "+0.15%",
                "Contract": "Dec 2023",
                "Time (EDT)": "10/24/2023"
            },
            "FC1:COM": {
                "name": "Feeder Cattle (CME)",
                "Units": "USd/lb.",
                "Price": "234.85",
                "Change": "-0.85",
                "%Change": "-0.36%",
                "Contract": "Jan 2024",
                "Time (EDT)": "10/24/2023"
            },
            "LH1:COM": {
                "name": "Lean Hogs (CME)",
                "Units": "USd/lb.",
                "Price": "66.38",
                "Change": "+0.20",
                "%Change": "+0.30%",
                "Contract": "Dec 2023",
                "Time (EDT)": "10/24/2023"
            }
        }
