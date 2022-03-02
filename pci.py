from bs4 import BeautifulSoup
from urllib.request import urlopen
import re



def Scrappy():

    def __init__(self):

        self.html = urlopen('https://www.pciconcursos.com.br/professores/')
        self.bs = BeautifulSoup(self.html, 'html.parser')
        
        self.regioes = self.pegar_regioes(self.bs)
        self.datas = self.pegar_datas(self.bs)
        self.links = self.pegar_links(self.bs)
        self.orgaos = self.pegar_orgaos(self.bs)
        self.titulos = self.pegar_titulos(self.bs)

        self.regioes_de_interesse = ['SP', 
                                     'RJ', 
                                     'NC', 
                                     'MG', 
                                     'ES']

        with open('concdata.txt', 'w') as f:
            for n in range(len(self.regioes)):
                if self.regioes[n] in self.regioes_INTERESSE:
                    print(f'{self.regioes[n]};{self.datas[n]};{self.orgaos[n]};{self.titulos[n]};{self.links[n]};{self.pegar_edital(self.links[n])}')
                    f.write(f'{self.regioes[n]};{self.datas[n]};{self.orgaos[n]};{self.titulos[n]};{self.links[n]};{self.pegar_edital(self.links[n])}\n')
                else:
                    continue

    
    def pegar_regioes(bs_obj):

        regioes = []

        for reg in bs_obj.html.body.findAll('div', class_='cc'):
            regioes.append(reg.get_text())

        regioes = [el.replace('\xa0', 'NC') for el in regioes]
        
        return regioes


    def pegar_datas(bs_obj):
        
        datas = []

        for item in bs_obj.html.body.findAll('div', class_='ce'):
            if re.search(r'\d{2}/\d{2}/\d{4}', item.get_text()) is not None:
                datas.append(re.search(r'\d{2}/\d{2}/\d{4}', item.get_text()).group())
            else:
                datas.append('Verificar no PCI')

        return datas


    def pegar_links(bs_obj):
        
        links = []
        
        for link in bs_obj.html.body.findAll('a',
                                             attrs={'href': re.compile("^https?://www.pciconcursos.com.br/noticias"),
                                                    'rel': 'bookmark'}):
            links.append(str(link).split('"')[1])
            
        return links


    def pegar_orgaos(bs_obj):
        
        orgaos = []
        
        for org in bs_obj.html.body.findAll('a',
                                            attrs={'href': re.compile("^https?://www.pciconcursos.com.br/noticias"),
                                                   'rel': 'bookmark'}):
            orgaos.append(org.get_text())
            
        return orgaos


    def pegar_titulos(bs_obj):
        
        titulos = []
        
        for titulo in bs_obj.html.body.findAll('a',
                                               attrs={'href': re.compile("^https?://www.pciconcursos.com.br/noticias"),
                                                      'rel': 'bookmark'}):
            titulos.append(titulo['title'])
            
        return titulos

    
    def pegar_edital(link):

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

