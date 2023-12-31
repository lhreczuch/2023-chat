# sockets chat
Chat (client-server-client)

Application works on local connection by default, but it could work on public by editing 

-IP in server.bind() function in server.py file,
-IP in server_ip variable in clientUI.py file.

Server file uses local IP of device that file is placed in by default, as mentioned above. According to this you don't have to edit server file, if you use app in local web.

Although you should always set server IP on server_ip variable in clientUI.py file

Many users can join chat.

There is also a SQLite database that its'been used to search messages
