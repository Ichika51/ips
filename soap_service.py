from aiohttp import web
import os

async def handle_soap(request):
    soap_request = await request.text()
    response_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:ex="http://example.com/">
        <soapenv:Header/>
        <soapenv:Body>
            <ex:sayHelloResponse>
                <ex:message>Hello, World</ex:message>
            </ex:sayHelloResponse>
        </soapenv:Body>
    </soapenv:Envelope>"""
    return web.Response(text=response_xml, content_type='text/xml')

async def handle_root(request):
    # Проверка наличия параметра ?wsdl
    if 'wsdl' in request.query:
        print('wsdl')  # Печать в консоль для отладки
        wsdl_path = os.path.join(os.path.dirname(__file__), 'service.wsdl')
        try:
            with open(wsdl_path, 'r') as wsdl_file:
                wsdl_content = wsdl_file.read()
            return web.Response(text=wsdl_content, content_type='text/xml')
        except FileNotFoundError:
            return web.Response(text='WSDL file not found', status=404)
    else:
        return web.Response(text='Welcome to the SOAP service!', content_type='text/plain')

app = web.Application()
app.router.add_post('/soap', handle_soap)
app.router.add_get('/', handle_root)

if __name__ == '__main__':
    web.run_app(app, port=8001)
