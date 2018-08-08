# -*- coding: utf-8 -*-

#import
from thrift.protocol import TCompactProtocol
from thrift.transport import THttpClient
from ttypes import LoginRequest
import json, requests, LineService

#deklarasi nama app dan Headers
nama = 'Aditmadzs'
Headers = {
        'User-Agent': "Line/5.8.0",
        'X-Line-Application': "DESKTOPWIN\t5.8.0\t"+nama+"\t10.0.0",
        "x-lal": "ja-US_US",
    }

#:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-#
#:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-#

#function Login QR
def qrLogin():
    
    #Update Headers pertama
    Headers.update({'x-lpqs' : '/api/v4/TalkService.do'})

    #membentuk Transport
    transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4/TalkService.do')
    transport.setCustomHeaders(Headers)

    #membentuk Protokol
    protocol = TCompactProtocol.TCompactProtocol(transport)

    #membuat client pertama
    client = LineService.Client(protocol)

    #mengambil QR Code
    qr = client.getAuthQrcode(keepLoggedIn=1, systemName=nama)
    #Hasil : (qrcode=u'data:image/jpeg;base64, BlaBlaBla, verifier=u'32digit'

    #ambil qr.verifier 32digit dan print untuk proses Login
    link = "line://au/q/" + qr.verifier
    print(link)

#:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-#
#:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-#

    #Update Headers kedua
    Headers.update({"x-lpqs" : '/api/v4/TalkService.do', 'X-Line-Access': qr.verifier})
    #membuntuk Session
    json.loads(requests.session().get('https://gd2.line.naver.jp/Q', headers=Headers).text)
    #Hasil : {u'timestamp': u'1522246627842', u'result': {u'verifier': u'32digit', u'authPhase': u'QRCODE_VERIFIED', u'metadata': {}}}

#:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-#
#:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-#

    #Update Headers ketiga
    Headers.update({'x-lpqs' : '/api/v4p/rs'})

    #membuat client kedua
    transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4p/rs')
    transport.setCustomHeaders(Headers)
    protocol = TCompactProtocol.TCompactProtocol(transport)
    client = LineService.Client(protocol)

    #membuat parameter LoginRequest
    req = LoginRequest()
    req.type = 1
    req.verifier = qr.verifier
    req.e2eeVersion = 1
    #Hasil : (identifier=None, identityProvider=None, certificate=None, e2eeVersion=1, secret=None, keepLoggedIn=None, verifier=u'32digit', systemName=None, accessLocation=None, password=None, type=1)

    #Proses Login
    res = client.loginZ(req)
    #Hasil : (authToken=u'HasilToken', displayMessage=None, certificate=u'Sertifikat', sessionForSMSConfirm=None, pinCode=None, verifier=None, lastPrimaryBindTime=1521439494501L, type=1)

    #Cetak Token
    print('\n')
    print(res.authToken)

#jalankan fungsi qrLogin
qrLogin()




