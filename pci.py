from bs4 import BeautifulSoup
from urllib.request import urlopen
import re



class Scrappy:

    def __init__(self):

        self.html = urlopen('https://www.pciconcursos.com.br/professores/')
        self.bs = BeautifulSoup(self.html, 'html.parser')

        print('\nRastreando as regioões ...' , end = '')
        
        self.regioes = self.pegar_regioes()

        print('\t(Concluído!)')

        print('Rastreando as datas ...' , end = '')

        self.datas = self.pegar_datas()

        print('\t(Concluído!)')

        print('Rastreando os links ...' , end = '')

        self.links = self.pegar_links()

        print('\t(Concluído!)')

        print('Rastreando os órgãos ...' , end = '')

        self.orgaos = self.pegar_orgaos()

        print('\t(Concluído!)')

        print('Rastreando os títulos ...' , end = '')

        self.titulos = self.pegar_titulos()

        print('\t(Concluído!)')

        self.regioes_de_interesse = ['SP', 
                                     'RJ', 
                                     'NC', 
                                     'MG', 
                                     'ES']

        with open('concdata.txt', 'w') as f:

            total_de_vagas = len(self.regioes)

            for i in range(total_de_vagas):

                if self.regioes[i] in self.regioes_de_interesse:

                    regiao = self.regioes[i]

                    data = self.datas[i]

                    orgao = self.orgaos[i]

                    titulo = self.titulos[i]

                    link = self.links[i]

                    edital = self.pegar_edital(self.links[i])

                    linha = f'{regiao}; {data}; {orgao}; {titulo}; {link}; {edital}\n'

                    print(f'Registrando linha: {linha}\t( {i + 1} / {total_de_vagas} )', end = '')

                    f.write(linha)

                    print('\t(Concluído!)')

                else:

                    continue

    
    def pegar_regioes(self):

        bs_obj = self.bs

        regioes = []

        for reg in bs_obj.html.body.findAll('div', class_='cc'):
            regioes.append(reg.get_text())

        regioes = [el.replace('\xa0', 'NC') for el in regioes]
        
        return regioes


    def pegar_datas(self):

        bs_obj = self.bs
        
        datas = []

        for item in bs_obj.html.body.findAll('div', class_='ce'):
            if re.search(r'\d{2}/\d{2}/\d{4}', item.get_text()) is not None:
                datas.append(re.search(r'\d{2}/\d{2}/\d{4}', item.get_text()).group())
            else:
                datas.append('Verificar no PCI')

        return datas


    def pegar_links(self):

        bs_obj = self.bs
        
        links = []
        
        for link in bs_obj.html.body.findAll('a',
                                             attrs={'href': re.compile("^https?://www.pciconcursos.com.br/noticias"),
                                                    'rel': 'bookmark'}):
            links.append(str(link).split('"')[1])
            
        return links


    def pegar_orgaos(self):

        bs_obj = self.bs
        
        orgaos = []
        
        for org in bs_obj.html.body.findAll('a',
                                            attrs={'href': re.compile("^https?://www.pciconcursos.com.br/noticias"),
                                                   'rel': 'bookmark'}):
            orgaos.append(org.get_text())
            
        return orgaos


    def pegar_titulos(self):

        bs_obj = self.bs
        
        titulos = []
        
        for titulo in bs_obj.html.body.findAll('a',
                                               attrs={'href': re.compile("^https?://www.pciconcursos.com.br/noticias"),
                                                      'rel': 'bookmark'}):
            titulos.append(titulo['title'])
            
        return titulos

    
    def pegar_edital(self, link):

        page = urlopen(link)
        bsaux = BeautifulSoup(page, 'html.parser')

        compilaçao = re.compile(r'\.pdf$')

        edital = bsaux.html.body.findAll('a', attrs={'href': compilaçao, 'rel': 'nofollow'})

        if len(edital) == 0:
            return 'Edital não encontrado.'
        elif len(edital) == 1:
            return edital[0]['href']
        elif len(edital) > 1:
            return 'Mais de um edital encontrado.'


pci = Scrappy()