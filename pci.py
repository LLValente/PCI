from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


def main():

    html = urlopen('https://www.pciconcursos.com.br/professores/')
    bs = BeautifulSoup(html, 'html.parser')

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

    def edital(link):

        page = urlopen(link)
        bsaux = BeautifulSoup(page, 'html.parser')
        ed = bsaux.html.body.findAll('a', attrs={'href': re.compile('.pdf$'), 'rel': 'nofollow'})

        if len(ed) == 0:
            return 'Edital não encontrado'
        elif len(ed) == 1:
            return ed[0]['href']
        elif len(ed) > 1:
            return 'Mais de um edital encontrado'

    REGS_INTERESSE = ['SP', 'RJ', 'NC', 'MG', 'ES']

    regs = pegar_regioes(bs)
    dats = pegar_datas(bs)
    orgs = pegar_orgaos(bs)
    tits = pegar_titulos(bs)
    liks = pegar_links(bs)
        
    with open('concdata.txt', 'w') as f:
        for n in range(len(regs)):
            if regs[n] in REGS_INTERESSE:
                print(f'{regs[n]};{dats[n]};{orgs[n]};{tits[n]};{liks[n]};{edital(liks[n])}')
                f.write(f'{regs[n]};{dats[n]};{orgs[n]};{tits[n]};{liks[n]};{edital(liks[n])}\n')
            else:
                continue


main()
