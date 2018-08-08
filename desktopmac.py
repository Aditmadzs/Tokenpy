from thrift.protocol import TCompactProtocol
from thrift.transport import THttpClient
from ttypes import LoginRequest
import json, requests, LineService

nama = 'Aditmadzs'
Headers = {
        'User-Agent': "Line/5.8.0",
        'X-Line-Application': "DESKTOPMAC\t5.8.0\t"+nama+"\t10.0.0",
        "x-lal": "ja-US_US",
    }
def qrLogin():
    Headers.update({'x-lpqs' : '/api/v4/TalkService.do'})
    transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4/TalkService.do')
    transport.setCustomHeaders(Headers)
    protocol = TCompactProtocol.TCompactProtocol(transport)
    client = LineService.Client(protocol)
    qr = client.getAuthQrcode(keepLoggedIn=1, systemName=nama)
    link = "line://au/q/" + qr.verifier
    print(link)
    Headers.update({"x-lpqs" : '/api/v4/TalkService.do', 'X-Line-Access': qr.verifier})
    json.loads(requests.session().get('https://gd2.line.naver.jp/Q', headers=Headers).text)
    Headers.update({'x-lpqs' : '/api/v4p/rs'})
    transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4p/rs')
    transport.setCustomHeaders(Headers)
    protocol = TCompactProtocol.TCompactProtocol(transport)
    client = LineService.Client(protocol)
    req = LoginRequest()
    req.type = 1
    req.verifier = qr.verifier
    req.e2eeVersion = 1
    res = client.loginZ(req)
    print('\n')
    print(res.authToken)
qrLogin()




