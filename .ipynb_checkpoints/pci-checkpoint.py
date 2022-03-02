def main():

    from urllib.request import urlopen
    from urllib.error import HTTPError
    from bs4 import BeautifulSoup

    html = urlopen('https://www.pciconcursos.com.br/professores')
    bs = BeautifulSoup(html, 'html.parser')

    vagas_tag = bs.html.body.findAll('a', rel='bookmark')
    estados_tag = bs.html.body.findAll('div', class_='cc')
    datas_insc_tag = bs.html.body.findAll('div', class_='ce')

    links = []
    orgs = []
    datas = []
    estados = []
    matriz = []

    for vaga in vagas_tag:

        if vaga.get_text() != '':
            orgs.append(vaga.get_text())

        else:
            orgs.append('x')

    for vaga in vagas_tag:

        if 'noticia' in str(vaga).split('"')[1]:
            links.append(str(vaga).split('"')[1])

        else:
            links.append('x')

    for estado in estados_tag:

        if estado != '':
            estados.append(estado.get_text())

        else:
            estados.append('x')

    for data in datas_insc_tag:

        if data != '':
            datas.append(data.get_text())

        else:
            datas.append('x')

    estados = [el.replace('\xa0', 'NC') for el in estados]

    while orgs.count('x') != 0:
        orgs.remove('x')

    for i in range(0, len(estados_tag)):
        matriz.append([estados[i], orgs[i], links[i], datas[i]])

    with open(r'C:\Users\lucas\projetos\estudo python\data.txt', 'w') as arquivo:

        for linha in matriz:
            for i in range(0, len(linha)):
                if i != len(linha)-1:
                    arquivo.write(f'{linha[i]}; ')

                else:
                    arquivo.write(f'{linha[i]}')

            arquivo.write(f'\n')

    print('Conclúído!')

main()
