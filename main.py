import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import time
import datetime

#por algum motivo este primeiro teste deveria ser possivel de execucao apenas com a utilizacao do metodo FIND do soup
# mas nao rolou, por isso importei a biblioteca lxml para poder fazer o parser da página html para teste formato.
#diferente do ultimo exemplo que fiz, este vai usar o request, para baixar as paginas inteirar, e interagir com elas.

URL = "https://www.amazon.com.br/gp/product/B07NZZZ746?pf_rd_r=GXPNKS20BXTQZXRBPVEB&pf_rd_p=72a7651a-a7d8-4551-" \
          "b248-c61480b6ce6e&pd_rd_r=92102280-8547-4981-955e-b6acaa3c0a8a&pd_rd_w=xbF7E&pd_rd_wg=Jh8F6&ref_=pd_gw_unk"

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                        'Version/14.0.3 Safari/605.1.15'}

pagina = requests.get(URL, headers=header)

soup = BeautifulSoup(pagina.content, 'lxml')

def FindByID(ID):
    try:
        return soup.find(id = ID).get_text()
    except:
        print("Erro: id nao encontrado")

def verifica_preco():

    #print(soup.prettify())

    produto = FindByID('productTitle')
    valor = FindByID('priceblock_ourprice')
    valor_convertido = float(valor[2:7])

    #print(produto.strip())
    #print(valor_convertido)

    if (valor_convertido <= 1.085):
        envia_email()
        return 1
    else:
        return 0

    #if(valor_convertido < 1.700)

def envia_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('d.bianchezzi@gmail.com', 'xiczhtzpjuggpatd')
    assunto = "o preco caiu"
    corpo = f"veja o link https://www.amazon.com.br/gp/product/B07NZZZ746?pf_rd_r=GXPNKS20BXTQZXRBPVEB&pf_rd_p=72a7651a-a7d8-4551-" \
          "b248-c61480b6ce6e&pd_rd_r=92102280-8547-4981-955e-b6acaa3c0a8a&pd_rd_w=xbF7E&pd_rd_wg=Jh8F6&ref_=pd_gw_unk"
    mensagem = f"assunto: {assunto}\n\n{corpo}"

    server.sendmail(
        'd.bianchezzi@gmail.com',
        'douglas@sponte.com.br',
        mensagem

    )
    #print("Um email foi enviado!!!")

    server.quit()



while(True):
    if (verifica_preco()) == 1:
        print(f"Um email foi enviado, parece que o preço atendeu as metas estabelecidas. Carimbo de data/hora: {datetime.date.today()}")
        time.sleep(86400)
    elif (verifica_preco()) == 0:
        print(f"Parece que o preço ainda não está dentro da faixa estabelecida. Aguarde nova checagem... Carimbo de data/hora: {datetime.date.today()}")
        time.sleep(86400)
    


#envia_email() #funcional

