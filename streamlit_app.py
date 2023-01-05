import streamlit as st
from bs4 import BeautifulSoup
import requests
import random

# listeler
ipler = ["IP40", "IP55", "IP65", "IP66", "IP67", "IP68"]
acikalanlar = ["otopark", "şantiye", "park", "meydan", "stadyum"]
belgeler = ["CE", "EAC", "LED"]
darbeler = ["IK00", "IK01", "IK02", "IK03", "IK04", "IK05", "IK06", "IK07", "IK08", "IK09", "IK10", "IK11"]
markalar = ["Pelsan", "pelsan"]


# Fonksiyonlar

def title_features(title):
    kelimeler = title.split(" ")
    ipler = ["IP40", "IP55", "IP65", "IP66", "IP67", "IP68"]
    sozluk = {}
    for kelime in kelimeler:
        if kelime[-1] == "W" and kelime[:-1].isnumeric():
            sozluk['güç'] = kelime
        if kelime[-1] == "K" and kelime[:-1].isnumeric():
            sozluk['sıcaklık'] = kelime
        if kelime in ipler:
            sozluk['ip'] = kelime

    for marka in markalar:
        if marka in kelimeler:
            sozluk['marka'] = marka

    return sozluk


def aciklama_features(text):
    text = text.replace("✔️", "")
    text = text.replace("\xa0", " ")
    text = text.replace(".", "")
    textliste = text.split(" ")
    acikalanlar = ["otopark", "şantiye", "park", "meydan", "stadyum"]
    random.shuffle(acikalanlar)
    sozluk = {}
    if "2 Yıl" in text or "2 yıl" in text:
        sozluk["garanti"] = "2 yıl"
    for a in acikalanlar:
        if a in text:
            sozluk["açıkalan"] = "uygun"
    for t in textliste:
        if len(t) > 0:
            if t[-1] == "h" and t[:-1].isnumeric():
                sozluk['çalışma süresi'] = t[:-1]

    for i in range(len(textliste)):
        if textliste[i] == "Lümen" and textliste[i - 1].isnumeric():
            sozluk["ışık akısı"] = textliste[i - 1]

    for b in textliste:
        belgeler = ["CE", "EAC", "LED"]
        for belge in belgeler:
            if belge in b:
                sozluk['belge'] = b.split(",")
    for d in darbeler:
        if d in text:
            sozluk['darbe dayanıklılığı'] = d

    if "Alüminyum Gövde" in text:
        sozluk["gövde"] = "aluminyum gövde"

    return sozluk


def kategori_features(kategori):
    sozluk = {}
    sozluk['kategori'] = kategori
    return sozluk


def all_features(*sozlukler):
    sozluk = {}
    for s in sozlukler:
        sozluk.update(s)
    return sozluk


def text_generator(sozluk):
    yazilar = []
    # marka
    if sozluk.get("marka") == "Pelsan":
        liste = markayazi['pelsan']
        marka_cumle = random.choice(liste)
        yazilar.append(marka_cumle[0])
    # garanti
    if sozluk.get("garanti") == "2 yıl":
        liste = altyazi['2 Yıl']
        garanti_cumle = random.choice(liste)
        yazilar.append(garanti_cumle)
    # çalışma süresi
    sure = sozluk.get("çalışma süresi")
    if type(sure) == "str":
        if sure.isnumeric():
            liste = detayyazi["Çalışma Ömrü"]
            sure_cumle = random.choice(liste)
            sure_cumle = sure_cumle.replace("#kodcs", sure)
            yazilar.append(sure_cumle)

    # açık alan

    if sozluk.get("açıkalan") == "uygun":
        liste = detayyazi["Açık Alan"]
        alan_cumle = random.choice(liste)
        alan_cumle = alan_cumle.replace("#açıkalan", ",".join(acikalanlar))
        alan_cumle = alan_cumle.replace("bu ürün", random.choice(['bu ürün', urun_baslik, bukategori]))
        alan_cumle = alan_cumle.replace("Bu ürün", random.choice(['Bu ürün', urun_baslik, Bukategori]))
        yazilar.append(alan_cumle)

    # ışık akısı

    if type(sozluk.get("ışık akısı")) == "str":
        if sozluk.get("ışık askısı").isnumeric():
            liste = detayyazi["Işık Akısı"]
            aki_cumle = random.choice(liste)
            aki_cumle = aki_cumle.replace("bu ürün", random.choice(['bu ürün', urun_baslik, bukategori]))
            aki_cumle = aki_cumle.replace("Bu ürün", random.choice(['Bu ürün', urun_baslik, Bukategori]))
            aki_cumle = aki_cumle.replace("#ışıkakısı", sozluk.get("ışık akısı"))
            yazilar.append(aki_cumle)

    ### belge

    if type(sozluk.get('belge')) == list:
        uisimler = ",".join(sozluk.get("belge"))
        liste = detayyazi['Belge']
        belge_cumle = random.choice(liste)
        belge_cumle = belge_cumle.replace("bu ürün", random.choice(['bu ürün', urun_baslik, bukategori]))
        belge_cumle = belge_cumle.replace("Bu ürün", random.choice(['Bu ürün', urun_baslik, Bukategori]))
        belge_cumle = belge_cumle.replace("#belge", ",".join(sozluk.get("belge")))
        yazilar.append(belge_cumle)

    ## ip

    if sozluk.get('ip') == "IP65":
        liste = detayyazi["IP65"]
        ip_cumle = random.choice(liste)

        ip_cumle = ip_cumle.replace("bu ürün", random.choice(['bu ürün', urun_baslik, bukategori]))
        ip_cumle = ip_cumle.replace("Bu ürün", random.choice(['Bu ürün', urun_baslik, Bukategori]))
        yazilar.append(ip_cumle)

    ### Alüminyum

    if sozluk.get('gövde') == "aluminyum gövde":
        liste = detayyazi["Alüminyum"]
        al_cumle = random.choice(liste)

        al_cumle = al_cumle.replace("bu ürün", random.choice(['bu ürün', urun_baslik, bukategori]))
        al_cumle = al_cumle.replace("Bu ürün", random.choice(['Bu ürün', urun_baslik, Bukategori]))
        yazilar.append(al_cumle)

    ### Güç

    if type(sozluk.get('güç')) == str:
        if sozluk.get('güç')[-1] == "W":
            liste = detayyazi["Güç"]
            guc_cumle = random.choice(liste)
            guc_cumle = guc_cumle.replace("#güç", sozluk.get('güç'))
            guc_cumle = guc_cumle.replace("bu ürün", random.choice(['bu ürün', urun_baslik, bukategori]))
            guc_cumle = guc_cumle.replace("Bu ürün", random.choice(['Bu ürün', urun_baslik, Bukategori]))
            yazilar.append(guc_cumle)

    ## renk sıcaklığı

    if type(sozluk.get('sıcaklık')) == str:
        if sozluk.get('sıcaklık')[-1] == "K":
            liste = detayyazi["Renk Sıcaklığı"]
            sica_cumle = random.choice(liste)
            sica_cumle = sica_cumle.replace("#kodrenk", sozluk.get('sıcaklık'))
            sica_cumle = sica_cumle.replace("bu ürün", random.choice(['bu ürün', urun_baslik, bukategori]))
            sica_cumle = sica_cumle.replace("Bu ürün", random.choice(['Bu ürün', urun_baslik, Bukategori]))
            yazilar.append(sica_cumle)

    return yazilar


def kategoriayar(kat):
    kat = kat.lower()
    kat = kat.replace("leri", "")
    kat = kat.replace("ları", "")
    # oyun oyunu kalem kalemi armatürü kelimesi alanı
    ılar = ["a", "ı"]
    iler = ["e", "i"]
    üler = ["ü"]
    ular = ["u"]
    if kat[-1] in ılar:
        ek = "sı"
    elif kat[-1] in iler:
        ek = "si"
    elif kat[-1] in üler:
        ek = "sü"
    elif kat[-1] in ular:
        ek = "su"
    elif kat[-2] in ılar:
        ek = "ı"
    elif kat[-2] in iler:
        ek = "i"
    elif kat[-2] in üler:
        ek = "ü"
    elif kat[-2] in ular:
        ek = "u"
    elif kat[-3] in ılar:
        ek = "ı"
    elif kat[-3] in iler:
        ek = "i"
    elif kat[-3] in üler:
        ek = "ü"
    elif kat[-3] in ular:
        ek = "u"
    else:
        ek = ""

    kat = kat + ek

    return kat


### Bağlantı

robot = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
adres =st.text_input("Ürün Linki Şu An sadece Pelsan ve armatür veya projektör")
buton=st.button("Oluştur")
if buton:
    site = requests.get(adres, headers=robot)
    icerik = site.content
    soup = BeautifulSoup(icerik, "html.parser")

    # İçerikler

    # Başlık
    urun_baslik = soup.find("h1").text

    # Açıklama
    aciklama = soup.find("div", {"id": "product-features"})
    aciklama = aciklama.find_all("p")
    aciklamalar = []
    for a in aciklama:
        aciklamalar.append(a.text)
    aciklamatext = " -- ".join(aciklamalar)

    # kategori
    kategori = soup.find("a", {"id": "more-category"}).text
    bukategori = "bu " + kategoriayar(kategori)
    Bukategori = "Bu " + kategoriayar(kategori)

    ############ Train Yazılar

    ### MARKA

    markayazi = {
        "pelsan": [
            [
                "Bu ürün Türkiye'nin en bilinen aydınlatma ürünleri üreticilerinden biri olan Pelsan tarafından üretilmiştir."],
            [
                "Uluslararası standartlara uygun şekilde Pelsan tarafından üretilen bu ürün kendini zorlu şartlarda kanıtlamıştır"],
            ["Pelsan tarafından üretilen bu ürün akredite laboratuvarda test edilmiştir."],
            [
                "Tüm ihtiyaçlar göz önüne alınarak Pelsan tarafından tasarlanan ve üretilen bu ürün uluslararası standartlara göre piyasaya sürülmüştür"],
            ["Bu ürün Türkiye'nin en gelişmiş full entegre fabrikalarından biri olan Pelsan fabrikasında üretilmiştir."]

        ]
    }

    #### DETAY

    detayyazi = {

        "Güç": [
            "Hem çevre dostu hem de kaliteli aydınlatma sağlayan bu ürün #güç gücünde enerji tüketimine sahiptir. Diğer modeller için kategorimizi inceleyebilirsiniz",
            "#güç güç değerine sahip olan bu ürün kaliteli ve verimli bir aydınlatma sağlamaktadır.",
            "En çok tercih edilen modellerden biri olan ve yeni nesil teknoloji ile üretilen bu ürün #güç değerinde enerji tüketimine sahiptir."
        ],

        "IP65": [
            "IP65 sınıflandırma kodu ile üretilen bu ürün sıvı ve katı malzemelere karşı koruma sağlamaktadır. Ayrıca toza karşı da güvenlik sağlamaktadır",
            "Bu ürün toz başta olmak üzere katı ve sıvı bir çok dış etkiye karşı koruma sınıfı olan IP65 ile üretilmiştir."
            "Ürünümüz Uluslararası bir sınıflandırma olan IP65 koduyla sıvı , katı bir çok dış etkiye karşı koruma altındadır."],

        "Alüminyum": [
            "Alüminyum gövdeli bu ürün bir çok farklı ve zor çevre şartları için sağlam ve uzun ömürlü olarak üretilmiştir",
            "bu ürün güçlü ve sağlam gövdesi ile uzun ömürlü bir yapıya sahiptir. Ayrıca şık bir görünüme sahiptir."
            "Şık yapısı ve uzun ömürlü özelliği ile üretilen bu ürün yıllara meydan okumaktadır."
        ],

        "Belge": [
            "Uluslararası standartlarda üretilen ürünümüz #belge belgelerine sahip her türlü projede kullanabilceğiniz ürünlerdir",
            "#belge belgerine sahip olan ürünümüz yerli ve yabancı bir çok projede ve kişisel kullanıma uygun üretilmiştir.",
            "Bu ürün uluslararası geçerliliğe sahip olan #belge belgelerine sahip bir üründür."

        ],
        "Işık Akısı": [
            "Birim zamanda kaynaktan çıkan ışık miktarı #ışıkakısı Lümen kadardır",
            "Güçlü bir ışık akısına sahip bu ürün #ışıkakısı Lümen özelliğindedir",
            "#ışık akısı Lümen özelliğine sahip bu ürün aydınlatma konusunda yeteneklidir."
        ],
        "Açık Alan": [
            "Açık alan kullanımına uygundur #açıkalan gibi alanlarda kullanımı test edilmiştir.",
            "Ürünümüzü #açıkalan ve benzeri bir çok alanda yüksek verim ile kullanabilirsiniz. Çevre koşullarına dayanıklıdır."
            "Bu ürün #açıkalan ve bir çok farklı alan için özel hazırlanmış bir üründür."
        ],
        "Darbe Dayanıklılığı": ["Darbelere dayanıklı bir üründür. Darbe dayanıklılığı #koddarbe standartlarındadır",
                                "Bu ürün #koddarbe kodlu dayanıklılık standardında üretilmiştir."],
        "IP65": ["Toz ve su geçirmez IP65 kodu içeren bu ürünümüz dış kullanım için uygundur",
                 "IP65 kodu bulunan bu ürün toz ve düşük tazyik'de su geçirmez",
                 "Bu ürünün IP seviyesi 65'dir. Bu toz ve su geçirmezlik anlamına gelir",
                 "IP65 seviyesinde üretilen bu ürün toz ve suya karşı koruma sağlar",
                 "Dış etkenlere karşı (su,toz) koruma sağlayan IP65 seviyesine sahiptir",
                 "IP65 sınıflandırma kodu ile üretilen bu ürün sıvı ve katı malzemelere karşı koruma sağlamaktadır. Ayrıca toza karşı da güvenlik sağlamaktadır",
                 "Bu ürün toz başta olmak üzere katı ve sıvı bir çok dış etkiye karşı koruma sınıfı olan IP65 ile üretilmiştir.",
                 "Ürünümüz Uluslararası bir sınıflandırma olan IP65 koduyla sıvı , katı bir çok dış etkiye karşı koruma altındadır."],
        "Tamperli": [
            "Bu ürün Tamperli dış cama sahiptir.Güvenli ve sağlam olan tamperli camlar kırılmaya karşı dayanıklıdır",
            "Tamperli cam teknolojisiyle üretilen bu ürün kırılmaya karşı dayanıklı bir cama sahipti.",
            "Bu ürün kırılmaya karşı dayanıklı tamperli cam teknolojisine sahiptir"],
        "Çalışma Ömrü": ["Yüksek çalışma ömrüne sahip olan ürünümüzün çalışma süresi #kodcs kadardır",
                         "#kodcs 'ye kadar çalışma saatine sahip olan ürünümüz uzun yıllar size hizmet sağlayacaktır.",
                         "Uzun ömrü ile bilinen bu ürün sizlere #kodcs 'ye kadar çalışma ömrü sunmaktadır."],
        "Çalışma Sıcaklığı": [
            "Sıcaklık şartlarına karşı dayanıklı olan ürünümüz #kodisi arasındaki tüm sıcaklıklarda verimli bir şekilde çalışmaktadır",
            "Bu ürün #kodisi arasında verimli ve kaliteli bir şekilde sorunsuz ve verimli bir şekilde çalışmaktadır",
            ],
        "Alüminyum Enjeksiyon": [
            "Ürünümüz alüminyum enjeksiyon yapısı sayesinde korozyona karşı büyük bir avantaj sağlamaktadır. Aluminyum yapılar plastiklere göre daha dayanıklı olmaktadır."],
        "Işık Açısı": [
            "Ürünümüzün ışık açısı #kodisik derecedir. Hangi ışık açısına ihtiyacınız olduğu emin değilseniz bizimle iletişime geçebilirsiniz",
            "#kodisik ışık açısı bulunan bu ürünü bir çok farklı amaçla kullanabilirsiniz.",
            "Bu ürün #kodisik derecesinde açıya sahiptir.Işık açıları hakkında daha fazla bilgi almak için bizimle iletişime geçin",
            ],
        "Renk Sıcaklığı": [
            "Ürünümüzün renk sıcaklığı #kodrenk dir. mutel.com.tr içerisinde diğer renklerde ve sıcaklıklarda ürünlerimize de göz atabilirsiniz"],

    }

    altyazi = {
        "2 Yıl": ["Uzun ömürlü düşük enerji tüketimine sahip olan bu ürünümüz 2 yıl garanti kapsamındadır.",
                  "2 Yıl garantili olan ürünümüzü gönül rahatlığı ile satın alabilirsiniz",
                  "Bu ürünü hızlı ve güvenli kargo ayrıca 2 yıl garanti ile hemen satın alabilirsiniz",
                  "Bu ürün 2 yıllık garanti belgesi ile beraber gönderilmektedir."],
        "Flicker Free": [
            "Ürünümüz Aydınlatmadaki önemli problemlerde biri olan titremeye karşı Flicker Free teknolojisiyle üretilmiştir.",
            "Flicker Free teknolojisiyle üretilen ürünümüz titreme yapmaz"
        ]
    }


    def spinle(yazi):
        spinsozluk = {
            "Açık alan": ["Açık alan", "Outdoor", "Dış mekan"],
            "en bilinen": ["en bilinen", "en çok bilinen", "en prestijli", "en çok güvenilen"],
            "zorlu şartlarda": ["zorlu şartlarda", "zorlu koşullarda", "en zorlu çevre şartlarında"],
            "Tüm ihtiyaçlar": ["Tüm ihtiyaçlar", "Tüm beklentiler", "Endüstriyel beklentiler", "Her türlü talep"],
            "piyasaya sürülmüştür": ["piyasaya sürülmüştür", "satışa sunulmuştur"],
            "en gelişmiş": ["en gelişmiş", "en son teknojilerle geliştirilmiş", "en gelişmiş"],
            "Hem çevre dostu hem de kaliteli": ["Hem çevre dostu hem de kaliteli", "Kaliteli ve çevre dostu"],
            "değerine sahip": ["değerine sahip", "değelerine sahip"],
            "En çok tercih edilen": ["Çok beğenilen", "En çok tercih edilen", "En beğenilen"],
            "Alüminyum gövdeli": ["Alüminyum gövdeli", "Alüminyum kasalı", "Alaşımlı alüminyum gövdeli"],
            "Şık yapısı": ["Şık yapısı", "Modern görünümü", "İlgi çeken yapısı"],
            "Uluslararası standartlarda": ["Uluslararası standartlarda", "Dünyaca standartlarında",
                                           "Avrupa ve Dünya standartlarında"],

        }

        for i in spinsozluk:
            yazi = yazi.replace(i, random.choice(spinsozluk[i]))

        return yazi


    xx=all_features(aciklama_features(aciklamatext),title_features(urun_baslik),kategori_features(kategori))
    yaziliste=text_generator(xx)[:7]
    random.shuffle(yaziliste)

    sonuc=spinle(" ".join(yaziliste))

    st.write(sonuc)
