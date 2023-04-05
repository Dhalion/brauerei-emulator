#!/usr/bin/env python

import json
from aiohttp import web
import socketio
from rich.pretty import pprint
from rich import print
from dataclasses import dataclass
import random
import asyncio
import websockets

PORT = 420

@dataclass
class Brauerei:
    t1: float
    t2: float
    heizstab: bool
    motor: int



brauerei = Brauerei(0.0,0.0,False,0)



async def handle_message(message, websocket):
    # Convert to Dict first
    print("Raw Message: " + message)
    message = json.loads(message)

    pprint(message)
    if not isCommandValid(message):
        return False
    print("[bold green]Command Valid")
    
    if message.get("type") == "get":
        refreshTemps()  # Generate new Temps
        response = brauerei.__dict__
        response = json.dumps(response)
        # pprint(response)
        await websocket.send(str(response))
        print("Response {} sent to {}".format(response, id))


    elif message.get("type") == "set":
        keys = message["data"].keys()
        for key in keys:
            match key:
                case "motor":
                    val = message["data"].get(key)
                    if not isValueValid(key, val):
                        return False
                    brauerei.motor = val
                case "heizstab":
                    val = message["data"].get(key)
                    if not isValueValid(key, val):
                        return False
                    brauerei.heizstab = val
    else:
        raise ValueError("Invalid command type")
    
    pprint(brauerei)
    return


def isValueValid(key, value):
    match key:
        case "motor":
            if not isinstance(value, int):
                raise Exception("Invalid Value to set")
                return False
            if not 0 <= value <= 255:
                raise Exception("Invalid Value to set")
                return False
            return True

        case "heizstab":
            if not isinstance(value, bool):
                raise Exception("Invalid Value to set")
                return False
            return True
    return False

def isCommandValid(command):
    if not isinstance(command, dict):
        raise Exception("Invalid type for command")
        return False

    if not "type" in command:
        raise Exception("No type provided in Command")
        return False
    

    if command.get("type") == "set":   # Only check set Command for data
        if not "data" in command:
            raise Exception("No data provided in Command")
            return False

    # All checks succeeded
    return True

def refreshTemps():
    brauerei.t1 = random.random()*80
    brauerei.t2 = random.random()*80

async def callback(websocket):
    async for message in websocket:
        # print("Type: " + type(message))
        print(message)
        await handle_message(message, websocket)

async def periodic(websocket):
    while True:
        await asyncio.sleep(.5)
        refreshTemps()
        response = brauerei.__dict__
        # pprint(response)
        try:

            await websocket.send("message" + str(response))
            print("Response {} sent to {}".format(response, websocket.id))        
        except:
            pass


async def handler(websocket):
    asyncio.create_task(periodic(websocket))
    await callback(websocket)


async def main():
    async with websockets.serve(handler, "localhost", PORT):
        await asyncio.Future()




if __name__ == "__main__":
    try:  
        pprint("BrauereiEmulator started...")
        # web.run_app(app)
        asyncio.run(main())
        pass
    except KeyboardInterrupt:
        exit(1)
    except asyncio.CancelledError:
        pass