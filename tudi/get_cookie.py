# coding=utf-8
from browser import HtmlWindow
import time

class Get_Cookie(object):

    def cookie(self,url):
        v8_browser = HtmlWindow(url)
        script = v8_browser.doc.getElementsByTagName('script')[0].text.strip()
        # print script
        v8_browser.evalScript(script)
        v8_browser.evalScript("YunSuoAutoJump()")
        # cookie1 = v8_browser.context.locals.document.cookie
        # print cookie1
        href = v8_browser.window.location
        time.sleep(0.5)
        v8_browser2 = HtmlWindow('http://www.landchina.com/' + href)
        script2 = v8_browser.doc.getElementsByTagName('script')[0].text.strip()
        # print script2
        try:
            v8_browser2.evalScript(script2)
        except:
            pass
        cookie = v8_browser2.context.locals.document.cookie
        # print cookie
        return cookie

if __name__ == '__main__':
    pass
    # cookie = Get_Cookie()
    # cookie.cookie('http://www.landchina.com/default.aspx?tabid=349&ComName=default')

# print v8_browser.evalScript('(function(){return document.cookie;})()')
# v8_browser = HtmlWindow('http://e.firefoxchina.cn/')
# print v8_browser.evalScript("(function(){return document.body.parentNode.parentNode})()")  # 正确
# print v8_browser.evalScript("(function(){document['cookie']='__jsl_clearance=1544519337.349|0|CcXxyu%2BNue5v%2FMNgidRMGG3oez0%3D;'})()")  # 错误
# print 'v8_browser.context.locals.document.cookie', '<+>' ,v8_browser.context.locals.document.cookie
# print v8_browser.evalScript("(function(){return Promise})()")