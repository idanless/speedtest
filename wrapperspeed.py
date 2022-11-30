import csv
path_to_dat = os.path.abspath(os.path.join(os.path.dirname(__file__), 'speedtest.exe'))
from datetime import date,datetime


#date time\now when the script is run
today = date.today()
time_now = now = datetime.now()
today_is = today.strftime("%d/%m/%Y")
time_is = now.strftime("%H:%M:%S")


def output_csv(IPLan,macAddr,DownLoad,Upload,Ping,PingLow,PingHigh,jitter,result):
    if os.path.exists('SpeedSum.csv'):
        header_exists = True
    else:
        header_exists = False
    with open('SpeedSum.csv', mode='a', newline='') as csv_file:
        fieldnames = ['date', 'time', 'IPLan', 'macAddr', 'DownLoad', 'Upload', 'Ping', 'PingLow', 'PingHigh', 'jitter',
                      'result']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not header_exists:
            writer.writeheader()
        writer.writerow({'date': today_is, 'time': time_is,'IPLan': IPLan,'macAddr':macAddr, 'DownLoad':DownLoad,'Upload':Upload,'Ping':Ping,'PingLow':PingLow,'PingHigh':PingHigh,'jitter':jitter,'result':result})



def run_process(command=[path_to_dat,'-s','18747','-u','Mbps','-f','json']):
    proc = subprocess.Popen(command,
       stdout = subprocess.PIPE,
       stderr = subprocess.PIPE,
       encoding='UtF-8',
    )
    out, err = proc.communicate()
    #print(out)
    return str(out).replace('\n','')

dataJosn = run_process()

y = json.loads(dataJosn)
DownLoad = int((y['download']['bandwidth']/1000)*8)/1000
Upload = int((y['upload']['bandwidth']/1000)*8)/1000
Ping = int((y['ping']['latency']))
jitter = int((y['ping']['jitter']))
PingLow = int((y['ping']['low']))
PingHigh = int((y['ping']['high']))
IPLan = y['interface']['internalIp']
macAddr = y['interface']['macAddr']
result = y['result']['url']

print(IPLan,macAddr,DownLoad,Upload,Ping,PingLow,PingHigh,jitter,result)
output_csv(IPLan=IPLan,macAddr=macAddr,DownLoad=DownLoad,Upload=Upload,Ping=Ping,PingLow=PingLow,PingHigh=PingHigh,jitter=jitter,result=result)

