import asyncio

class ErrorState(Exception):
    pass

async def my_sleep(secs):
    print(f'task {secs}')
    await asyncio.sleep(secs)
    print(f'task {secs} finished sleeping')

    if secs == 5:
        raise ErrorState('5 is forbidden')
    print(f'Slept for {secs} secs')

async def main_cancel_future():
    tasks = [asyncio.create_task(my_sleep(secs)) for secs in [2,5,7]]
    sleepers = asyncio.gather(*tasks)

    #sleepers = asyncio.gather(*[my_sleep(secs) for secs in [2,5,7]])
    print('awaiting')
    try:
        await sleepers
    except ErrorState:
        print("Fatal error")
        for t in tasks:
            print(f'cancelling {t}')
            print(t.cancel())
        #sleepers.cancel()
    finally:
        await asyncio.sleep(5)

if __name__== '__main__':
    asyncio.run(main_cancel_future())
    #asyncio.run(main_cancel_future())
