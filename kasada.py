from playwright.sync_api import sync_playwright
from colorama import Fore, Style
from raducord import BannerUtils
import time

gray = Fore.LIGHTBLACK_EX
orange = Fore.LIGHTYELLOW_EX
lightblue = Fore.LIGHTBLUE_EX

class log:
    @staticmethod
    def slog(type, color, message, time):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ] [ {Fore.CYAN}{time:.2f}s{gray} ]"
        print(log.center(msg))
        
    @staticmethod
    def ilog(type, color, message):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ]"
        inputmsg = input(log.center(msg) + " ")
        return inputmsg

    @staticmethod
    def log(type, color, message):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ]{Style.RESET_ALL}"
        print(log.center(msg))

    @staticmethod
    def success(message, time):
        log.slog('+', Fore.GREEN, message, time)

    @staticmethod
    def fail(message):
        log.log('X', Fore.RED, message)

    @staticmethod
    def warn(message):
        log.log('!', Fore.YELLOW, message)

    @staticmethod
    def info(message):
        log.log('i', lightblue, message)
        
    @staticmethod
    def input(message):
        return log.ilog('i', lightblue, message)

    @staticmethod
    def working(message):
        log.log('-', orange, message)

    @staticmethod
    def center(txt):
        return BannerUtils.center_text(txt)
        
class X_KSPDK_CT:
    def __init__(self) -> None:
        pass
    
    def __getCT__(self) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            isCT = False 
            ctVal = None
            isST = False 
            stVal = None

            def solve(resp):
                nonlocal isCT, ctVal, isST, stVal
                if not isCT and not isST and '/tl' in resp.url:
                    headers = resp.headers
                    ST = headers.get("x-kpsdk-st")
                    CT = headers.get('x-kpsdk-ct')
                    isCT = True
                    ctVal = CT
                    isST = True
                    stVal = ST

            page.on("response", solve)
            page.goto("https://twitch.tv") # replace with the site you need 
            browser.close()
            
            return ctVal, stVal

while True:
    KSPDK = X_KSPDK_CT()
    s = time.time()
    ct, st = KSPDK.__getCT__()
    if ct:
        log.success(f"CT --> {ct[:25]}***", round(time.time()-s, 2))
    else:
        log.fail("CT not retrieved")
    if st:
        log.success(f"ST --> {st}", round(time.time()-s, 2))
    else:
        log.fail("ST not retrieved")
