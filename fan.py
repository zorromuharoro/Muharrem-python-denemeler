import time
from datetime import datetime as dt
class FanAyari:
    def __init__(self):
        self.fan_hizi = 0
        self.fan_calisiyor = False
        self.fan_voltajlari = 0
        self.baslangic_zamani = None
        self.fan_akimlari = 0
        self.watt = 0
        self.fan_hiz_orani = 0
    
    #Fanı aç kapat yaptırdığım yer
    def fan_baslat(self):
        baslatici = input("Fanı başlatmak istiyor musunuz? (e/h): ")
        if self.fan_calisiyor == False:
            if baslatici == "e":
                print("Lütfen biraz bekleyiniz")
                time.sleep(1)
                self.fan_calisiyor = True
                self.baslangic_zamani = dt.now()
                print("Fan başlatıldı")
        elif baslatici == "h":
            print("Lütfen biraz bekleyiniz")
            time.sleep(1)
            self.fan_calisiyor = False
            print("Fan kapatıldı")
            bitis = dt.now()
            gecen_sure = bitis - self.baslangic_zamani
            self.baslangic_zamani = None
            self.fan_hizi = 0
            self.fan_voltajlari = 0
            print(f"Fan Şu süre kadar çalıştı: {gecen_sure.total_seconds()}")
        else:
            print("Fan zaten çalışıyor")

    #Fan hızı belirlediğim yer
    def fan_hizi_ayari(self):
        if self.fan_calisiyor == True:
            hiz = int(input("Fan hızını giriniz (RPM): "))
            if hiz > 0 and hiz <= 6500 :
                self.fan_hizi = hiz
                print(f"Fan hızı: {hiz} RPM")
            else:
                print("Geçersiz hız değeri. Lütfen 1-6500 RPM arasında bir değer girin")
        else:
            print("Önce fanı çalıştırın")
            
    #Fan voltajı yaptırdığım yer
    def fan_voltaj_ayari(self):
        print("Voltaj Ayarları")
        if self.fan_calisiyor == True:
            print("""
                  1- 110V
                  2- 220V
                  3- 380V
                  """)
            secim = input("Voltaj seçiminiz: ")
            if secim == "1":
                onay = input("110V'a geçiş yapılsın mı? (e/h): ")
                if onay == "e":
                    self.fan_voltajlari = 110
                    print(f"Voltaj {self.fan_voltajlari}V olarak ayarlandı")
                else:
                    print("Voltaj değişimi iptal edildi")
            elif secim == "2":
                onay = input("220V'a geçiş yapılsın mı? (e/h): ")
                if onay == "e":
                    self.fan_voltajlari = 220
                    print(f"Voltaj {self.fan_voltajlari}V olarak ayarlandı")
                else:
                    print("Voltaj değişimi iptal edildi")
            elif secim == "3":
                onay = input("380V'a geçiş yapılsın mı? (e/h): ")
                if onay == "e":
                    self.fan_voltajlari = 380
                    print(f"Voltaj {self.fan_voltajlari}V olarak ayarlandı")
                else:
                    print("Voltaj değişimi iptal edildi")
            else:
                print("Geçersiz seçim")
        
        else:
            print("Önce fanı çalıştırın")
            
    #Mod seçim ayarlarımı yaptığım yer
    def mod_sec(self):
        secimler = input("""
                         1 - Ekonomi Mod
                         2 - Normal Mod
                         3 - Turbo Mod
                         
                         Lütfen 3 seçenekten birini seçiniz: 
                         """)
        if secimler == "1":
            print("Ekonomi mod seçildi\n")
            if self.fan_calisiyor == False:
                self.fan_calisiyor = True
            self.fan_voltajlari = 110
            self.fan_hizi = 1100
            print(f"Fan açıldı, Fan hızı: {self.fan_hizi} RPM, Fan Voltajı: {self.fan_voltajlari}V olarak otomatik belirlendi.\n")
        elif secimler == "2":
            print("Normal mod seçildi\n")
            if self.fan_calisiyor == False:
                self.fan_calisiyor = True
            self.fan_hizi = 3000
            self.fan_voltajlari = 220
            print(f"Fan açıldı, Fan hızı: {self.fan_hizi} RPM, Fan Voltajı: {self.fan_voltajlari}V olarak otomatik belirlendi.\n")
        elif secimler == "3":
            print("Turbo mod seçildi")
            if self.fan_calisiyor == False:
                self.fan_calisiyor = True
            self.fan_hizi = 6500
            self.fan_voltajlari = 380
            print(f"Fan açıldı, Fan hızı: {self.fan_hizi} RPM, Fan Voltajı: {self.fan_voltajlari}V olarak otomatik belirlendi.\n")
        else:
            print("Hatalı bir seçimde bulundunuz.")
    
   
            
    #Rapor yazdırdığım yer   
    def rapor_et(self):
        if self.fan_calisiyor != False:
            if self.fan_voltajlari == 110:
                self.fan_akimlari = 5
            elif self.fan_voltajlari == 220:
                self.fan_akimlari = 10
            elif self.fan_voltajlari == 380:
                self.fan_akimlari = 15
        else:
            self.watt = 0
        
        if self.fan_calisiyor != False:
            self.fan_hiz_orani = (self.fan_hizi / 6500) * 100
            if self.fan_hiz_orani >= 10 and self.fan_hiz_orani <= 650:
                print(f"Fan Oranı {self.fan_hiz_orani}")
                
        
        self.watt = self.fan_voltajlari * self.fan_akimlari
        simdiki_zaman = dt.now()
        print(f"""
              Tarih : {simdiki_zaman.year,simdiki_zaman.month,simdiki_zaman.day}               
              Durum: {'Çalışıyor' if self.fan_calisiyor else 'Kapalı'}
              Hız: {self.fan_hizi} RPM
              Voltaj: {self.fan_voltajlari}V
              Watt: {self.watt}W 
              """)
            
def main():
    fan = FanAyari()
    
    print("Fan Kontrol Sistemi")
    print("""
          1 - Fan Aç/Kapat
          2 - Hız Ayarı
          3 - Voltaj Ayarı
          4 - Oto Mod Seç
          5 - Durum Raporu
          6 - Çıkış
          
          """)
    
    while True:
        secim = input("Seçiminiz: ")
        
        if secim == "1":
            fan.fan_baslat()
        elif secim == "2":
            fan.fan_hizi_ayari()
        elif secim == "6":
            print("Program sonlandırıldı")
            break
        elif secim == "3":
             fan.fan_voltaj_ayari()
        elif secim == "5":
            fan.rapor_et()
        elif secim == "4":
            fan.mod_sec()
        else :
            print("Geçersiz seçim")
            
if __name__ == "__main__":
    main()