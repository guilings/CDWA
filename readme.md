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



simple_chinese
以下是简体中文的自述文件：
欢迎使用CDWA---可部署悄悄话
简介：什么是CDWA？

        什么是CDWA，按其全面顾名思义是一个由作者Coffee_dou所开发的一个可部署的悄悄话。我们日常需要与他人进行交流，但是有些话是属于我们的悄悄话，通常是一些不可告人的秘密。又想和别人分享，又不想留下痕迹？一个可以自己部署的悄悄话系统可以满足你的使用需求。而部署步骤非常简单，你只需要一个自己的服务器，当然也可以内网部署，还有双方的客户端就行。本方案采取websocket的传输方案，以提高在聊天中的传输效率。本程序是灵感来源：hMailServer。与hMailServer相同的是，都属于一个可以自己部署与他人建立联系的程序。接下来让我们看看应用介绍

服务端的部署：

       服务端分为服务端管理面板和服务主进程。管理面板还在开发中~~~~~

       因为我们采用了websocket的传输方案，所以在一般的服务器上面不能直接使用。我们需要给我们的服务器开启websocket的协议（不知道为什么现在的服务器都不原生支持）。我们需要通过Windows的IIS服务器管理系统来安装websocket（主进程是py程序，且linux原生支持websocket协议，故Linux端可以直接使用主进程）因为作者感觉安装websocket有点麻烦，故准备了一键配置脚本，用户可以通过管理面板。选择一键配置，等待脚本的执行完成，这边建议完成后可以重启一遍服务器后再运行主进程，同样，也可以点击安装包中的一键脚本以达到相同目的：

环境配置好后，我们就可以直接打开服务端主进程，因为服务端需监听55668端口以建立客户端与服务端之间的联系，故需要放行55668的端口，当然这操作在一键配置脚本中也包含在内，如果没有成功，可以试着手动开启防火墙的55668端口

就这样，服务端已经部署完成，接下来就是我们使用的客户端

客户端的使用：

在服务端部署完成后，我们便可以使用客户端进行悄悄话了。打开客户端的登录器，


由于早期开发的缘故，客户端UI较丑，当然我们在尽力美化和 优化当中，敬请期待后续的开发

在 客户端，2用户需要输入刚刚部署的服务端的ip并使用ws://+ip+:55668的链接形式，然后输入使用用户名和密码，用户名和密码可在服务端安装包中的csv文件中查看和修改

完成后点击登录，客户端会请求服务端来验证用户账号和密码，登录成功后就可以进入悄悄话的界面了


我们可以在文本框中输入悄悄话的内容，点击send后就可以了。


感谢您对coffeedou的关注，coffeedou将尽快将最好的体验给您体验


更快，效率更高一直是我们的追求，希望 CDWA----Coffee-Deployable whispers Application 能给您带来最完美的体验
