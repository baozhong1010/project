# coding=utf-8
from browser import HtmlWindow

v8_browser = HtmlWindow('http://www.landchina.com/default.aspx?tabid=347&ComName=default')
print v8_browser.doc
script = v8_browser.doc.getElementsByTagName('script')[0].text.strip()
print script
v8_browser.evalScript(script)
try:
    v8_browser.evalScript("YunSuoAutoJump()")
except:
    pass

print 'v8_browser.context.locals.document.cookie', v8_browser.context.locals.document.cookie
# print v8_browser.evalScript('(function(){return document.cookie;})()')
# v8_browser = HtmlWindow('http://e.firefoxchina.cn/')
# print v8_browser.evalScript("(function(){return document.body.parentNode.parentNode})()")  # 正确
# print v8_browser.evalScript("(function(){document['cookie']='__jsl_clearance=1544519337.349|0|CcXxyu%2BNue5v%2FMNgidRMGG3oez0%3D;'})()")  # 错误
# print 'v8_browser.context.locals.document.cookie', '<+>' ,v8_browser.context.locals.document.cookie
# print v8_browser.evalScript("(function(){return Promise})()")