from time import sleep

import uiautomation as auto
from wechat_login import wechat_login

from get_ipv6 import getIPv6Address, httpIPv6Address
from webui_control import *


auto.uiautomation.SetGlobalSearchTimeout(5)
wechatWindow = None
runing = 0
ipv6 = ''
huishi_started = False


def gain_focus():
    global wechatWindow
    try:
        wechatWindow = auto.WindowControl(searchDepth=1, Name="微信", ClassName='WeChatMainWndForPC')
        wechatWindow.SetFocus()
    except LookupError:
        return False
    else:
        return True

def send_ipv6():
    global ipv6
    ipv6 = getIPv6Address(2)
    chat_btn = wechatWindow.ButtonControl(Name='聊天')
    chat_btn.Click()

    chats = wechatWindow.ListControl(Name="会话")
    for chat in chats.GetChildren():
        if chat.Name == "文件传输助手":
            chat.Click()
            edit = wechatWindow.EditControl(Name=chat.Name)
            edit.SendKeys(httpIPv6Address(ipv6, "7860"))
            sendButton = wechatWindow.ButtonControl(Name='发送(S)')
            sendButton.Click()
            break
        print(chat.Name)

def get_latest_msg():
    messages = wechatWindow.ListControl(Name="消息")
    msg = messages.GetLastChildControl()
    return msg.Name

def deal_msg(msg: str):
    global runing
    global huishi_started
    if msg.startswith('@'):
        print("收到指令：%s" % msg)
        if msg == '@启动6':
            gain_focus()
            send_feedback(info="将以 IPv6 模式启动 Stable Diffusion ......")
            if runing == 0:
                start_webui('webui_ipv6.bat')
            elif runing == 4:
                quit_webui('SD_IPv4')
                start_webui('webui_ipv6.bat')
            elif runing == 14:
                quit_huishi_control()
                start_webui('webui_ipv4.bat')
            elif runing == 16:
                quit_huishi_control()
                start_webui('webui_ipv4.bat')
            else:
                pass
            runing = 6
            gain_focus()

        elif msg == '@启动':
            gain_focus()
            send_feedback(info="将以普通模式启动 Stable Diffusion ......")
            if runing == 0:
                start_webui('webui_ipv4.bat')
            elif runing == 6:
                quit_webui('SD_IPv6')
                start_webui('webui_ipv4.bat')
            elif runing == 14:
                quit_huishi_control()
                start_webui('webui_ipv4.bat')
            elif runing == 16:
                quit_huishi_control()
                start_webui('webui_ipv4.bat')
            else:
                pass
            runing = 4
            gain_focus()

        if msg == '@启动绘世6':
            gain_focus()
            send_feedback(info="将以 IPv6 模式启动 绘世 ......")
            if not huishi_started:
                launch_huishi()
                huishi_started = True
            if runing == 0:
                start_huishi_ipv6("[%s]"%ipv6)
            elif runing == 4:
                quit_webui('SD_IPv4')
                start_huishi_ipv6("[%s]"%ipv6)
            elif runing == 6:
                quit_webui('SD_IPv6')
                start_huishi_ipv6("[%s]"%ipv6)
            elif runing == 14:
                quit_huishi_control()
                start_huishi_ipv6("[%s]"%ipv6)
            else:
                pass
            runing = 16
            gain_focus()

        elif msg == '@启动绘世':
            gain_focus()
            send_feedback(info="将以普通模式启动 绘世 ......")
            if not huishi_started:
                launch_huishi()
                huishi_started = True
            if runing == 0:
                start_huishi_default()
            elif runing == 4:
                quit_webui('SD_IPv4')
                start_huishi_default()
            elif runing == 6:
                quit_webui('SD_IPv6')
                start_huishi_default()
            elif runing == 16:
                quit_huishi_control()
                start_huishi_default()
            else:
                pass
            runing = 14
            # gain_focus()

        elif msg == '@关闭':
            gain_focus()
            send_feedback(info="已停止 Stable Diffusion ......")
            print(runing)
            if runing == 4:
                quit_webui('SD_IPv4')
            elif runing == 6:
                quit_webui('SD_IPv6')
            else:
                pass
            runing = 0
            gain_focus()

        elif msg == '@关闭绘世':
            gain_focus()
            if runing == 14 or runing == 16:
                send_feedback(info="已停止 绘世 ......")
                quit_huishi()
                huishi_started = False
            sleep(2)
            gain_focus()
    else:
        # print(msg)
        pass

def send_feedback( info: str, compName: str='文件传输助手'):
    edit = wechatWindow.EditControl(Name=compName)
    edit.SendKeys(info)
    sendButton = wechatWindow.ButtonControl(Name='发送(S)')
    sendButton.Click()


if __name__ == '__main__' :
    # 登录微信
    # if(wechat_login()):
    #     print('成功登录微信。')
    # else :
    #     print('未执行微信登录，尝试让微信获取焦点。')

    # 微信获取焦点
    if(gain_focus()):
        # 发送 ipv6 地址
        # send_ipv6()
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
