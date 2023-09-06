@echo off
% 激活 Conda 环境, 使用的是: Python3.10.12 %
call conda activate py10

% 激活微信脚本环境 %
call .\venv\Scripts\activate
% 运行脚本--登录 %
python .\code\wechat_login.py

%登录需要一会儿, 等待10s%
timeout /t 10 /nobreak > NUL
% 运行脚本--发送并保存临时 ipv6 地址 %
python .\code\wechat.py

:end