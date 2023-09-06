#coding=utf-8
import os
import uiautomation as auto

from get_ipv6 import getIPv6Address

# 退出绘世
def quit_huishi_control():
    try:
        huishi_control = auto.WindowControl(searchDepth=1, Name="控制台", ClassName='Window')
        huishi_control.SetFocus()
        login_btn = huishi_control.ButtonControl(AutomationId='PART_CloseButton')
        login_btn.Click()
        confirm_btn = huishi_control.ButtonControl(Name='是(Y)')
        confirm_btn.Click()
    except LookupError:
        return False
    else:
        return True

def quit_huishi_window():
    try:
        huishi_window = auto.WindowControl(searchDepth=1, Name="绘世 2.2.19", ClassName='Window')
        huishi_window.SetFocus()
        exit_btn = huishi_window.ButtonControl(AutomationId='PART_CloseButton')
        exit_btn.Click()
    except LookupError:
        return False
    else:
        return True

def quit_huishi():
    quit_huishi_control()
    return quit_huishi_window()

# 启动绘世
def launch_huishi():
    start_webui('launch_huishi.bat')

def start_huishi_default():
    try:
        start_huishi_ipv6('127.0.0.1')
    except Exception:
        return False
    else:
        return True

def start_huishi_ipv6(adress:str):
    try:
        huishi_window = auto.WindowControl(searchDepth=1, Name='绘世 2.2.19', ClassName='Window')
        huishi_window.SetFocus()
        advanced_btn = huishi_window.TextControl(foundIndex = 4)
        advanced_btn.Click()
        advanced_config = huishi_window.PaneControl(foundIndex = 2)
        sub_config = advanced_config.PaneControl(foundIndex = 1)
        scroll_bar = sub_config.ScrollBarControl(foundIndex=1)
        scroll_bar.Click()
        listen_group = advanced_config.GroupControl(foundIndex=2)
        listen_group.Click()
        ip = listen_group.EditControl(foundIndex=1)
        # 全选替换ip
        ip.SendKeys('{Ctrl}a')
        ip.SendKeys(adress)

        start_btn = advanced_config.ButtonControl(foundIndex = 2)
        start_btn.Click()
    except Exception:
        return False
    else:
        return True


def start_webui(webui:str='webui.bat'):
    os.system(' start cmd.exe /K %s ' % webui)

def quit_webui(webui: str='SD'):
    cmdWindow = auto.WindowControl(searchDepth=1, Name=webui, ClassName='CASCADIA_HOSTING_WINDOW_CLASS')
    cmdWindow.SetFocus()
    title_bar = cmdWindow.TitleBarControl(foundIndex = 2)
    title_bar.ButtonControl(foundIndex = 3).Click()


if __name__ == '__main__':
    print('start')
    print(start_huishi_ipv6('weihr'))
