import uiautomation as auto


def wechat_login():
    try:
        wechatWindow = auto.PaneControl(searchDepth=1, Name="微信", ClassName='WeChatLoginWndForPC')
        wechatWindow.SetFocus()
        login_btn = wechatWindow.ButtonControl(Name='进入微信')
        login_btn.Click()
    except LookupError:
        return False
    else:
        return True

if __name__ == '__main__':
    print('start')
    print(wechat_login())
