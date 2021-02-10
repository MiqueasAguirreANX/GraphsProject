# This is a sample Python script.

import requests as r

token = '534466e905f901ad45b642db7ddd4f6080e925d1'

CANT_DEVS_PRO = {
    'omgnetwork': [],
    'maticnetwork': [],
    'cryptoeconomicslab': [], # obtuve error 0 1 /gazelle
    'perun-network': [],
    'raiden-network': [], # obtuve error 20
    'connext': [],
    'AztecProtocol': [],
    'matter-labs': [], # obtuve error 0 1 /zksync
    'LoopringSecondary': [], # obtuve error 0 1 /protocol
    'starkware-libs': [], # obtuve error 0 1
    'fuellabs': [],
    'ethereum-optimism': [], # obtuve error 29
    'OffchainLabs': [], # obtuve error 0 1 /arbitrum
    'celer-network': [],
    'skalenetwork': [],
}


def main():
    cont1 = 0
    for k in CANT_DEVS_PRO.keys():
        url = f'https://api.github.com/orgs/{k}/repos'
        lista_proyectos = r.get(url, params={'access_token': token}).json()
        cont2 = 0
        if cont1 == 2:
            _url = f'https://api.github.com/repos/{k}/contributors'
            collaborators = r.get(_url, params={'type': 'public', 'access_token': token}).json()
            CANT_DEVS_PRO[k].append(len(collaborators))
            cont1 += 1
            continue

        if cont1 == 7:
            _url = f'https://api.github.com/repos/{k}/zksync/contributors'
            collaborators = r.get(_url, params={'type': 'public', 'access_token': token}).json()
            CANT_DEVS_PRO[k].append(len(collaborators))
            cont1 += 1
            continue

        if cont1 == 8:
            _url = f'https://api.github.com/repos/{k}/protocol/contributors'
            collaborators = r.get(_url, params={'type': 'public', 'access_token': token}).json()
            CANT_DEVS_PRO[k].append(len(collaborators))
            cont1 += 1
            continue

        if cont1 == 12:
            _url = f'https://api.github.com/repos/{k}/arbitrum/contributors'
            collaborators = r.get(_url, params={'type': 'public', 'access_token': token}).json()
            CANT_DEVS_PRO[k].append(len(collaborators))
            cont1 += 1
            continue

        for item in lista_proyectos:
            try:
                print(item['contributors_url'])
                url2 = item['contributors_url']
                collaborators = r.get(url2, params={'type': 'public', 'access_token': token}).json()
                CANT_DEVS_PRO[k].append(len(collaborators))
            except Exception as e:
                print(f'Ocurred an error at index ({cont1},{cont2})')
                print(f'Mensaje: {e}')
                CANT_DEVS_PRO[k].append(0)
            finally:
                cont2 += 1

        cont1 += 1

    print('Trabajo terminado: contribuidores de todos los proyectos de todos los repositorios')
    print(CANT_DEVS_PRO)
    # with open('contributors.csv', 'w') as f:
    #     for k in CANT_DEVS_PRO.keys():
    #         print(f'{k}: repositorios({len(CANT_DEVS_PRO[k])})/ contribuidores({sum(CANT_DEVS_PRO[k])})')
    #         for ind, elem in enumerate(CANT_DEVS_PRO[k]):
    #             f.write(f'{k},{ind},{elem}\n')


if __name__ == "__main__":
    main()
