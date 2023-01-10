import pygame, random

class Sudoku():
    def __init__(self):
        pygame.init()
        #Peliruudukko jota muokataan ja joka tulostetaan pelaajalle
        self.vaikeustaso = ""
        self.peliruudukko = self.muodosta_vaikeustaso(1)
        self.oikea_ratkaisu = self.uusi_sudoku()
        self.valmis = True
        self.pelaa_uusi_peli = False
        self.kysy_vaikeus = True
        self.ruutua_klikattu = False
        self.klikattu_ruutu = (11, 11)
        self.testia_klikattu = 0

        self.aika_sekunteina = 0
        self.aika_minuutteina = 0

        self.korkeus = 9
        self.leveys = 9
        self.skaala = 40
        nayton_korkeus = self.skaala * self.korkeus
        nayton_leveys = self.skaala * self.leveys
        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus + 160))

        pygame.display.set_caption("Sudoku")

        self.pelisilmukka()


    #Toistettava silmukka
    def pelisilmukka(self):
        kello = pygame.time.Clock()
        aika = 0
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()
            self.testaa_ratkaisu()
            if self.valmis and self.pelaa_uusi_peli:
                self.valitse_vaikeustaso()
            #Aika etenee jos peli ei ole valmis
            if not self.valmis:
                kello.tick(60)
                aika += 1
                if aika >= 60:
                    self.aika_sekunteina += 1
                    aika = 0
                if self.aika_sekunteina >= 60:
                    self.aika_sekunteina = 0
                    self.aika_minuutteina += 1


    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            #Jos painetaan peli-ikkunan rastia niin suljetaan ikkuna
            if tapahtuma.type == pygame.QUIT:
                exit()
            
            #Seurataan tapahtumia jos peli kesken
            if self.valmis == False:
                #Jos klikataan ruutua niin kirjataan muistiin, että mitä ruutua on klikattu
                if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                    x, y = tapahtuma.pos
                    ruutu_x = x // 40
                    ruutu_y = (y - 40) // 40
                    if 0 <= ruutu_x < 9 and 0 <= ruutu_y < 9:
                        #Jos klikattu ruutu on pelin alussa annettu ruutu, niin oletetaan että pelaaja ei halua muuttaa mitään ruutua
                        if self.peliruudukko[ruutu_y][ruutu_x] == "X":
                            self.ruutua_klikattu = False
                            pass
                        else:
                            self.ruutua_klikattu = True
                            self.klikattu_ruutu = (ruutu_x, ruutu_y)
                    #Jos klikataan päävalikko-nappia
                    if 103 < x < 257 and 407 < y < 435:
                        self.valmis = True
                        self.kysy_vaikeus = True

                #Jos ruuuta klikattu, otetaan vastaan numero ja kirjataan muistiin että ruutua ei ole klikattu
                if tapahtuma.type == pygame.KEYDOWN:
                    if self.ruutua_klikattu == True:
                        x = self.klikattu_ruutu[0]
                        y = self.klikattu_ruutu[1]
                        syote = int(str(tapahtuma.key)[-2:]) - 48
                        if int(syote) == 0:
                            self.peliruudukko[y][x] = 0
                            self.ruutua_klikattu = False
                        elif 0 < int(syote) <= 9:
                            self.peliruudukko[y][x] = int(syote)
                            self.ruutua_klikattu = False
                        else:
                            #Jos ei hyväksyttävä syöte, niin oletetaan että pelaaja ei halunnut antaa syötettä
                            self.ruutua_klikattu = False

            #Seurataan tapahtumia jos peli on valmis
            else:
                #Jos vaikeustasovalikossa
                if self.kysy_vaikeus:
                    if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                        x, y = tapahtuma.pos
                        #Jos klikataan Helppo
                        if 130 < x < 230 and 207 < y < 237:
                            self.peliruudukko = self.muodosta_vaikeustaso(1)
                            self.oikea_ratkaisu = self.uusi_sudoku()
                            self.valmis = False
                            self.kysy_vaikeus = False
                            self.testia_klikattu = 0
                            self.nollaa_aika()
                        #Jos klikataan keski
                        if 130 < x < 230 and 247 < y < 277:
                            self.peliruudukko = self.muodosta_vaikeustaso(2)
                            self.oikea_ratkaisu = self.uusi_sudoku()
                            self.valmis = False
                            self.kysy_vaikeus = False
                            self.testia_klikattu = 0
                            self.nollaa_aika()
                        #Jos klikataan vaikea
                        if 130 < x < 230 and 287 < y < 317:
                            self.peliruudukko = self.muodosta_vaikeustaso(3)
                            self.oikea_ratkaisu = self.uusi_sudoku()
                            self.valmis = False
                            self.kysy_vaikeus = False
                            self.testia_klikattu = 0
                            self.nollaa_aika()
                        #Jos klikataan Vaikeustasonappia kolmesti
                        if 40 < x < 320 and 148 < y < 188:
                            self.testia_klikattu += 1
                            if self.testia_klikattu >= 3:
                                self.peliruudukko = self.muodosta_vaikeustaso(9)
                                self.oikea_ratkaisu = self.uusi_sudoku()
                                self.valmis = False
                                self.kysy_vaikeus = False
                                self.testia_klikattu = 0
                                self.nollaa_aika()
                #Jos ollaan pelinjälkeisessä "haluatko pelata uudestaan" valikossA
                else:
                    #Otetaan muistiin kumpaa ruutua painettiin
                    if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                        x, y = tapahtuma.pos
                        #Jos klikataan Kyllä uusi peli
                        if 90 < x < 160 and 470 < y < 510:
                            self.kysy_vaikeus = True
                        #Jos klikataan Ei uutta peliä
                        elif 210 < x < 280 and 470 < y < 510:
                            exit()


    def piirra_naytto(self):
        self.naytto.fill((100, 100, 100))

        #Piirrä ruudut
        for y in range(self.korkeus):
            for x in range(self.leveys):
                ruutu = self.peliruudukko[y][x]
                if ruutu == "X":
                    #Jos ruutu on pelin alussa annettu numero, tulostetaan sen kohdalle ratkaisumatriisista sen arvo
                    pygame.draw.rect(self.naytto, (50, 50, 50), (x * self.skaala + 2, y * self.skaala + 42, 38, 38))
                    fontti = pygame.font.SysFont("Arial", 30)
                    teksti = fontti.render(f"{self.oikea_ratkaisu[y][x]}", True, (255, 255, 255))
                    self.naytto.blit(teksti, (x * self.skaala + 12, y * self.skaala + 44))
                elif 0 < ruutu < 10:
                    #Jos ruudun arvo on välillä 1-9 niin tulostetaan se
                    pygame.draw.rect(self.naytto, (240, 240, 240), (x * self.skaala + 2, y * self.skaala + 42, 38, 38))
                    fontti = pygame.font.SysFont("Arial", 30)
                    teksti = fontti.render(f"{ruutu}", True, (0, 0, 0))
                    self.naytto.blit(teksti, (x * self.skaala + 12, y * self.skaala + 44))
                elif ruutu == 0:
                    #Jos ruudun arvo on 0, niin tulostetaan ruutu tyhjänä
                    pygame.draw.rect(self.naytto, (240, 240, 240), (x * self.skaala + 2, y * self.skaala + 42, 38, 38))

        #Väritä klikattu ruutu
        if self.valmis == False:
            if self.ruutua_klikattu:
                x = self.klikattu_ruutu[0]
                y = self.klikattu_ruutu[1]
                pygame.draw.rect(self.naytto, (200, 255, 200), (x * 40 + 2, y * 40 + 42, 38, 38))

        #Piirrä 3x3 ruudukot rajaavat viivat
        pygame.draw.rect(self.naytto, (0, 0, 0), (118, 40, 5, 360))
        pygame.draw.rect(self.naytto, (0, 0, 0), (238, 40, 5, 360))
        pygame.draw.rect(self.naytto, (0, 0, 0), (0, 158, 360, 5))
        pygame.draw.rect(self.naytto, (0, 0, 0), (0, 278, 360, 5))
        pygame.draw.rect(self.naytto, (255, 255, 255), (120, 40, 1, 360))
        pygame.draw.rect(self.naytto, (255, 255, 255), (240, 40, 1, 360))
        pygame.draw.rect(self.naytto, (255, 255, 255), (0, 160, 360, 1))
        pygame.draw.rect(self.naytto, (255, 255, 255), (0, 280, 360, 1))

        #Piirrä tekstiboksi pelikentän ylle
        pygame.draw.rect(self.naytto, (255, 255, 255), (0, 0, 360, 40))
        pygame.draw.rect(self.naytto, (50, 50, 50), (8, 0, 344, 36))
        pygame.draw.rect(self.naytto, (255, 255, 255), (0, 0, 360, 35))
        fontti = pygame.font.SysFont("Arial", 24)
        teksti = fontti.render(f"{self.vaikeustaso} Sudoku", True, (0, 0, 0))
        teksti_aika = fontti.render(f"{self.aika_minuutteina:02d}:{self.aika_sekunteina:02d}", True, (0, 0, 0))
        self.naytto.blit(teksti, (11, 7))
        self.naytto.blit(teksti_aika, (292, 7))

        #Piirrä tekstiboksi pelikentän alle
        pygame.draw.rect(self.naytto, (255, 255, 255), (0, 402, 360, 118))
        #Takaisin päävalikkoon-nappi
        pygame.draw.rect(self.naytto, (0, 0, 0), (103, 407, 154, 28))
        pygame.draw.rect(self.naytto, (255, 255, 255), (105, 409, 150, 24))
        fontti_palaa = pygame.font.SysFont("Arial", 16)
        teksti_palaa = fontti_palaa.render("Uusi vaikeustaso", True, (0, 0, 0))
        leveys_palaa = teksti_palaa.get_width()
        self.naytto.blit(teksti_palaa, (180 - leveys_palaa / 2, 412))
        if self.valmis:
            #Piirrä jos ollaan valitsemassa vaikeustasoa:
            if self.kysy_vaikeus:
                pygame.draw.rect(self.naytto, (255, 255, 255), (0, 0, 360, 540))
                fontti_iso = pygame.font.SysFont("Arial", 32)
                fontti = pygame.font.SysFont("Arial", 20)         
                #Valitse vaikeus
                pygame.draw.rect(self.naytto, (255, 255, 255), (40, 148, 280, 40))
                teksti_vaikeus = fontti_iso.render("Valitse vaikeustaso", True, (0, 0, 0))
                leveys_vaikeus = teksti_vaikeus.get_width()
                self.naytto.blit(teksti_vaikeus, (180 - leveys_vaikeus / 2, 150))
                #Helppo
                pygame.draw.rect(self.naytto, (0, 0, 0), (130, 207, 100, 30))
                pygame.draw.rect(self.naytto, (255, 255, 255), (132, 209, 96, 26))
                teksti_helppo = fontti.render("Helppo", True, (0, 0, 0))
                leveys_helppo = teksti_helppo.get_width()
                self.naytto.blit(teksti_helppo, (180 - leveys_helppo / 2, 210))
                #Keskitaso
                pygame.draw.rect(self.naytto, (0, 0, 0), (130, 247, 100, 30))
                pygame.draw.rect(self.naytto, (255, 255, 255), (132, 249, 96, 26))
                teksti_keski = fontti.render("Keskitaso", True, (0, 0, 0))
                leveys_keski = teksti_keski.get_width()
                self.naytto.blit(teksti_keski, (180 - leveys_keski / 2, 250))
                #Vaikea
                pygame.draw.rect(self.naytto, (0, 0, 0), (130, 287, 100, 30))
                pygame.draw.rect(self.naytto, (255, 255, 255), (132, 289, 96, 26))
                teksti_vaikea = fontti.render("Vaikea", True, (0, 0, 0))
                leveys_vaikea = teksti_vaikea.get_width()      
                self.naytto.blit(teksti_vaikea, (180 - leveys_vaikea / 2, 290))
   

            #Piirrä jos ei olla valitsemassa vaikeustasoa mutta peli on valmis
            else:    
                pygame.draw.rect(self.naytto, (200, 255, 200), (0, 402, 360, 118))
                fontti = pygame.font.SysFont("Arial", 24)
                teksti = fontti.render("Voitit pelin!", True, (0, 0, 0))
                teksti2 = fontti.render("Haluatko pelata uudestaan?", True, (0, 0, 0))
                self.naytto.blit(teksti, (125, 407))
                self.naytto.blit(teksti2, (35, 435))
                #Kyllä nappi
                pygame.draw.rect(self.naytto, (0, 0, 0), (90, 470, 70, 40))
                pygame.draw.rect(self.naytto, (255, 255, 255), (92, 472, 66, 36))
                teksti3 = fontti.render("Kyllä", True, (0, 0, 0))
                self.naytto.blit(teksti3, (98, 476))
                #Ei nappi
                pygame.draw.rect(self.naytto, (0, 0, 0), (210, 470, 70, 40))
                pygame.draw.rect(self.naytto, (255, 255, 255), (212, 472, 66, 36))
                teksti4 = fontti.render("Ei", True, (0, 0, 0))
                self.naytto.blit(teksti4, (232, 476))
    
        pygame.display.flip()

    #Nollaa aika
    def nollaa_aika(self):
        self.aika_sekunteina = 0
        self.aika_minuutteina = 0


    #Netistä kopsattu koodi luo uuden arvotun täyden sudoku-pohjan
    def uusi_sudoku(self):
        pohja  = 3
        sivu  = pohja*pohja

        # pattern for a baseline valid solution
        def pattern(r,c): return (pohja*(r%pohja)+r//pohja+c)%sivu

        # randomize rows, columns and numbers (of valid base pattern)
        from random import sample
        def shuffle(s): return sample(s,len(s)) 
        rpohja = range(pohja) 
        rivit  = [g*pohja + r for g in shuffle(rpohja) for r in shuffle(rpohja)] 
        sarakkeet  = [g*pohja + c for g in shuffle(rpohja) for c in shuffle(rpohja)]
        numerot  = shuffle(range(1,pohja*pohja+1))

        # produce board using randomized baseline pattern
        ruudukko = [[numerot[pattern(r,c)] for c in sarakkeet] for r in rivit]

        return ruudukko


    #Tarkistaa onko täytetty sudoku sääntöjen mukainen
    def testaa_ratkaisu(self):
        rivit_oikein = False
        sarakkeet_oikein = False
        ruudukot_oikein = False
        testattava = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        #Täytetään tarkistettavan matriisin arvot peliruudukosta ja korvataan X:t oikean ratkaisun arvoilla
        y = 0
        for rivi in testattava:
            x = 0
            for sarake in rivi:
                testattava[y][x] = self.peliruudukko[y][x]
                if testattava[y][x] == "X":
                    testattava[y][x] = self.oikea_ratkaisu[y][x]
                x += 1
            y += 1

        #Tarkistetaan onko rivit oikein
        rivia_oikein = 0
        for rivi in testattava:
            if len(set(rivi)) == 9 and 0 not in rivi:
                rivia_oikein += 1
        if rivia_oikein == 9:
            rivit_oikein = True

        #Tarkistetaan onko sarakkeet oikein
        sarakkeita_oikein = 0
        sarake = []
        indeksi = 0
        while indeksi < 9:
            for rivi in testattava:
                sarake.append(rivi[indeksi])
            if len(set(sarake)) == 9 and 0 not in sarake:
                sarakkeita_oikein += 1
            indeksi += 1
        if sarakkeita_oikein == 9:
            sarakkeet_oikein = True

        #Tarkistetaan onko miniruudukot oikein
        ruudukkoja_oikein = 0
        ruudukko_1 = [testattava[0][0], testattava[0][1], testattava[0][2],
                      testattava[1][0], testattava[1][1], testattava[1][2],
                      testattava[2][0], testattava[2][1], testattava[2][2]]
        ruudukko_2 = [testattava[0][3], testattava[0][4], testattava[0][5],
                      testattava[1][3], testattava[1][4], testattava[1][5],
                      testattava[2][3], testattava[2][4], testattava[2][5]]
        ruudukko_3 = [testattava[0][6], testattava[0][7], testattava[0][8],
                      testattava[1][6], testattava[1][7], testattava[1][8],
                      testattava[2][6], testattava[2][7], testattava[2][8]]
        ruudukko_4 = [testattava[3][0], testattava[3][1], testattava[3][2],
                      testattava[4][0], testattava[4][1], testattava[4][2],
                      testattava[5][0], testattava[5][1], testattava[5][2]]
        ruudukko_5 = [testattava[3][3], testattava[3][4], testattava[3][5],
                      testattava[4][3], testattava[4][4], testattava[4][5],
                      testattava[5][3], testattava[5][4], testattava[5][5]]
        ruudukko_6 = [testattava[3][6], testattava[3][7], testattava[3][8],
                      testattava[4][6], testattava[4][7], testattava[4][8],
                      testattava[5][6], testattava[5][7], testattava[5][8]]
        ruudukko_7 = [testattava[6][0], testattava[6][1], testattava[6][2],
                      testattava[7][0], testattava[7][1], testattava[7][2],
                      testattava[8][0], testattava[8][1], testattava[8][2]]
        ruudukko_8 = [testattava[6][3], testattava[6][4], testattava[6][5],
                      testattava[7][3], testattava[7][4], testattava[7][5],
                      testattava[8][3], testattava[8][4], testattava[8][5]]
        ruudukko_9 = [testattava[6][6], testattava[6][7], testattava[6][8],
                      testattava[7][6], testattava[7][7], testattava[7][8],
                      testattava[8][6], testattava[8][7], testattava[8][8]]
        ruudukot = [ruudukko_1, ruudukko_2, ruudukko_3, ruudukko_4, ruudukko_5, ruudukko_6, ruudukko_7, ruudukko_8, ruudukko_9]
        for ruudukko in ruudukot:
            if len(set(ruudukko)) == 9 and 0 not in ruudukko:
                ruudukkoja_oikein += 1
        if ruudukkoja_oikein == 9:
            ruudukot_oikein = True
        #Jos kaikki oikein, sudoku on ratkaistu
        if ruudukot_oikein and rivit_oikein and sarakkeet_oikein:
            self.valmis = True


    #Antaa peliruudukon jossa on vaikeustason määräämä lukumäärä annettuja ruutuja
    def muodosta_vaikeustaso(self, vaikeustaso: int):
        peliruudukko = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        if vaikeustaso == 1:
            self.vaikeustaso = "Helppo "
            annettuja_yht = 45
            annettuja_nyt = 0
            while annettuja_nyt < annettuja_yht:
                rivi = random.choice(range(9))
                indeksi = random.choice(range(9))
                if peliruudukko[rivi][indeksi] == 0:
                    peliruudukko[rivi][indeksi] = "X"
                    annettuja_nyt += 1
        elif vaikeustaso == 2:
            self.vaikeustaso = "Keskitason "
            annettuja_yht = 40
            annettuja_nyt = 0
            while annettuja_nyt < annettuja_yht:
                rivi = random.choice(range(9))
                indeksi = random.choice(range(9))
                if peliruudukko[rivi][indeksi] == 0:
                    peliruudukko[rivi][indeksi] = "X"
                    annettuja_nyt += 1
        elif vaikeustaso == 3:
            self.vaikeustaso = "Vaikea "
            annettuja_yht = 35
            annettuja_nyt = 0
            while annettuja_nyt < annettuja_yht:
                rivi = random.choice(range(9))
                indeksi = random.choice(range(9))
                if peliruudukko[rivi][indeksi] == 0:
                    peliruudukko[rivi][indeksi] = "X"
                    annettuja_nyt += 1
        elif vaikeustaso == 9:
            self.vaikeustaso = "Testi "
            annettuja_yht = 80
            annettuja_nyt = 0
            while annettuja_nyt < annettuja_yht:
                rivi = random.choice(range(9))
                indeksi = random.choice(range(9))
                if peliruudukko[rivi][indeksi] == 0:
                    peliruudukko[rivi][indeksi] = "X"
                    annettuja_nyt += 1
        return peliruudukko






if __name__ == "__main__":
    Sudoku()


    