from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import paramiko
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


def send_to_keenetic(ind_unit:int, ind_vpn:int)->str:

    host = '192.168.1.1'
    user = 'admin'
    secret = 'Q2w3e4r5'
    port = 22
    macs = [{'name': 'Kitchen tv', 'mac': '80:97:33:00:01:48'}, {'name': 'Yandex module', 'mac': 'b8:87:6e:48:9b:4a'}]
    polices = [{'name': 'yandex', 'policy': 'Policy0'}, {'name': 'all', 'policy': 'Policy1'}]
    mac = macs[ind_unit]['mac']
    police = polices[ind_vpn]['policy']

    command = f"ip hotspot host {mac}  policy {police}"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command(command)
    data = stdout.read() + stderr.read()
    print(data)
    client.close()
    return str(data, 'utf-8') # data


@app.get('/')
def form_post(request: Request):
    result = 'Type a number'
    return templates.TemplateResponse('item.html', context={'request': request, 'result': result})

@app.post('/')
def form_post(request: Request, action: str = Form(...)):
    match action:
        case 'Зал Youtube':
            result = send_to_keenetic(1, 0)
        case 'Зал Кинопоиск':
            result = send_to_keenetic(1, 1)
        case 'Кухня Youtube':
            result = send_to_keenetic(0, 0)
        case 'Кухня Кинопоиск':
            result = send_to_keenetic(0, 1)
    print(action)
    return templates.TemplateResponse('item.html', context={'request': request, 'result': result})
