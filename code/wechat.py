from time import sleep

import uiautomation as auto
from wechat_login import wechat_login

from get_ipv6 import getIPv6Address, httpIPv6Address
from webui_control import *
from config import settings

auto.uiautomation.SetGlobalSearchTimeout(5)


def gain_focus():
    try:
        settings.wechatWindow = auto.WindowControl(searchDepth=1, Name="微信", ClassName='WeChatMainWndForPC')
        settings.wechatWindow.SetFocus()
    except LookupError:
        return False
    else:
        return True

def send_ipv6():
    settings.ipv6 = getIPv6Address(2)
    chat_btn = settings.wechatWindow.ButtonControl(Name='聊天')
    chat_btn.Click()

    chats = settings.wechatWindow.ListControl(Name="会话")
    for chat in chats.GetChildren():
        if chat.Name == "文件传输助手":
            chat.Click()
            edit = settings.wechatWindow.EditControl(Name=chat.Name)
            edit.SendKeys(httpIPv6Address(settings.ipv6, "7860"))
            sendButton = settings.wechatWindow.ButtonControl(Name='发送(S)')
            sendButton.Click()
            break
        print(chat.Name)

def get_latest_msg():
    messages = settings.wechatWindow.ListControl(Name="消息")
    msg = messages.GetLastChildControl()
    return msg.Name

def deal_msg(msg: str):
    if msg.startswith('@'):
        print("收到指令：%s" % msg)
        if msg == '@启动6':
            gain_focus()
            send_feedback(info="将以 IPv6 模式启动 Stable Diffusion ......")
            if settings.runing == 0:
                start_webui('webui_ipv6.bat')
            elif settings.runing == 4:
                quit_webui('SD_IPv4')
                start_webui('webui_ipv6.bat')
            elif settings.runing == 14:
                quit_huishi_control()
                start_webui('webui_ipv4.bat')
            elif settings.runing == 16:
                quit_huishi_control()
                start_webui('webui_ipv4.bat')
            else:
                pass
            settings.runing = 6
            gain_focus()

        elif msg == '@启动':
            gain_focus()
            send_feedback(info="将以普通模式启动 Stable Diffusion ......")
            if settings.runing == 0:
                start_webui('webui_ipv4.bat')
            elif settings.runing == 6:
                quit_webui('SD_IPv6')
                start_webui('webui_ipv4.bat')
            elif settings.runing == 14:
                quit_huishi_control()
                start_webui('webui_ipv4.bat')
            elif settings.runing == 16:
                quit_huishi_control()
                start_webui('webui_ipv4.bat')
            else:
                pass
            settings.runing = 4
            gain_focus()

        if msg == '@启动绘世6':
            gain_focus()
            send_feedback(info="将以 IPv6 模式启动 绘世 ......")
            if not settings.huishi_started:
                launch_huishi()
                settings.huishi_started = True
            if settings.runing == 0:
                start_huishi_ipv6()
            elif settings.runing == 4:
                quit_webui('SD_IPv4')
                start_huishi_ipv6()
            elif settings.runing == 6:
                quit_webui('SD_IPv6')
                start_huishi_ipv6()
            elif settings.runing == 14:
                quit_huishi_control()
                start_huishi_ipv6()
            else:
                pass
            settings.runing = 16
            gain_focus()

        elif msg == '@启动绘世':
            gain_focus()
            send_feedback(info="将以普通模式启动 绘世 ......")
            if not settings.huishi_started:
                launch_huishi()
                settings.huishi_started = True
            if settings.runing == 0:
                start_huishi_default()
            elif settings.runing == 4:
                quit_webui('SD_IPv4')
                start_huishi_default()
            elif settings.runing == 6:
                quit_webui('SD_IPv6')
                start_huishi_default()
            elif settings.runing == 16:
                quit_huishi_control()
                start_huishi_default()
            else:
                pass
            settings.runing = 14
            # gain_focus()

        elif msg == '@关闭':
            gain_focus()
            send_feedback(info="已停止 Stable Diffusion ......")
            print(settings.runing)
            if settings.runing == 4:
                quit_webui('SD_IPv4')
            elif settings.runing == 6:
                quit_webui('SD_IPv6')
            else:
                pass
            settings.runing = 0
            gain_focus()

        elif msg == '@关闭绘世':
            gain_focus()
            if settings.runing == 14 or settings.runing == 16:
                send_feedback(info="已停止 绘世 ......")
                quit_huishi()
                settings.huishi_started = False
            sleep(2)
            gain_focus()
    else:
        # print(msg)
        pass

def send_feedback( info: str, compName: str='文件传输助手'):
    edit = settings.wechatWindow.EditControl(Name=compName)
    edit.SendKeys(info)
    sendButton = settings.wechatWindow.ButtonControl(Name='发送(S)')
    sendButton.Click()


if __name__ == '__main__' :
    # 登录微信
    if(wechat_login()):
        print('成功登录微信。')
    else :
        print('未执行微信登录，尝试让微信获取焦点。')

    # 微信获取焦点
    if(gain_focus()):
        # 发送 ipv6 地址
        send_ipv6()
        # 循环处理信息
        while True:
            # 获取最后一条信息
            msg = get_latest_msg()
            # 处理信息
            deal_msg(msg=msg)
            # 休息3秒
            sleep(3)
    else :
        print('微信获取焦点失败，将退出程序。')
