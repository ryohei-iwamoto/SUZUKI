import urllib.request, urllib.error
from bs4 import BeautifulSoup
import subprocess
import requests
import socks, socket
import ssl


# Tor = f'C:\\Users\\celeron\\Desktop\\tor-expert-bundle-12.0.4-windows-x86_64\\tor\\tor.exe'
# running = subprocess.Popen(Tor)


# socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
# socket.socket = socks.socksocket


# URLからHTMLを返す
def fetch_html(url):
    res = urllib.request.urlopen(url)
    return BeautifulSoup(res, 'html.parser')


# 現在のグローバルIPアドレスを返す
def get_ip_addr():
    html = fetch_html('http://checkip.dyndns.com/')
    return html.body.text.split(': ')[1]


# Torを使っているかを返す
def check_use_tor():
    html = fetch_html('https://check.torproject.org/')
    return html.find('h1')['class'][0] != 'off'








# ログインページのURL
login_url = 'https://stn.suzuki.co.jp/sios/menu/login.jsp'


# セッションを作成
session = requests.Session()
session.verify = False
# store_names = ssl.enum_certificates()


# ログインページにアクセス
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')


# ログインに必要なフォームデータを取得
# login_form = soup.find({'id': 'login-form'})
login_form = soup


form_data = {}
for input_field in login_form.find_all('input'):
    field_name = input_field.get('name')
    field_value = input_field.get('value')
    if field_name:
        form_data[field_name] = field_value


# フォームデータにユーザー名とパスワードを追加
# form_data['username'] = "je000000'or'1'='1"
# form_data['password'] = "'or'1'='1"
form_data['j_username'] = "EBW0063768H"
form_data['j_password'] = "57110TTAJ92"



# ログインを実行
response = session.post(login_url, data=form_data)


# セッション情報を表示
print("###############")
print(session.cookies)
print("###############")
print(response)
print("###############")


# ログイン後のページにアクセス
main_url = 'https://biz.honda.co.jp/gpj10/plsearch.part.do'
form_data = {}




# operation: searchParts
# field(target):
# field(partnr):
# field(isaccessorypart):
# field(partdesc):
# field(scrollSize): 15
# field(direction): NONE
# field(rowpos): 0
# field(partprice):
# field(modelname):
# field(petname):
# field(selectedModel):
# field(wsOrigin):
# field(pinhin):
# field(enginenr):
# field(partslist):
# field(fprefix):
# field(fstart):
# field(fend):
# field(eprefix):
# field(model):
# field(key):
# field(attachment):
# field(searchpartnr): 08W16-S47-A0004
# field(flag): Y
# field(searchpartdesc):







response = session.post(main_url, data=form_data)






# ログイン後のページの内容を表示
print("!!!!!!!!!!!!!!!!!!")
print(response.text)
print("!!!!!!!!!!!!!!!!!!")








print('You are using tor.' if check_use_tor() else 'You are not using tor.')
print('Current IP address is ' + get_ip_addr())

