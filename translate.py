# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:28:01 2017

@author: dapenghuang
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#import httplib
import md5
import urllib
import random
import urllib2
from pythainlp.segment import segment
import time


class Log:
    def __init__(self,logPath = '/home/hp/CODE/AD/LOG/log.txt'):
        self.file = logPath
    def write(self , info , infoType = 'INFO'):
        '''append log info in log
        input:
            @info : log text
        '''
        try:
            s = '[%s][%s]%s' % (infoType , time.ctime() , info)
            print s
            f = open(self.file , 'w')
            f.write(s)
            f.write('\n')
            f.close()
        except Exception as e:
            print "Someting wrong when record log. The error info are : %s" %e
            

class DealWithText:
    def __init__(self):
        '''init the class
        '''
        pass
    def read(self , fileFullPath):
        '''read text in file
        input:
            @fileFullPath ex:'/home/hp/code/AD/data/thai.txt'
        output:
            strings
        '''
        try:
            f = open(fileFullPath)
            s = u''
            for l in f.readlines():
                pureL = l.strip('\n').strip(' ').strip('\t').strip('\r').strip('\r\n')
                pureL = ''.join(l.split())
                #pureL = l.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                if pureL != '':
                    s += pureL
            f.close()
            return s.strip('\n')
        except Exception as e:
            Log().write(e ,'Error')
            
        return False
    def write(self , text , fileFullPath):
        '''write text in file
        input:
            @fileFullPath ex:'/home/hp/code/AD/data/thai.txt'
            @text : strings
        output:
            True if success else False
        '''
        try:
            f = open(fileFullPath , 'w')
            f.write(text)
            f.write('\n')
            f.close()
            return True
        except Exception as e:
            Log().write(e , 'Error')
            
        return False
    
class TranslateUseBaidu:
    def __init__(self , appid = '20170417000045035' , secretKey = 'rBp0CfklktvWAAHoMNfJ' , isProxy = False):
        self.appid = appid
        self.secretKey = secretKey
        self.isProxy = False
    def translate(self, text ,fromLang = 'th' , toLang = 'en' , proxyPath = 'proxy.tencent.com:8080'):
        '''translate text with baidu api
        input:
            @text
            @fromLang
            @toLang
            @proxy
        outPut:
            strings
        '''
        text = text.decode('utf-8')
        salt = random.randint(32768, 65536)
        sign = self.appid+text+str(salt)+self.secretKey
        m1 = md5.new()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        myurl = myurl+'?appid='+self.appid+'&q='+urllib.quote(text.encode('utf-8'))+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
        
        if self.isProxy:
            proxy = urllib2.ProxyHandler({'http': proxyPath})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
        
        result =  urllib2.urlopen(myurl).read()
        result_dic = eval(result)
        
        if 'error_code' in result_dic.keys():
            Log().write('Something worong when use baidu API.Error code : %s , error message : %s' % (result_dic['error_code'] , result_dic['error_msg']), 'Error')
            return False
        
        
        
        result_text = result_dic['trans_result'][0]['dst'].decode('unicode_escape').encode('utf-8')
        Log().write('translate from %s to %s complete.' % (fromLang , toLang))
        return result_text

class CutThaiLanguage:
    def __init__(self):
        '''
        '''
        pass
    def cutSentence(self , sentence):
        '''cut thai language
        input:
            @sentence : input text
        output:
            a list of words
        '''
        try:
            result_cut = segment(sentence)
            Log().write('thai language cut words complete.' )
            return result_cut
        except Exception as e:
            Log().write(e , 'Error')
        return False
    

languageFile = '/home/hp/CODE/AD/data/thai.txt'
DWT = DealWithText()
strings = DWT.read(languageFile)
transAPP =  TranslateUseBaidu()
thai2en = transAPP.translate(strings ,fromLang = 'th', toLang = 'en')
thai2zh = transAPP.translate(strings , toLang = 'zh')
cutThai = CutThaiLanguage().cutSentence(strings)
cutThaiStrings = u''
for s in cutThai:
    cutThaiStrings += s + '  '
    
print '--------------------------'
print strings
print '--------------------------'
print thai2en
print '--------------------------'
print thai2zh
print '--------------------------'
print cutThaiStrings
    
thai2enF = '/home/hp/CODE/AD/data/thai2en.txt'
thai2zhF = '/home/hp/CODE/AD/data/thai2zh.txt'
thaiCutF = '/home/hp/CODE/AD/data/thaicut.txt'
DWT.write(thai2en , thai2enF)
DWT.write(thai2zh , thai2zhF)
DWT.write(cutThaiStrings , thaiCutF)
