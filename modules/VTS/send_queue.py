import queue

send = queue.Queue()

async def sender(function, args):
    send.put_nowait( (function, args) )