"""
GLITXH-VIP GENERATOR V1.4 (OPTIMIZED)
Credits : glitxh (tele : @glitxh4ff) 
saluran : https://whatsapp.com/channel/0029VbCM9ME17EmxSJP3ox3j
Modifikasi: Proxy rotasi TOR + Webshare | Minimized N/A | Fast Mode
NOTED : JANGAN DI HAPUS ANGGEP AJA CREDITS! 
"""

import os, sys, subprocess, time, threading, socket, re, json
import hmac, hashlib, string, random, codecs, base64, itertools
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def _i(p, m=None):
    try: __import__(m or p.replace("-","_"))
    except ImportError:
        subprocess.check_call([sys.executable,"-m","pip","install",p,"-q"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

for _p,_m in [("colorama",None),("requests",None),("pycryptodome","Crypto"),
               ("protobuf_decoder","protobuf_decoder"),("urllib3",None),("cfonts",None)]:
    _i(_p,_m)

import requests, urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from colorama import Fore, Style, init
from cfonts import render

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

red=Fore.RED; lg=Fore.LIGHTGREEN_EX; green=Fore.GREEN; bold=Style.BRIGHT
purpel=Fore.MAGENTA; cyan=Fore.CYAN; yellow=Fore.YELLOW; W=Fore.RESET

# ══════════════════════════════════════════════════════════════════
#  FORMAT WAKTU
# ══════════════════════════════════════════════════════════════════
def format_time(seconds):
    seconds = max(0, int(seconds))
    d = seconds//86400; seconds%=86400
    h = seconds//3600;  seconds%=3600
    m = seconds//60;    s = seconds%60
    parts = []
    if d: parts.append(f"{d}hari")
    if h: parts.append(f"{h}jam")
    if m: parts.append(f"{m}menit")
    if s or not parts: parts.append(f"{s}detik")
    return " ".join(parts)

# ══════════════════════════════════════════════════════════════════
#  FILE CHANGE DETECTOR
# ══════════════════════════════════════════════════════════════════
SCRIPT_PATH   = os.path.abspath(__file__)
_SCRIPT_HASH  = None
_pause_event  = threading.Event()
_pause_event.set()

def _get_hash():
    try:
        with open(SCRIPT_PATH,'rb') as f: return hashlib.md5(f.read()).hexdigest()
    except: return None

def _file_detector():
    global _SCRIPT_HASH
    _SCRIPT_HASH = _get_hash()
    while True:
        time.sleep(3)
        h = _get_hash()
        if h and _SCRIPT_HASH and h != _SCRIPT_HASH:
            _pause_event.clear()
            print(f"\n{yellow}{bold}[!] FILE BERUBAH! Restart? (y/n): {W}", end='', flush=True)
            try:
                c = input().strip().lower()
                if c == 'y':
                    os.execv(sys.executable, [sys.executable]+sys.argv)
                else:
                    _SCRIPT_HASH = h
            except: pass
            _pause_event.set()

threading.Thread(target=_file_detector, daemon=True).start()

# ══════════════════════════════════════════════════════════════════
#  TOR SETUP
# ══════════════════════════════════════════════════════════════════
_TOR_PROC    = None
_TOR_READY   = False
_TOR_LOCK    = threading.Lock()
_TOR_RENEWING= False

def _setup_tor():
    global _TOR_PROC, _TOR_READY
    try:
        _resolv="nameserver 1.1.1.1\nnameserver 1.0.0.1\noptions rotate timeout:1 attempts:1\n"
        for p in ['/data/data/com.termux/files/usr/etc/resolv.conf','/etc/resolv.conf']:
            try: os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(_resolv); break
            except: pass
    except: pass
    try: subprocess.run(['pkill','-9','tor'],capture_output=True,check=False); time.sleep(1)
    except: pass
    rc=("SocksPort 127.0.0.1:9050\nControlPort 127.0.0.1:9051\n"
        "CookieAuthentication 0\nMaxCircuitDirtiness 8\nUseEntryGuards 0\n"
        "NumEntryGuards 8\nSafeLogging 0\nLog notice stdout\nClientUseIPv4 1\n"
        "CircuitBuildTimeout 10\nLearnCircuitBuildTimeout 0\nMaxOnionsPending 1024\n")
    tp='/tmp/torrc'
    for p in ['/data/data/com.termux/files/usr/etc/tor/torrc','/tmp/torrc']:
        try: os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(rc); tp=p; break
        except: pass
    _TOR_PROC=subprocess.Popen(['tor','-f',tp],stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,start_new_session=True)
    for _ in range(25):
        time.sleep(1)
        if subprocess.run(['pgrep','-x','tor'],capture_output=True).returncode==0:
            _TOR_READY=True; break

def _renew_tor_bg():
    """Renew TOR di background — tidak block worker."""
    global _TOR_RENEWING
    with _TOR_LOCK:
        if _TOR_RENEWING: return
        _TOR_RENEWING = True
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(4); s.connect(('127.0.0.1',9051))
        s.sendall(b'AUTHENTICATE ""\r\nSIGNAL NEWNYM\r\nQUIT\r\n')
        s.recv(256); s.close()
        time.sleep(2)
    except: pass
    finally:
        _TOR_RENEWING = False

threading.Thread(target=_setup_tor, daemon=True).start()
time.sleep(5)

# ══════════════════════════════════════════════════════════════════
#  PROXY MANAGER — thread-local sessions, rotate tiap N request
# ══════════════════════════════════════════════════════════════════
WEBSHARE_PROXIES = [
    "http://gajuiica:wo29gu5sa2sh@31.59.20.176:6754/",
    "http://gajuiica:wo29gu5sa2sh@92.113.242.158:6742/",
    "http://gajuiica:wo29gu5sa2sh@198.23.239.134:6540/",
    "http://gajuiica:wo29gu5sa2sh@45.38.107.97:6014/",
    "http://gajuiica:wo29gu5sa2sh@107.172.163.27:6543/",
    "http://gajuiica:wo29gu5sa2sh@216.10.27.159:6837/",
    "http://gajuiica:wo29gu5sa2sh@142.111.67.146:5611/",
    "http://gajuiica:wo29gu5sa2sh@191.96.254.138:6185/",
    "http://gajuiica:wo29gu5sa2sh@31.58.9.4:6077/",
    "http://gajuiica:wo29gu5sa2sh@23.229.19.94:8689/",
    "http://cidyiiul:0x1sq2qkuk6a@31.59.20.176:6754/",
    "http://cidyiiul:0x1sq2qkuk6a@92.113.242.158:6742/",
    "http://cidyiiul:0x1sq2qkuk6a@198.23.239.134:6540/",
    "http://cidyiiul:0x1sq2qkuk6a@45.38.107.97:6014/",
    "http://cidyiiul:0x1sq2qkuk6a@107.172.163.27:6543/",
    "http://cidyiiul:0x1sq2qkuk6a@216.10.27.159:6837/",
    "http://cidyiiul:0x1sq2qkuk6a@142.111.67.146:5611/",
    "http://cidyiiul:0x1sq2qkuk6a@191.96.254.138:6185/",
    "http://cidyiiul:0x1sq2qkuk6a@31.58.9.4:6077/",
    "http://cidyiiul:0x1sq2qkuk6a@23.229.19.94:8689/",
    "http://ffrevdai:kapukxzd8av3@31.59.20.176:6754/",
    "http://ffrevdai:kapukxzd8av3@92.113.242.158:6742/",
    "http://ffrevdai:kapukxzd8av3@198.23.239.134:6540/",
    "http://ffrevdai:kapukxzd8av3@45.38.107.97:6014/",
    "http://ffrevdai:kapukxzd8av3@107.172.163.27:6543/",
    "http://ffrevdai:kapukxzd8av3@216.10.27.159:6837/",
    "http://ffrevdai:kapukxzd8av3@142.111.67.146:5611/",
    "http://ffrevdai:kapukxzd8av3@191.96.254.138:6185/",
    "http://ffrevdai:kapukxzd8av3@31.58.9.4:6077/",
    "http://ffrevdai:kapukxzd8av3@23.229.19.94:8689/",
    "http://nfjndowc:vuc84qb19nsg@31.59.20.176:6754/",
    "http://nfjndowc:vuc84qb19nsg@92.113.242.158:6742/",
    "http://nfjndowc:vuc84qb19nsg@198.23.239.134:6540/",
    "http://nfjndowc:vuc84qb19nsg@45.38.107.97:6014/",
    "http://nfjndowc:vuc84qb19nsg@107.172.163.27:6543/",
    "http://nfjndowc:vuc84qb19nsg@216.10.27.159:6837/",
    "http://nfjndowc:vuc84qb19nsg@142.111.67.146:5611/",
    "http://nfjndowc:vuc84qb19nsg@191.96.254.138:6185/",
    "http://nfjndowc:vuc84qb19nsg@31.58.9.4:6077/",
    "http://nfjndowc:vuc84qb19nsg@23.229.19.94:8689/",
]

VALID_REGIONS = ["ME","IND","ID","VN","TH","BD","PK","TW","EU","CIS","NA","SAC","BR","SG"]

# Proxy state — global tapi lock minimal
_pidx      = 0
_pidx_lock = threading.Lock()
_use_tor   = False
_tor_ts    = time.time()  # kapan terakhir switch ke TOR
_local     = threading.local()

def _get_session():
    """
    Thread-local session pool.
    Setiap thread punya session sendiri, di-refresh tiap 8 request.
    Switch TOR ↔ Webshare berdasarkan waktu (non-blocking).
    """
    global _use_tor, _tor_ts, _pidx

    # Tentukan mode proxy (non-blocking, hanya baca/tulis 1 bool)
    now = time.time()
    if now - _tor_ts >= 5:
        _use_tor = not _use_tor
        _tor_ts  = now
        if _use_tor and not _TOR_RENEWING:
            threading.Thread(target=_renew_tor_bg, daemon=True).start()

    # Init thread-local state
    if not hasattr(_local,'count'): _local.count=0; _local.sess=None
    _local.count += 1

    # Refresh session tiap 8 request
    if _local.sess is None or _local.count % 8 == 0:
        s = requests.Session()
        s.verify = False
        a = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=20, max_retries=0)
        s.mount('http://',a); s.mount('https://',a)
        if _use_tor and _TOR_READY:
            s.proxies = {'http':'socks5h://127.0.0.1:9050',
                         'https':'socks5h://127.0.0.1:9050'}
        else:
            with _pidx_lock:
                p = WEBSHARE_PROXIES[_pidx % len(WEBSHARE_PROXIES)]
                _pidx += 1
            s.proxies = {'http':p,'https':p}
        _local.sess = s

    return _local.sess

# ══════════════════════════════════════════════════════════════════
#  GLOBAL STATE
# ══════════════════════════════════════════════════════════════════
hex_key = "32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533"
key     = bytes.fromhex(hex_key)

file_lock   = threading.Lock()
print_lock  = threading.Lock()
cnt_lock    = threading.Lock()
stuck_lock  = threading.Lock()
tier_lock   = threading.Lock()

total_accounts       = 0
num_workers          = 20
success_count        = 0
_stuck_running       = True
_last_success        = time.time()
_start_time          = time.time()
_last_100_time       = time.time()
_last_100_count      = 0
start_time_progress  = time.time()
last_progress_time   = time.time()
last_progress_count  = 0

tier_stats = {"NORMAL":0,"LOW":0,"MEDIUM":0,"HIGH":0,"LEGEND":0}
TIER_EMOJIS = {"NORMAL":"🍀","LOW":"😬","MEDIUM":"🤩","HIGH":"☠️","LEGEND":"❤️‍🔥"}
TIER_COLORS = {"LEGEND":Fore.RED+Style.BRIGHT,"HIGH":Fore.MAGENTA+Style.BRIGHT,
               "MEDIUM":Fore.CYAN+Style.BRIGHT,"LOW":Fore.YELLOW,"NORMAL":Fore.GREEN}

REGION_LANG = {"ME":"ar","IND":"hi","ID":"id","VN":"vi","TH":"th","BD":"bn",
               "PK":"ur","TW":"zh","EU":"en","CIS":"ru","NA":"en","SAC":"es",
               "BR":"pt","SG":"en"}

BASE_DIR = "/sdcard/GLITXH-VIP"
_tf_cache = {}

def get_tier_files(region):
    ru = region.upper()
    rd = os.path.join(BASE_DIR,ru)
    for sub in [rd,os.path.join(rd,"LEGENDA"),os.path.join(rd,"High"),
                os.path.join(rd,"Medium"),os.path.join(rd,"Low"),
                os.path.join(rd,"Normal")]:
        os.makedirs(sub,exist_ok=True)
    return {"LEGEND":os.path.join(rd,"LEGENDA",f"Account-{ru}.json"),
            "HIGH":  os.path.join(rd,"High",   f"Account-{ru}.json"),
            "MEDIUM":os.path.join(rd,"Medium", f"Account-{ru}.json"),
            "LOW":   os.path.join(rd,"Low",    f"Account-{ru}.json"),
            "NORMAL":os.path.join(rd,"Normal", f"Account-{ru}.json")}

def cached_tf(region):
    if region not in _tf_cache: _tf_cache[region]=get_tier_files(region)
    return _tf_cache[region]

# ── Stuck detector — hanya success_count ──────────────────────────
def _stuck_loop():
    global _stuck_running,_last_success
    while _stuck_running:
        time.sleep(5)
        with stuck_lock: idle=time.time()-_last_success
        if total_accounts>0 and success_count>=total_accounts: break
        if idle>=25:
            threading.Thread(target=_renew_tor_bg,daemon=True).start()
            with stuck_lock: _last_success=time.time()

threading.Thread(target=_stuck_loop,daemon=True).start()

# ══════════════════════════════════════════════════════════════════
#  TIER
# ══════════════════════════════════════════════════════════════════
def calculate_tier(aid):
    if not aid or aid=="N/A": return "NORMAL"
    s=0
    if len(aid)>=6:
        rem=aid[3:]
        if len(set(aid))==1: s+=30
        elif len(set(rem))==1: s+=25
        elif aid[:3] in["154","155","156","157","158","159"] and len(set(rem))==1: s+=28
    for pat,pts in [(r'(\d)\1{5,}',10),(r'(\d)\1{4,}',8),(r'(\d)\1{3,}',6),(r'(\d)\1{2,}',3)]:
        if re.search(pat,aid): s+=pts; break
    if re.search(r'(12345|23456|34567|45678|56789|98765|87654|76543|65432|54321)',aid): s+=7
    elif re.search(r'(1234|2345|3456|4567|5678|6789|9876|8765|7654|6543|5432|4321)',aid): s+=4
    if len(aid)>=6 and aid==aid[::-1]: s+=8
    elif len(aid)>=4 and aid[:2]==aid[-1:-3:-1]: s+=4
    if len(aid)>=6 and len(set(aid[::2]))==1 and len(set(aid[1::2]))==1: s+=6
    for sn in['888','999','666','777','000','123','321','111','222','333','444','555']:
        if sn in aid: s+=2
    if len(aid)<=8: s+=5
    elif len(aid)<=9: s+=3
    if s>=20: return "LEGEND"
    if s>=12: return "HIGH"
    if s>=6:  return "MEDIUM"
    if s>=2:  return "LOW"
    return "NORMAL"

def save_by_tier(entry,tier,region):
    if entry.get("account_id")=="N/A": return
    fp=cached_tf(region).get(tier)
    if not fp: return
    with file_lock:
        try:
            data=json.load(open(fp,'r',encoding='utf-8')) if os.path.exists(fp) else []
            if not isinstance(data,list): data=[data]
            data.append(entry)
            json.dump(data,open(fp,'w',encoding='utf-8'),indent=4,ensure_ascii=False)
        except: pass

# ══════════════════════════════════════════════════════════════════
#  CRYPTO
# ══════════════════════════════════════════════════════════════════
_AES_KEY=bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
_AES_IV =bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])

def aes_enc(hex_pt) -> bytes:
    pt=bytes.fromhex(hex_pt)
    return AES.new(_AES_KEY,AES.MODE_CBC,_AES_IV).encrypt(pad(pt,AES.block_size))

def aes_enc_hex(hex_pt) -> str:
    return aes_enc(hex_pt).hex()

def enc_varint(n):
    if n<0: return b''
    h=[]
    while True:
        b=n&0x7F; n>>=7
        if n: b|=0x80
        h.append(b)
        if not n: break
    return bytes(h)

def proto_varint(f,v): return enc_varint((f<<3)|0)+enc_varint(v)
def proto_len(f,v):
    p=v.encode() if isinstance(v,str) else v
    return enc_varint((f<<3)|2)+enc_varint(len(p))+p

def build_proto(fields):
    pkt=bytearray()
    for f,v in fields.items():
        if isinstance(v,dict):  pkt.extend(proto_len(f,build_proto(v)))
        elif isinstance(v,int): pkt.extend(proto_varint(f,v))
        else:                   pkt.extend(proto_len(f,v))
    return bytes(pkt)

def encode_oid(orig):
    ks=[0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,
        0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,
        0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,
        0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
    enc="".join(chr(ord(c)^ks[i%len(ks)]) for i,c in enumerate(orig))
    return {"open_id":orig,"field_14":enc}

def to_ue(s):
    return "".join(c if 32<=ord(c)<=126 else f"\\u{ord(c):04x}" for c in s)

def decode_jwt(token):
    """
    Fix: cari JWT dengan lebih robust — tidak hanya dari posisi 'eyJ'.
    Coba semua kemungkinan posisi JWT di response text.
    """
    # Pola JWT standard FF
    JWT_PREFIX = "eyJhbGciOiJIUzI1NiIsInN2ciI6IjEiLCJ0eXAiOiJKV1QifQ"
    try:
        # Cari prefix spesifik dulu
        idx = token.find(JWT_PREFIX)
        if idx == -1:
            # Fallback: cari eyJ manapun
            idx = token.find("eyJ")
        if idx == -1: return "N/A"
        jwt = token[idx:]
        d1  = jwt.find(".")
        if d1 == -1: return "N/A"
        d2  = jwt.find(".", d1+1)
        if d2 == -1: return "N/A"
        # Ambil payload
        pl = jwt[d1+1:d2]
        pl += "=" * ((4-len(pl)%4)%4)
        d  = json.loads(base64.urlsafe_b64decode(pl).decode())
        for k in ('account_id','external_id','user_id','uid'):
            if k in d and d[k]: return str(d[k])
    except: pass
    return "N/A"

# ══════════════════════════════════════════════════════════════════
#  USER AGENTS
# ══════════════════════════════════════════════════════════════════
_UA_LIST = [
    "GarenaMSDK/4.0.39(SM-A325M;Android 13;en;HK;)",
    "GarenaMSDK/4.0.39(Poco F3;Android 12;en;SG;)",
    "GarenaMSDK/4.0.39(Redmi Note 10;Android 11;en;ID;)",
    "GarenaMSDK/4.0.39(Samsung A52;Android 12;en;MY;)",
    "GarenaMSDK/4.0.39(Oppo Reno5;Android 11;en;PH;)",
    "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
    "GarenaMSDK/4.0.39(CPH2359;Android 12;en;US;)",
    "GarenaMSDK/4.0.39(NE2213;Android 13;en;EU;)",
    "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
    "Dalvik/2.1.0 (Linux; U; Android 12; M2101K7AG Build/SKQ1.210908.001)",
]
_ua_idx=0; _ua_lock=threading.Lock()

def _next_ua():
    global _ua_idx
    with _ua_lock:
        ua=_UA_LIST[_ua_idx%len(_UA_LIST)]; _ua_idx+=1
    return ua

def gen_name(): return 'N4taza'+''.join(random.choice(string.ascii_uppercase+string.digits) for _ in range(6))
def gen_pw(n=9): return f"N4TAZA-{''.join(random.choice(string.ascii_uppercase+string.digits) for _ in range(n))}-VVIP"

# ══════════════════════════════════════════════════════════════════
#  API — fix N/A dengan retry & fallback
# ══════════════════════════════════════════════════════════════════
_REG_URL  = "https://100067.connect.garena.com/api/v2/oauth/guest:register"
_TOK_URL  = "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"

def _register(pw):
    """
    Register via v2 API dengan HMAC signature.
    Retry 4x dengan delay 0.3s.
    """
    body_json = json.dumps({"app_id":100067,"client_type":2,"password":pw,"source":2},
                           separators=(",",":"))
    sig = hmac.new(key, body_json.encode(), hashlib.sha256).hexdigest()
    hdrs = {"User-Agent":_next_ua(),
            "Authorization":f"Signature {sig}",
            "Content-Type":"application/json; charset=utf-8",
            "Accept":"application/json",
            "Connection":"Keep-Alive",
            "Host":"100067.connect.garena.com"}
    for _ in range(4):
        try:
            r=_get_session().post(_REG_URL,headers=hdrs,data=body_json,timeout=12)
            if r.status_code in (403,429): time.sleep(1); continue
            b=r.json(); d=b.get("data",b)
            uid=d.get("uid") or b.get("uid")
            if uid: return uid
        except: pass
        time.sleep(0.3)
    return None

def _get_token(uid,pw):
    """
    Grant token via v2 API.
    Fix: key harus str untuk client_secret, bukan bytes.
    """
    client_secret = key.decode("ascii")
    body_json = json.dumps({"client_id":100067,"client_secret":client_secret,
                             "client_type":2,"password":pw,
                             "response_type":"token","uid":uid},
                           separators=(",",":"))
    sig = hmac.new(key, body_json.encode(), hashlib.sha256).hexdigest()
    hdrs = {"User-Agent":_next_ua(),
            "Authorization":f"Signature {sig}",
            "Content-Type":"application/json; charset=utf-8",
            "Accept":"application/json",
            "Connection":"Keep-Alive",
            "Host":"100067.connect.garena.com"}
    for _ in range(3):
        try:
            r=_get_session().post(_TOK_URL,headers=hdrs,data=body_json,timeout=12)
            if r.status_code in (403,429): time.sleep(1); continue
            b=r.json(); d=b.get("data",b)
            if "open_id" in d:
                oi=d["open_id"]; at=d["access_token"]
                res=encode_oid(oi)
                field=codecs.decode(to_ue(res["field_14"]),"unicode_escape").encode("latin1")
                return oi,at,field
        except: pass
        time.sleep(0.3)
    return None,None,None

_LOGIN_PL=(
    b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28'
    b' (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05'
    b'r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640'
    b'\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f'
    b'\xa2\x01\x0e105.235.139.91\xaa\x01\x02'
)
_LOGIN_PL2=(
    b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d'
    b'\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA'
    b'\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390'
    b'\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI'
    b'\xca\x03 7428b253defc164018c604a1ebbfebdf'
    b'\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07'
    b'\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02'
    b'\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm'
    b'\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9'
    b'|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk'
    b'\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692'
    b'\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F'
    b'\xea\x05\x07android'
    b'\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3pt'
    b'NrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2'
    b'\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014'
    b'\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
)
_AT_PH = b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390'
_OI_PH = b'1d8ec0240ede109973f3321b9354b44d'

def _major_register(at,oi,field,uid,pw,region):
    name=gen_name()
    lang=REGION_LANG.get(region.upper(),"en")
    if region.upper() in("ME","TH"):
        url="https://loginbp.common.ggbluefox.com/MajorRegister"; host="loginbp.common.ggbluefox.com"
    else:
        url="https://loginbp.ggblueshark.com/MajorRegister"; host="loginbp.ggblueshark.com"
    pl=build_proto({1:name,2:at,3:oi,5:102000007,6:4,7:1,13:1,14:field,15:lang,16:1,17:1})
    body=aes_enc(pl.hex())
    try:
        _get_session().post(url,headers={
            "Accept-Encoding":"gzip","Authorization":"Bearer","Connection":"Keep-Alive",
            "Content-Type":"application/x-www-form-urlencoded","Expect":"100-continue",
            "Host":host,"ReleaseVersion":"OB53","User-Agent":_next_ua(),
            "X-GA":"v1 1","X-Unity-Version":"2018.4."},
            data=body,verify=False,timeout=12)
    except: pass
    return name

def _major_login(at,oi,region,retry=3):
    """
    Fix N/A: retry 3x, parse JWT lebih robust.
    """
    lang=REGION_LANG.get(region.upper(),"en")
    if region.upper() in("ME","TH"):
        url="https://loginbp.common.ggbluefox.com/MajorLogin"; host="loginbp.common.ggbluefox.com"
    else:
        url="https://loginbp.ggblueshark.com/MajorLogin"; host="loginbp.ggblueshark.com"
    raw=_LOGIN_PL+lang.encode("ascii")+_LOGIN_PL2
    raw=raw.replace(_AT_PH,at.encode()).replace(_OI_PH,oi.encode())
    fp=bytes.fromhex(aes_enc_hex(raw.hex()))
    hdrs={"Accept-Encoding":"gzip","Authorization":"Bearer","Connection":"Keep-Alive",
          "Content-Type":"application/x-www-form-urlencoded","Expect":"100-continue",
          "Host":host,"ReleaseVersion":"OB53","User-Agent":_next_ua(),
          "X-GA":"v1 1","X-Unity-Version":"2018.4.11f1"}
    for _ in range(retry):
        try:
            r=_get_session().post(url,headers=hdrs,data=fp,verify=False,timeout=15)
            if r.status_code==200 and len(r.text)>10:
                aid=decode_jwt(r.text)
                if aid!="N/A": return aid,r.text
        except: pass
        time.sleep(0.5)
    return "N/A",""

def _bind_region(jwt_token,region):
    if region.upper() in("ME","TH"):
        url="https://loginbp.common.ggbluefox.com/ChooseRegion"
    else:
        url="https://loginbp.ggblueshark.com/ChooseRegion"
    rk="RU" if region.upper()=="CIS" else region.upper()
    pl=bytes.fromhex(aes_enc_hex(build_proto({1:rk}).hex()))
    try:
        _get_session().post(url,data=pl,headers={
            "User-Agent":_next_ua(),"Connection":"Keep-Alive","Accept-Encoding":"gzip",
            "Content-Type":"application/x-www-form-urlencoded","Expect":"100-continue",
            "Authorization":f"Bearer {jwt_token}",
            "X-Unity-Version":"2018.4.11f1","X-GA":"v1 1","ReleaseVersion":"OB53"},
            verify=False,timeout=10)
    except: pass

def create_account(region):
    """
    Full flow: register → token → major_register → major_login → bind.
    Return dict atau None. Tidak pernah return N/A account.
    """
    pw  = gen_pw()
    uid = _register(pw)
    if not uid: return None

    oi,at,field = _get_token(uid,pw)
    if not oi: return None

    name = _major_register(at,oi,field,uid,pw,region)
    aid,jwt = _major_login(at,oi,region)

    if aid=="N/A": return None  # buang — worker akan coba lagi

    if jwt and region.upper()!="BR":
        threading.Thread(target=_bind_region,args=(jwt,region),daemon=True).start()

    return {"uid":uid,"password":pw,"name":name,
            "account_id":aid,"region":region,"status":"success"}

# ══════════════════════════════════════════════════════════════════
#  OUTPUT
# ══════════════════════════════════════════════════════════════════
def add_output(result,region):
    global success_count,_last_success,last_progress_time,last_progress_count

    uid  = result["uid"]; pw   = result["password"]
    name = result["name"]; aid = result["account_id"]
    tier = calculate_tier(aid)
    te   = TIER_EMOJIS.get(tier,"🍀")
    tc   = TIER_COLORS.get(tier,Fore.GREEN)
    ts   = datetime.now().strftime('%H:%M:%S')

    with tier_lock: tier_stats[tier]=tier_stats.get(tier,0)+1

    success_count+=1; cur=success_count
    with stuck_lock: _last_success=time.time()

    entry={"uid":uid,"password":pw,"account_id":aid,"name":name,
           "region":region,"tier":tier,
           "created_at":datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    save_by_tier(entry,tier,region)

    with print_lock:
        print(f"[{ts}] {green}✅{W} {cur} | {tc}ID:{aid} ({te}){W} | {uid} | {pw}")

        if cur%100==0 and cur>0:
            now        = time.time()
            el_total   = now-start_time_progress
            rate       = cur/el_total if el_total>0 else 0
            el_100     = now-last_progress_time if last_progress_count>0 else el_total
            total_s    = f"/{total_accounts}" if total_accounts>0 else ""
            with tier_lock: ts2=dict(tier_stats)
            print(f"\n{cyan}{bold}▶ PROGRESS {cur}{total_s} | "
                  f"+100: {format_time(el_100)} | total: {format_time(el_total)} | "
                  f"{rate:.2f}/detik{W}")
            print(f"  {green}🍀:{ts2['NORMAL']}{W} "
                  f"{yellow}😬:{ts2['LOW']}{W} "
                  f"{cyan}🤩:{ts2['MEDIUM']}{W} "
                  f"{purpel}☠️:{ts2['HIGH']}{W} "
                  f"{red}❤️‍🔥:{ts2['LEGEND']}{W}\n")
            last_progress_time  = now
            last_progress_count = cur

# ══════════════════════════════════════════════════════════════════
#  WORKER — loop sampai target, N/A dibuang & retry otomatis
# ══════════════════════════════════════════════════════════════════
def worker(region):
    global success_count
    while True:
        if not _pause_event.is_set(): _pause_event.wait()
        with cnt_lock:
            if total_accounts>0 and success_count>=total_accounts: return

        result = None
        try: result=create_account(region)
        except: pass

        if not result: continue  # gagal/N/A → coba lagi

        with cnt_lock:
            if total_accounts>0 and success_count>=total_accounts: return

        add_output(result,region)

        with cnt_lock:
            if total_accounts>0 and success_count>=total_accounts: return

# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════
if __name__=="__main__":
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        print(f"{render('x6ataza',colors=['white','red'],align='center')}\n\n")

        while True:
            region=input(f" {Style.NORMAL}{Fore.RESET}- Enter Region "
                         f"(ME,IND,ID,VN,TH,BR..) >>> {Fore.WHITE}").upper().strip()
            if region in VALID_REGIONS: break
            print(f"{red}[ ! ] Region tidak valid.{W}")

        while True:
            try:
                jml=input(f" {Style.NORMAL}{Fore.RESET}- Jumlah ID (0=unlimited) >>> {Fore.WHITE}").strip()
                if jml=="0" or (jml.isdigit() and int(jml)>=0):
                    total_accounts=int(jml); break
            except: pass

        try:
            wk=input(f" {Style.NORMAL}{Fore.RESET}- Workers [{num_workers}] >>> {Fore.WHITE}").strip()
            if wk.isdigit() and int(wk)>0: num_workers=min(int(wk),60)
        except: pass

        # Reset
        success_count=0; _stuck_running=True
        last_progress_time=time.time(); last_progress_count=0
        for k in tier_stats: tier_stats[k]=0
        cached_tf(region)

        print()
        _last_success=time.time()
        start_time_progress=time.time()

        try:
            with ThreadPoolExecutor(max_workers=num_workers) as ex:
                futures=[ex.submit(worker,region) for _ in range(num_workers)]
                for f in futures: f.result()
        except KeyboardInterrupt:
            print(f"\n{yellow}[ ! ] Dihentikan.{W}")

        _stuck_running=False
        elapsed=time.time()-start_time_progress
        spd=success_count/elapsed if elapsed>0 else 0
        tf=cached_tf(region)

        print(f"\n{lg}{bold}✓ Selesai! {success_count}"
              f"{'/' + str(total_accounts) if total_accounts>0 else ''} akun{W}")
        print(f"{cyan}{bold}⏱ Waktu : {format_time(elapsed)} | {spd:.2f} akun/detik{W}")
        print(f"{lg}{bold}📁 {BASE_DIR}/{region}/{W}")
        print(f"\n{cyan}[ i ] Final Stats:{W}")
        print(f"  {green}🍀 NORMAL  : {tier_stats['NORMAL']}{W}")
        print(f"  {yellow}😬 LOW     : {tier_stats['LOW']}{W}")
        print(f"  {cyan}🤩 MEDIUM  : {tier_stats['MEDIUM']}{W}")
        print(f"  {purpel}☠️  HIGH    : {tier_stats['HIGH']}{W}")
        print(f"  {red}❤️‍🔥 LEGEND : {tier_stats['LEGEND']}{W}")

        try:
            input(f"\n{Style.NORMAL}{Fore.RESET} tekan enter untuk generate ulang.. {Fore.RESET}")
        except (KeyboardInterrupt,EOFError):
            if _TOR_PROC:
                try: _TOR_PROC.terminate()
                except: pass
            break
