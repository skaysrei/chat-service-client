import asyncio
from sys import stdout


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
        print('Data received: {}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)

    # middleware yet to be implemented
    def process_msg(self, data):
        pass

    def send(self, msg):
        #if msg and self.user:
        self.last_message = "{author}: {content}".format(author=self.user, content=msg)
        self.transport.write(msg.encode())

    async def getmsgs(self, loop):
        self.output = self.stdoutput
        self.output("Connected to {0}:{1}\n".format(*self.sockname))
        while True:
            msg = await loop.run_in_executor(None, input, "{}: ".format(self.user)) #Get stdout input forever
            self.send(msg)
            if msg == 'quit':
                break

    def stdoutput(self, data):
        stdout.write(data.strip() + '\n')


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
        await on_con_lost
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())