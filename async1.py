import aiohttp
import async_timeout

# async def fetch(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.text()
#
async def fetch(url):
    """Fetch the specified URL using the aiohttp session specified."""
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)

        return response
