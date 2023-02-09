import asyncio
import sys


params = {
    'server_ip': 'localhost',
    'server_port': 1337,
}

class ChatClient(asyncio.Protocol):
    def __init__(self, on_con_lost, loop, user):
        self.on_con_lost = on_con_lost
        self.user =  user
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport
        self.sockname = transport.get_extra_info("sockname")

    def data_received(self, data):
        parsed = data.decode()
        temp = parsed.removeprefix('<h>') # workaround for random double header bug
        if parsed.startswith('<h>'):
            message = temp.removeprefix('<h>')
            if len(message) > 0:
                print(f'\n{message}\n')

    def connection_lost(self, exc):
        print('\n\nConnection terminated')
        self.on_con_lost.set_result(True)

    # middleware yet to be implemented
    def process_msg(self, data):
        pass

    def send(self, msg):
        self.transport.write(msg.encode())

    async def getmsgs(self, loop):
        self.output = self.stdoutput
        self.output("Connected to {0}:{1}\n".format(*self.sockname))
        while True:
            msg = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline)
            cleanedUp = msg[:-1]
            if cleanedUp == 'quit':
                break
            self.send(cleanedUp)

    def stdoutput(self, data):
        sys.stdout.write(data.strip() + '\n')


async def main():
    # using event_loop and low level APIs.
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()

    userClient = ChatClient(on_con_lost, loop, "TESTUSER")
    transport, protocol = await loop.create_connection(
        lambda: userClient,
        params['server_ip'], params['server_port'])

    # runs input terminal as a concurrent task
    task = asyncio.create_task(userClient.getmsgs(loop))

    # loop.create_task(userClient.getmsgs(loop))

    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    try:
        await task
        # await on_con_lost
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())
