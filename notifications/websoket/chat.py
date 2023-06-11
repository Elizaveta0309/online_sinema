import asyncio

import websockets
from websockets.exceptions import ConnectionClosedError

peoples = {}


async def welcome(websocket: websockets.WebSocketServerProtocol) -> str:
    await websocket.send('Представьтесь!')
    name = await websocket.recv()
    await websocket.send(
        'Чтобы поговорить, напишите "<имя>: <сообщение>". Например: Ира: купи хлеб.'
    )
    await websocket.send('Посмотреть список участников можно командой "?"')
    peoples[name.strip()] = websocket
    return name


async def receiver(
    websocket: websockets.WebSocketServerProtocol,
    path: str)-> None:
    name = await welcome(websocket)
    try:
        while True:
            message = (await websocket.recv()).strip()
            if message == '?':
                await websocket.send(', '.join(peoples.keys()))
                continue
            else:
                try:
                    to, text = message.split(': ', 1)
                    if to in peoples:
                        await peoples[to].send(f'Сообщение от {name}: {text}')
                    else:
                        await websocket.send(f'Пользователь {to} не найден')
                except ValueError:
                    await websocket.send(
                        'Неправильный формат сообщения! Попробуйте "<имя>: <сообщение>"'
                    )
    except ConnectionClosedError:
        del peoples[name.strip()]


ws_server = websockets.serve(receiver, "localhost", 8765)

loop = asyncio.get_event_loop()
loop.run_until_complete(ws_server)
loop.run_forever()
