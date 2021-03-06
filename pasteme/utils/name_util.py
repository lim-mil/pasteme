import asyncio
import random

from pasteme.pkg.redis import GetRedis, RedisTBName

LETTERS = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
]


async def give_me_a_name():
    async with GetRedis() as redis:
        name = ''.join(random.choices(LETTERS, k=20))
    return name


if __name__ == '__main__':
    name = ''.join(random.choices(LETTERS, k=20))
    print(name)
