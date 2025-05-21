import time
from datetime import datetime as dt

class DimmerDevresi:
    def __init__(self):
        self.sebeke_voltaj_ac = False
        self.lamba_ac = False
        self.sebeke_voltaj = 0
        self.lamba_voltajlari = 0
        self.lamba_parlakligi = 0
        self.baslangic_zamani = None
        self.calisma_suresi = 0
        self.cekilen_akim = 0
        self.guc_tuketimi = 0
        self.enerji_tuketimi = 0
        self.birim_fiyat = 1.5
        self.harcanan_maliyet = 0
        self.konturlu_kullanim = 0
        
    def bekle(self,sure):
        print("Lütfen Biraz Bekleyiniz\n")
        time.sleep(sure)
        
    def kontrol_yeterli_mi(self, gereken_miktar):
        return self.konturlu_kullanim >= gereken_miktar
        
    def sebeke_ac(self):
        try:
            if self.sebeke_voltaj_ac:
                secim = input("Şebekeyi kapatmak ister misiniz? (E/H): \n")
                if secim.lower() == "e":
                    self.bekle(1)
                    self.sebeke_voltaj_ac = False
                    self.sebeke_voltaj = 0
                    print("Şebeke kapatıldı!\n")
                elif secim.lower() == "h":
                    print("Şebeke açık kalmaya devam edecek!\n")
                else:
                    print("Hatalı işlem yaptınız!\n")
            else:
                secim = input("Şebekeyi açmak ister misiniz? (E/H): \n")
                if secim.lower() == "e":
                    self.bekle(1)
                    self.sebeke_voltaj_ac = True
                    print("Şebeke açıldı!\n")
                elif secim.lower() == "h":
                    print("Şebeke kapalı kalmaya devam edecek!\n")
                else:
                    print("Hatalı işlem yaptınız!\n")
        except ValueError:
            print("Hatalı işlem yaptınız! Lütfen E veya H harflerinden birini giriniz.\n")
            
    def lamba_acma(self):
        try:
            if not self.sebeke_voltaj_ac:
                print("Lütfen öncelikle şebeke voltajını devreye alın!\n")
                return
                
            secim = input("Lambayı açmak istermisiniz? (E/H): \n")
            if secim.lower() == "e":
                self.bekle(1)
                self.lamba_ac = True
                self.baslangic_zamani = dt.now()
                print("Lamba açıldı!\n")
            elif secim.lower() == "h":
                self.bekle(1)
                self.lamba_ac = False
                self.lamba_voltajlari = 0
                if self.baslangic_zamani:
                    bitis_sure = dt.now()
                    gecen_sure = bitis_sure - self.baslangic_zamani
                    self.calisma_suresi = gecen_sure.total_seconds()
                    self.hesapla_enerji_tuketimi()
                    print("Lamba Kapatıldı!\n")
                    print(f"Lamba {self.calisma_suresi} süre çalıştı. ")
                    self.baslangic_zamani = None
                    self.cekilen_akim = 0
                    self.guc_tuketimi = 0
                    self.enerji_tuketimi = 0
            else:
                print("Hatalı işlem yaptınız!\n")
        except ValueError:
            print("Hatalı işlem yaptınız! Lütfen E veya H harflerinden birini giriniz.\n")
            
    def sebeke_voltaji_secimi(self):
        try:
            if not self.sebeke_voltaj_ac:
                print("Önce şebekeyi açmanız gerekiyor!\n")
                return
                
            secim = int(input("Lütfen kullanmak istediğiniz şebeke voltajını seçiniz (110/220/380)V: \n"))
            if secim in [110, 220, 380]:
                self.sebeke_voltaj = secim
                print(f"Şebeke voltajı {self.sebeke_voltaj}V olarak seçildi.\n")
                if self.lamba_voltajlari and self.lamba_voltajlari != secim:
                    print("UYARI: Lamba voltajı şebeke voltajından farklı!\n")
            else:
                print("Hatalı seçim yaptınız!")
        except ValueError:
            print("Hatalı işlem yaptınız! Lütfen sayısal değerler giriniz.\n")
    
    def lamba_voltaji_sec(self):
        try:
            if not self.lamba_ac:
                print("Önce lambayı açmanız gerekiyor!\n")
                return
                
            secim = int(input("Lütfen lamba voltajınızı giriniz (110/220/380)V: \n"))
            if secim in [110, 220, 380]:
                self.lamba_voltajlari = secim
                print(f"Seçtiğiniz lamba voltajı {self.lamba_voltajlari}V\n")
                if self.sebeke_voltaj and self.sebeke_voltaj != secim:
                    print("UYARI: Lamba voltajı şebeke voltajından farklı!\n")
            else:
                print("Hatalı işlem yaptınız!\n")
        except ValueError:
            print("Hatalı işlem yaptınız! Lütfen sayısal değerler giriniz.\n")
            
    def lamba_parlaklik(self):
        try:
            if not self.lamba_ac:
                print("Önce lambayı açmanız gerekiyor!\n")
                return
                
            secim = int(input("0'ila 100 arasında bir parlaklık belirleyiniz: \n"))
            if 0 <= secim <= 100:
                self.lamba_parlakligi = secim
                self.cekilen_akim = (16 * self.lamba_parlakligi) / 100
                print(f"Seçilen parlaklık seviyesi: %{self.lamba_parlakligi}\n")
            else:
                print("Parlaklık 0-100 arasında olmalıdır!\n")
        except ValueError:
            print("Hatalı işlem yaptınız! Lütfen sayısal değerler giriniz.\n")

    def hesapla_enerji_tuketimi(self):
        self.guc_tuketimi = self.lamba_voltajlari * self.cekilen_akim
        sure_saat = self.calisma_suresi / 3600
        kw = self.guc_tuketimi / 1000
        self.enerji_tuketimi = kw * sure_saat
        self.harcanan_maliyet = self.enerji_tuketimi * self.birim_fiyat

    def oto_microlar(self):
        print("""
            1 - 110V şebeke voltajı, 110V lamba voltajı, %20 Parlaklık
            2 - 220V şebeke voltajı, 220V lamba voltajı, %50 Parlaklık
            3 - 380V şebeke voltajı, 380V lamba voltajı, %100 Parlaklık
            \n""")
        try:
            secim = input("Lütfen yukardan bir otomatik ayar seçiniz: \n")
            
            kontur_degeri = {"1": 50, "2": 100, "3": 200}.get(secim)
            if not kontur_degeri:
                print("Hatalı seçim!")
                return
                
            if not self.kontrol_yeterli_mi(kontur_degeri):
                print(f"Yetersiz kontör! Gereken: {kontur_degeri}, Mevcut: {self.konturlu_kullanim}")
                return

            self.sebeke_voltaj_ac = True
            self.lamba_ac = True
            self.baslangic_zamani = dt.now()

            if secim == "1":
                self.sebeke_voltaj = 110
                self.lamba_voltajlari = 110
                self.lamba_parlakligi = 20
            elif secim == "2":
                self.sebeke_voltaj = 220
                self.lamba_voltajlari = 220
                self.lamba_parlakligi = 50
            elif secim == "3":
                self.sebeke_voltaj = 380
                self.lamba_voltajlari = 380
                self.lamba_parlakligi = 100
                
            self.cekilen_akim = (16 * self.lamba_parlakligi) / 100
            self.konturlu_kullanim -= kontur_degeri
            self.harcanan_maliyet += kontur_degeri
            
            print(f"Seçilen şebeke voltajı {self.sebeke_voltaj}V, seçilen lamba voltajı {self.lamba_voltajlari}V, Seçilen Lamba parlaklığı %{self.lamba_parlakligi}. Olarak belirlendi ve sistem çalışmakta. Kullanilan Kontür : {kontur_degeri}\n")

        except ValueError:
            print("Hatalı işlem yaptınız!\n")
            
    def kontur_yukle(self):
        try:
            print("Dimmeri kullanabilmek için kontür yüklemesi yapmanız gerekli...")
            yukle = int(input("Lütfen yüklemek istediğiniz kontür miktarını seçiniz : "))
            
            if 0 < yukle <= 10000:
                self.konturlu_kullanim = yukle
                print(f"Başarılı bir şekilde {self.konturlu_kullanim} kontür yüklenmiştir..")
            else:
                print("Kontör miktarı 0-10000 arasında olmalıdır...")
        except ValueError:
            print("Lütfen sayısal değer giriniz...")
            
    def durum_raporu(self):
        if self.lamba_ac and self.baslangic_zamani:
            simdiki_zaman = dt.now()
            self.calisma_suresi = (simdiki_zaman - self.baslangic_zamani).total_seconds()
            self.hesapla_enerji_tuketimi()
            
        print("-----Dimmer Devresi Rapor-----")
        print(f"Şebeke voltajı durumu : {self.sebeke_voltaj_ac}")
        print(f"Şebeke voltajı : {self.sebeke_voltaj}V")
        print(f"Lamba durumu : {self.lamba_ac}")
        print(f"Lamba voltajı : {self.lamba_voltajlari}V")
        print(f"Lamba parlaklığı : %{self.lamba_parlakligi}")
        print(f"Lamba çalışma süresi : {self.calisma_suresi} saniye")
        print(f"Lambanın Çektiği akım : {self.cekilen_akim}A")
        print(f"Çekilen Güç : {self.guc_tuketimi:.2f}W")
        print(f"Harcanan tutar : {self.harcanan_maliyet:.2f}TL")
        print(f"Kalan Kontör : {self.konturlu_kullanim}")

def main():
    dimmer = DimmerDevresi()
    
    print("...Dimmer Devresine hoşgeldiniz...\n")
    print("""
          1 - Şebeke voltajını aç/kapat
          2 - şebeke voltajını seç
          3 - Lamba'yı aç/kapat
          4 - Lamba voltajını seç
          5 - Lamba parlaklığını seç
          6 - Otomatik seçenekler 
          7 - Durum raporu
          8 - kontür yükleme
          9 - Çıkış
          \n""")
    
    if dimmer.konturlu_kullanim <= 0:
        print("Kullanım için önce kontör yüklemelisiniz!")
        dimmer.kontur_yukle()
    
    while True:
        secim = input("Lütfen bir seçenek seçiniz!: \n")
        
        if secim == "1":
            dimmer.sebeke_ac()
        elif secim == "2":
            dimmer.sebeke_voltaji_secimi()
        elif secim == "3":
            dimmer.lamba_acma()
        elif secim == "4":
            dimmer.lamba_voltaji_sec()
        elif secim == "5":
            dimmer.lamba_parlaklik()
        elif secim == "6":
            dimmer.oto_microlar()
        elif secim == "7":
            dimmer.durum_raporu()
        elif secim == "8":
            dimmer.kontur_yukle()
        elif secim == "9":
            print("Program Sonlandırılıyor...\n")
            dimmer.sebeke_voltaj = 0
            dimmer.lamba_voltajlari = 0
            dimmer.lamba_parlakligi = 0
            dimmer.konturlu_kullanim = 0
            break
        else:
            print("Yanlış seçim yaptınız!\n")

if __name__ == "__main__":
    main()