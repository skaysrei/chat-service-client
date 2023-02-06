import socket
import sys
import asyncio


params = {
    'server_ip': socket.gethostname(),
    'server_port': 1337,
}

display_buffer = []

def main(**kwargs):
    # updates the app params from user input
    params.update(kwargs)

    # try:
    #     # initializes the socket and starts the connection
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     s.connect((params["server_ip"], params["server_port"]))
    #     s.setblocking(False)
    # except socket.error as e:
    #     print("""
    #         Couldn't connect to the socket-server OwO: %s
    #     """ % e)
    #     sys.exit(1)

    # execution_loop(s)

    in_queue = asyncio.Queue()
    out_queue = asyncio.Queue()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(client_engine(in_queue, out_queue))
    
    while True:
        print(asyncio.create_task(out_queue.get()).decode())
        data = input("Say something: ")
        asyncio.create_task(out_queue.put(data.encode()))

# helper functions----------------------------------------------------------------

def execution_loop(s):
    while(True):
        msg_in = ''
        try:
            while True:
                buffer = s.recv(1024)
                if(len(buffer) <= 0):
                    break
                msg_in += buffer.decode("utf-8")
        except socket.error as e:
            print("Exception: ", e)
        print(msg_in)

        usr_in = ''
        while(len(usr_in) <= 0):
            usr_in = input("Say something: ")
        if(usr_in == '--quit'):
            s.close()
            break

        msg_out = usr_in.encode()
        s.send(msg_out)

async def client_engine(in_queue, out_queue) -> str:
    reader, writer = await asyncio.open_connection(
        params["server_ip"], 
        params["server_port"])

    # TODO: create two separate tasks for better efficency
    out = ''
    while True:
        # awaits for incoming data
        data = await reader.read(1024)
        if not data:
            raise Exception("socket closed UwU")
        # stores data received in queue
        await in_queue.put(data)
        
        # awaits to send queued data
        task = asyncio.create_task(out_queue.get())
        out = task.result()
        if(len(out) > 0):
            writer.write(out.encode())
            # awaits until writer buffer is empty
            await writer.drain()

def display_engine():
    pass


if __name__ == "__main__":
    main()