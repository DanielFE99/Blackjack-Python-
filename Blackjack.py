regler = '''
Prøv å komme så nært til 21 som mulig uten å gå over.
Konge, dronning og knekt er verdt 10 poeng hver.
Ess er verdt 1 eller 11 poeng.
(H)it for å be om ett kort til.
(S)tand for å ikke ta kort.
På første spill kan du bruke (D)ouble for å doble
hvor mye du hart veddet, men du må "hitte" en gang
før du kan stå.
I tilfelle uavgjort blir veddemålet returnert til spilleren.
Dealeren stopper å hitte på 17.
'''
import random, sys
#------------
HJERTER = chr(9829)
RUTER = chr(9830)
SPAR = chr(9824)
KLØVER = chr(9827)
BAKSIDE = 'bakside'

def main():
    print(regler)

    konto = 5000
    while True:
        if konto <= 0:
            print('Kontoen din er tom for penger')
            print('Takk for at du spillte')
            sys.exit()

        #lar spilleren velge innsatsen
        print('konto: ', konto)
        innsats = hentInnsats(konto)

        #Gir dealeren og spilleren to kort fra kortstokken hver
        kortstokk = hentKort()
        dealerKort = [kortstokk.pop(), kortstokk.pop()]
        spillerKort = [kortstokk.pop(), kortstokk.pop()]

        #håndterer spiller interaksjon
        print('Veddet: ', innsats)
        while True: #loopen fortsetter til spilleren står eller går over 21 (bust)
            visHånd(spillerKort, dealerKort, False)
            print()

            if hentKortverdi(spillerKort) > 21:
                break

            #Hent spillerens trekk H, S eller D
            trekk = hentTrekk(spillerKort, konto - innsats)

            #Håndterer spiller interaksjon
            if trekk == 'D':
                #Spilleren "hentKortverdis down", de kan øke innsatsen
                tilleggsInnsats = hentInnsats(min(innsats, (konto - innsats)))
                innsats += tilleggsInnsats
                print('Bet increased to '.format(innsats))
                print('Innsats: '.format(innsats))

            if trekk in ('H','D'):
                #Hit/doubling får gir spilleren et ekstra kort
                nyttKort = kortstokk.pop()
                rank, suit = nyttKort
                print('Du fikkk en {} {}.'.format(rank, suit))
                spillerKort.append(nyttKort)

                if hentKortverdi(spillerKort) > 21:
                    continue

            if trekk in ('S', 'D'):
                break

        if hentKortverdi(spillerKort) <= 21:
            while hentKortverdi(dealerKort) < 17:
                #dealeren trekker kort
                print('dealeren trekker kort...')
                dealerKort.append(kortstokk.pop())
                visHånd(spillerKort, dealerKort, False)

                if hentKortverdi(dealerKort) > 21:
                    break #bust
                input('Trykk på enter for å fortsette')
                print('\n\n')

        visHånd(spillerKort, dealerKort, True)

        spillerVerdi = hentKortverdi(spillerKort)
        dealerVerdi = hentKortverdi(dealerKort)

        if dealerVerdi > 21:
            print('Dealeren tapte, du vant! Du får {}kr'.format(innsats))
            konto += innsats
        elif (spillerVerdi > 21) or (spillerVerdi < dealerVerdi):
            print('Du tapte!')
            konto -= innsats
        elif spillerVerdi > dealerVerdi:
            print('du vant {}'.format(innsats))
            konto += innsats
        elif spillerVerdi == dealerVerdi:
            print('Uavgjort! innsatsen returneres til deg')

        input('trykk Enter for å fortsette...')
        print('\n\n')

def hentInnsats(maksInnsats):
    #spør spilleren hvor mye de vil satse denne runden
    while True:
        print('Hvor mye vil du satse? (1-{}, elller QUIT)'.format(maksInnsats))
        innsats = input('> ').upper().strip()

        if innsats == 'QUIT':
            print('takk for at du spilte')
            sys.exit()

        if not innsats.isdecimal():
            continue #spilleren oppga ikke et nummer

        innsats = int(innsats)
        if 1 <= innsats <= maksInnsats:
            return innsats #spilleren oppga et gyldig beløp

def hentKort():
    #returnerer en kortstokk
    kortstokk = []
    for suit in (HJERTER, RUTER, SPAR, KLØVER):
        for rank in range(2, 11):
            kortstokk.append((str(rank), suit))
        for rank in ('J','Q','K','A'):
            kortstokk.append((rank, suit))
    random.shuffle(kortstokk)
    return kortstokk

def visHånd(spillerKort, dealerKort, visDealerKort):
    """Viser spillerens og dealerens kort. Hvis visDealerKort er
    alse gjemmes dealerens første """
    if visDealerKort:
        print('DEALER:', hentKortverdi(dealerKort))
        visKort(dealerKort)
    else:
        print('DEALER: ???')
        #gjemmer dealerens første kort
        visKort([BAKSIDE] + dealerKort[:1])

    #vis spillerens kort
    print('SPILLER:', hentKortverdi(spillerKort))
    visKort(spillerKort)

def hentKortverdi(alleKort):
    """Returnerer verdien til kort.Ess er verdt 1 eller 11.
    Funksjonen velger det beste alternativet"""
    verdi = 0
    antallEss = 0

    #Legg til verdien for vanlige kort
    for kort in alleKort:
        rank = kort[0] #kort er en tuple (rank, suit)
        if rank == 'A':
            antallEss += 1
        elif rank in ('K', 'Q', 'J'):
            verdi += 10
        else:
            verdi += int(rank)

    #legg til verdien for ess(ene)
    verdi += antallEss
    #Hvis ekstra 10 poeng kan legges til uten å buste gjøres det
    for i in range (antallEss):
        if verdi + 10 <= 21:
            verdi += 10

    return verdi

def visKort(alleKort):
    """Viser alle kortene i kortlisten"""
    rader = ['', '', '', '', ''] #teksten som vises på hver rad

    for i, kort in enumerate(alleKort):
        rader[0] += ' ___ ' #toppen av kortet
        if kort == BAKSIDE:
            rader[1] += '|## | '
            rader[2] += '|###| '
            rader[3] += '|_##| '
        else:
            #print forsiden av kortet
            rank, suit = kort
            rader[1] += '|{} | '.format(rank.ljust(2))
            rader[2] += '| {} | '.format(suit)
            rader[3] += '|_{}| '.format(rank.rjust(2, '_'))

    for rad in rader:
        print(rad)

def hentTrekk(spillerKort, konto):
    """Spør spilleren for trekket, og returnerer H for hit,
    S for stand, og D for double down"""
    while True:
        #loopen fortsetter til spilleren oppgir gyldig valg
        lovligetrekk = ['(H)it', '(S)tand']

        #Spilleren kan doble på sitt første trekk
        #Dette kan vi avgjøre ved at spilleren bare har to kort
        if len(spillerKort) == 2 and konto > 0:
            lovligetrekk.append('(D)ouble down')

        #Hent spillerens trekk
        trekkPrompt = ', '.join(lovligetrekk) + '> '
        trekk = input(trekkPrompt).upper()
        if trekk in ('H', 'S'):
            return trekk
        if trekk == 'D' and '(D)ouble down' in lovligetrekk:
            return trekk

if __name__=='__main__':
    main()























