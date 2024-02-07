#!/bin/env python3
"""
import asyncio
import sys

# stop=False

async def compute(n, p, event):
    # global stop
    async def C(n, p):
        await asyncio.sleep(0)
        if p == 0 or n == p:
            return 1
        else:
            return await C(n - 1, p) + await C(n - 1, p - 1)

    res = await C(n, p)
    event.set()
    # stop = True
    return res


async def g(event):
    # while not stop
    while not event.is_set():
        for i in range(20):
            print("* ", end="", flush=True)
        for i in range(20):
            print("\b\b  \b\b", end="", flush=True)
        await asyncio.sleep(0)


async def main(n, p):
    event = asyncio.Event()
    res = await asyncio.gather(g(event), compute(n, p, event))

    return res[1]


args = sys.argv
n, p = int(args[1]), int(args[2])
print(asyncio.run(main(n, p)))

"""

"""
import asyncio
import sys


async def ping(host="example.com", count=1, wait_sec=1):
    try:
        p = await asyncio.create_subprocess_exec(
            "ping",
            "-c",
            str(count),
            "-W",
            str(wait_sec),
            host,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout_data, _ = await p.communicate()

        output = stdout_data.decode()
        lines = output.split("\n")
        lines = list(filter(lambda x: x != "", lines))
        total = lines[-2].split(",")[3].split()[1]
        loss = lines[-2].split(",")[2].split()[0]
        timing = lines[-1].split()[3].split("/")
        return {
            "type": "rtt",
            "min": timing[0],
            "avg": timing[1],
            "max": timing[2],
            "mdev": timing[3],
            "total": total,
            "loss": loss,
        }
    except Exception:
        return None


async def test_all_addresses(host):
    async def test_address(h):
        res = await ping(h)
        if res:
            return h

    res = await asyncio.gather(
        *[test_address(f"{host}.{i}") for i in range(256)]
    )

    return list(filter(lambda x: x is not None, res))


async def main():
    args = sys.argv
    hosts = args[1:]

    res = await asyncio.gather(*[test_all_addresses(h) for h in hosts])
    return [item for row in res for item in row]

if __name__ == "__main__":
    print(asyncio.run(main()))

"""
