import json


def toClash(vmesses):
    yamltext = 'Proxy:\n'
    names = []
    for vmess in vmesses:
        if vmess['net'] != 'h2':
            obj = {
                'name': vmess['ps'],
                'type': 'vmess',
                'server': vmess['add'],
                'port': vmess['port'],
                'uuid': vmess['id'],
                'alterId': vmess['aid'],
                'cipher': 'auto',
                'udp': True
            }
            names.append(vmess['ps'])
            if vmess['net'] == 'ws':
                obj.update({
                    'network': 'ws',
                    'ws-path': vmess['path'],
                    'tls': True,
                    'ws-headers': {
                        'Host': vmess['host']
                    }
                })
            yamltext += '  - {}\n'.format(json.dumps(obj, ensure_ascii=False))
    yamltext += "\n\nProxy Group:\n"
    yamltext += "- name: Proxy\n"
    yamltext += "  type: select\n"
    yamltext += "  proxies:\n"
    yamltext += ''.join(["    - '{}'\n".format(n) for n in names])
    yamltext += open('template-clash.yaml', 'r').read()
    return yamltext
