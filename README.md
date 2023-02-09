# Chat Service Client
A simple Python3 TCP client for the [erlang-chat-service](https://github.com/skaysrei/erlang-chat-service) project. 
The client runs two async tasks in the main event loop: one that listens, and one that waits for user inputs. 
By default at startup it it will attempt to connect on: 'localhost:1337'.

## Requirements
To run the client you will need to have Python3 installed on your machine.
You can get it [from here](https://www.python.org/downloads/).

## Running the client
In order to use the app simply clone the repository and from within the folder run the client:
```
python3 client.py
```
You can also pass the client some arguments to modify the behaviour at startup:
```
-ip [server_ip]
```
```
-port [server_port]
```

## Commands
All the business logic is implemented server-side, to have a look at the list of commands just 
visit the server project's [GitHub page](https://github.com/skaysrei/erlang-chat-service).

###### To quit the app
To quit the client simply type this command:
```
!quit
```

<br></br>

### References used during development: 

[asyncio — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)

[asyncio: TCP Echo Client](https://docs.python.org/3/library/asyncio-protocol.html#tcp-echo-client)

[asyncio: Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)

[asyncio: Streams](https://docs.python.org/3/library/asyncio-stream.html)

[asyncio: Queues](https://docs.python.org/3/library/asyncio-queue.html)

[aioconsole like, Non-blocking Console Input](https://stackoverflow.com/a/65326191)

[A simple asyncio chat server and client made in Python](https://github.com/henry232323/Simple-Asyncio-Chat-Client)
