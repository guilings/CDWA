@echo off
:: 需要管理员权限才能执行的命令
setlocal

:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% == 0 (
    echo 已经拥有管理员权限
) else (
    echo 请求管理员权限
    powershell -Command "Start-Process cmd -ArgumentList '/c %~dp0%~nx0' -Verb RunAs"
    exit /b
)
:: 安装 IIS 和 WebSocket 功能
echo Installing IIS and WebSocket Protocol...
dism /online /enable-feature /featurename:IIS-WebServerRole /all
dism /online /enable-feature /featurename:IIS-WebSockets /all

:: 启用 WebSocket 协议
echo Enabling WebSocket Protocol in IIS...
%windir%\System32\inetsrv\appcmd set config /section:webSocket /enabled:true

:: 添加防火墙规则
set PORT=55668
echo Configuring firewall rules for WebSocket...
netsh advfirewall firewall add rule name="WebSocket Server" protocol=TCP dir=in localport=%PORT% action=allow

echo.
echo WebSocket server setup is complete.
echo Please ensure your WebSocket server is running on port %PORT%.
echo.

pause
endlocal
