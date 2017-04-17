# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:28:01 2017

@author: dapenghuang
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import httplib
import md5
import urllib
import random
import urllib2

appid = '20170417000045035'
secretKey = 'rBp0CfklktvWAAHoMNfJ'

 
httpClient = None
myurl = '/api/trans/vip/translate'
myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

q = u'ดราม่าข้าวแกงกล่องละ 90 บ. เจ้าของร้านเผย ติดป้ายบอกราคาชัดเจน แจงปลาสีเสียดชิ้นเดียว 50 บาทแล้ว ชี้เป็นราคาที่จำหน่ายปกติในทุกวัน อ้างปลาชนิดนี้ราคาสูง... อ่านต่อที่'
#q = u'this is a test'
q = q.encode('utf-8')
fromLang = 'th'
toLang = 'zh'
salt = random.randint(32768, 65536)

sign = appid+q+str(salt)+secretKey
m1 = md5.new()
m1.update(sign)
sign = m1.hexdigest()
myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
      
proxy = urllib2.ProxyHandler({'http': 'proxy.tencent.com:8080'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
result =  urllib2.urlopen(myurl).read()
result_dic = eval(result)
print result_dic
f = open('D://result.txt','w')
result_s = result_dic['trans_result'][0]['dst'].decode('unicode_escape').encode('utf-8')
print result_s
f.write(result_s)
f.close()