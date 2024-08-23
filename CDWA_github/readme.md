Welcome to CDWA--- Deployable Whispers


Introduction: What is CDWA?

        What is CDWA, as the name suggests, is a deployable whisper developed by the author's Coffee_dou. We need to communicate with others on a daily basis, but some words are whispers that belong to us, and are usually some secret that cannot be heard. Want to share it with others but don't want to leave a trace? A self-deployable whispering system can meet your needs. The deployment steps are very simple, you only need a server of your own, of course, you can also deploy it over the intranet, and there are clients on both sides. This solution uses the WebSocket transmission scheme to improve the transmission efficiency in chats. This program was the inspiration: hMailServer. Like hMailServer, they are all part of a program that can be deployed by themselves to connect with others. Let's take a look at the application introduction

Server-side deployment:

       The server is divided into the server-side management panel and the main process of the service. The admin panel is still ~~~~~ in development

       Because we use the websocket transmission scheme, it cannot be used directly on general servers. We need to enable the websocket protocol for our server (I don't know why the current server doesn't natively support it). We need to install websocket through the IIS server management system of Windows (the main process is a py program, and Linux natively supports the websocket protocol, so the Linux side can directly use the main process) because the author feels that it is a bit troublesome to install websocket, so a one-click configuration script is prepared, and users can use the management panel. Select one-click configuration, wait for the execution of the script to complete, here it is recommended that you can restart the server once and then run the main process, and you can also click the one-click script in the installation package to achieve the same purpose:

After the environment is configured, we can directly open the main process of the server, because the server needs to listen to port 55668 to establish the connection between the client and the server, so we need to allow the port of 55668, of course, this operation is also included in the one-click configuration script, if it is not successful, you can try to manually open the 55668 port of the firewall

In this way, the server has been deployed, and the next step is the client we use

Use of the client:

After the server-side deployment is complete, we can use the client to whisper. Open the client's login,


Due to the early development, the client UI is ugly, of course, we are trying our best to beautify and optimize, so stay tuned for subsequent development

On the client, 2 users need to enter the IP of the server just deployed and use the link form of ws://+ip+:55668, and then enter the username and password, which can be viewed and modified in the csv file in the server installation package

After completing the login, the client will request the server to verify the user account and password, and after the login is successful, you can enter the interface of the whisper


We can enter the content of the whisper in the text box, and click send to do so.


Thank you for your interest in coffeedou, coffeedou will give you the best experience as soon as possible


Faster and more efficient has always been our pursuit, and we hope that CDWA----Coffee-Deployable whispers Application can bring you the best experience