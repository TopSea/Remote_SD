from uiautomation import WindowControl

class Settings():
    wechatWindow: WindowControl = None
    runing:int = 0
    ipv6:str = ''
    huishi_started:bool = False
    
settings: Settings = Settings() 