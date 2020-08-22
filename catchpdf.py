import requests
import getpass
import os, sys, platform
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class FindPdf:
    def __init__(self):
        self.target = input("\u001b[32m Hedefi Giriniz (Örnek-> www.google.com): ")
        self.osName = platform.system()
        self.currentUserName = getpass.getuser()

    def MakeRequest(self):
        try:
            self.replaceHttps = "https://" + self.target
            self.req = requests.get(self.replaceHttps, allow_redirects=True)
            self.soup = BeautifulSoup(self.req.text, "html.parser")
            
            if self.req.status_code == 200:
                self.ScrapingPDF()

            else:
                print("\u001b[31m Sayfa Yanıt Vermiyor !")
                sys.exit()

        except HTTPError as http_err:
            print(http_err)
            sys.exit()

        except Exception as err:
            print(err)
            sys.exit()

    def ScrapingPDF(self):
        self.numberOfPdf = 0

        for link in self.soup.select("a[href$='.pdf']"):
            self.numberOfPdf += 1
            self.folderLocation = os.getcwd()
            
            if not os.path.exists(self.folderLocation +"/AllPDF"):os.mkdir(self.folderLocation+"/AllPDF") # pdfleri kaydedeceğinmiz dosya yoksa dosyayı oluşturur
            #pdf dosyalarını adlandırıyoruz
            self.filename = os.path.join(self.folderLocation+"/AllPDF",link['href'].split('/')[-1])

            with open(self.filename, 'wb') as f:
                f.write(requests.get(urljoin(self.replaceHttps,link['href'])).content)
                print("\u001b[34m PDF Dosyaları Şuraya Kaydedildi -> \u001b[32m" + self.folderLocation + "/AllPDF")

        if self.numberOfPdf == 0:
            print("\u001b[31m Her hangi bir PDF bulunamadı !")



a = FindPdf()
a.MakeRequest()
