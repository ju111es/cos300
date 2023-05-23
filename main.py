from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import random as rnd

from idlelib.tooltip import Hovertip as Ht

# привет :D и доброе пожаловать!!
# я надеюсь, что это легко понять- comments may be in weird orders just because of the order in which i did things,
# и как все изменил через время
# будьте добрый со мной :') я сделала лучшо, что я могла делать и я думаю, что это хорош...
# ведь, это достаточно хорош для меня :P

all_verbs = []
all_nouns = []

pronounsn = {'я':'i', 'ты':'you', 'он':'he', 'она':'she', 'оно':'it',
             'мы':'we', 'вы':'you (polite/plural)', 'они':'they'}
ilist = ['г', 'к', 'х', 'ж', 'ч', 'ш', 'щ']
ylist = ilist
ylist.append('ц')
alist = ylist
olist = ['ж', 'ч', 'ш', 'щ', 'ц']
vowels = ['а', 'я', 'у', 'ю', 'о', 'е', 'ё', 'и', 'ы']

tried = []
correct_count1 = 0
correct_count = 0

questions = []
inp = []

def spellcheck(string):
    # some vowels (ы, ю, я, sometimes o) can't follow certain consonants.
    ispelling = []
    for letter in ilist:
        ispelling.append(letter + 'ы')
    yspelling = []
    for letter in ylist:
        yspelling.append(letter + 'ю')
    aspelling = []
    for letter in alist:
        aspelling.append(letter + 'я')

    for item in ispelling:
        if item in string:
            return str(item + 'i')
        else:
            pass
    for item in yspelling:
        if item in string:
            return str(item + 'y')
        else:
            pass
    for item in aspelling:
        if item in string:
            return str(item + 'a')
        else:
            pass
    return False

class Noun:
    def __init__(self, noun, nom_stem, nom_end, gender, animate, english):
        self.noun = noun
        self.gender = gender
        self.animate = animate
        self.nom_stem = nom_stem
        self.nom_end = nom_end
        self.english = english

        global all_nouns
        all_nouns.append(self)

        self.g = [[self.nom_stem], [self.nom_stem]]
        self.a = [[self.nom_stem], [self.nom_stem]]
        self.p = [[self.nom_stem], [self.nom_stem]]
        self.d = [[self.nom_stem], [self.nom_stem]]
        self.i = [[self.nom_stem], [self.nom_stem]]
        self.cases = [self.g, self.a, self.p, self.d, self.i]
        if self.nom_end != '':
            self.plural = self.noun.rstrip(self.noun[-1])
            if self.nom_end == 'я́':
                # for whatever reason this one counts as two characters
                self.plural = self.plural.rstrip(self.plural[-1])
        else:
            self.plural = self.noun
        # letters stand for genitive, accusative, prepositional, dative, and instrumental (cases).
        # nouns have different endings in each case depending on the letter they end in,
        # as well as different plural endings in both the nominative (default) case and others.
        # in the accusative case, it is relevant whether the noun is animate or not.
        # it is also sometimes relevant where the word is stressed. i'm still figuring out how to incorporate this.
        self.assign_cases()

    def assign_cases(self):
        if self.nom_end == 'а' or self.nom_end == 'á':
            if self.nom_end == 'á':
                self.plural = self.plural + 'ы́'
            else:
                self.plural = self.plural + 'ы'
            self.g[0].append('ы')
            if self.nom_stem[-1] not in vowels and self.nom_stem[-2] not in vowels:
                # if a noun ends in a double consonant it is common to add an extra letter in the genitive plural
                # ex тарелка would be тарелк, but instead it's тарелок for ease of pronunciation
                # this is true for -a and -o nouns, whose genitive plurals are formed by removing the last letter,
                # and for -я nouns, whose genitive plural is formed by replacing the я with a soft sign
                if self.nom_stem[-2] in olist:
                    self.g_stem = self.nom_stem.rstrip(self.nom_stem[-1]) + 'е' + self.nom_stem[-1]
                else:
                    self.g_stem = self.nom_stem.rstrip(self.nom_stem[-1]) + 'о' + self.nom_stem[-1]
                self.g[1][0] = self.g_stem
            self.g[1].append('')
            if self.nom_stem[-1] in olist:
                self.i[0].append('ей')
            else:
                self.i[0].append('ой')
            self.i[1].append('ами')
            self.a[0].append('у')
            self.p[0].append('е')
            self.p[1].append('ах')
            self.d[0].append('е')
            self.d[1].append('ам')

        elif self.nom_end == 'я' or self.nom_end == 'я́':
            if self.nom_end == 'я́':
                self.plural = self.plural + 'и́'
            else:
                self.plural = self.plural + 'и'
            self.a[0].append('ю')
            if self.nom_stem[-1] == 'и':
                self.p[0].append('и')
                self.d[0].append('и')
            else:
                self.p[0].append('е')
                self.d[0].append('е')
            self.g[0].append('и')
            if self.nom_stem[-1] in vowels:
                self.g[1].append('й')
            else:
                if self.nom_stem[-1] not in vowels and self.nom_stem[-2] not in vowels:
                    if self.nom_stem[-1] in olist:
                        self.g_stem = self.nom_stem.rstrip(self.nom_stem[-1]) + 'е' + self.nom_stem[-1]
                    else:
                        self.g_stem = self.nom_stem.rstrip(self.nom_stem[-1]) + 'о' + self.nom_stem[-1]
                    self.g[1][0] = self.g_stem
                self.g[1].append('ь')
            if self.nom_end == 'я́':
                self.i[0].append('ёй')
            else:
                self.i[0].append('ей')
            self.p[1].append('ях')
            self.d[1].append('ям')
            self.i[1].append('ями')

        elif self.nom_end == '':
            self.plural = self.plural + 'ы'
            self.a[0].append('а')
            self.g[0].append('а')
            if self.nom_end == 'ж' or self.nom_end == 'ч' or self.nom_end == 'ш' or self.nom_end == 'щ':
                self.g[1].append('ев')
            else:
                self.g[1].append('ов')
            self.p[0].append('е')
            self.p[1].append('ах')
            self.d[0].append('у')
            self.d[1].append('ам')
            self.i[0].append('ом')
            self.i[1].append('ами')

        elif self.nom_end == 'й':
            self.plural = self.plural + 'и'
            self.a[0].append('я')
            self.g[0].append('я')
            self.g[1].append('ев')
            self.p[0].append('е')
            self.p[1].append('ях')
            self.d[0].append('ю')
            self.d[1].append('ям')
            self.i[0].append('ем')
            self.i[1].append('ями')

        elif self.nom_end == 'ь':
            # this letter (the 'soft sign') can indicate either a masculine or feminine noun.
            # case endings differ based on the noun's gender.
            self.plural = self.plural + 'и'
            if self.gender == 'm':
                self.g[0].append('я')
                self.a[0].append('я')
                self.p[0].append('е')
                self.d[0].append('ю')
                self.i[0].append('ем')
            elif self.gender == 'f':
                self.a[0].append(self.nom_end)
                self.g[0].append('и')
                self.p[0].append('е')
                self.d[0].append('и')
                self.i[0].append('ью')
            self.g[1].append('ей')
            self.p[1].append('ях')
            self.d[1].append('ям')
            self.i[1].append('ями')

        elif self.nom_end == 'о' or self.nom_end == 'ó':
            if self.nom_end == 'ó':
                self.plural = self.plural + 'á'
            else:
                self.plural = self.plural + 'а'
            self.a[0].append(self.nom_end)
            self.g[0].append('а')
            if self.nom_stem[-1] not in vowels and self.nom_stem[-2] not in vowels:
                self.g_stem = self.nom_stem.rstrip(self.nom_stem[-1]) + 'о' + self.nom_stem[-1]
                self.g[1][0] = self.g_stem
            self.g[1].append('')
            self.p[0].append('е')
            self.p[1].append('ах')
            self.d[0].append('у')
            self.d[1].append('ам')
            self.i[0].append('ом')
            self.i[1].append('ами')

        elif self.nom_end == 'е' or self.nom_end == 'é':
            if self.nom_end == 'é':
                self.plural = self.plural + 'я́'
            else:
                self.plural = self.plural + 'я'
            self.a[0].append(self.nom_end)
            self.g[0].append('я')
            if self.nom_stem[-1] == 'и':
                self.p[0].append('и')
                self.g[1].append('й')
            else:
                self.p[0].append('е')
                self.g[1].append('ей')
            self.d[0].append('ю')
            self.i[0].append('ем')
            self.p[1].append('ях')
            self.d[1].append('ям')
            self.i[1].append('ями')

        if self.nom_stem[-1] in ilist and (self.plural[-1] == 'ы' or self.plural[-1] == 'ы́'):
            if self.plural[-1] == 'ы́':
                self.plural = self.plural.rstrip('ы́')
                self.plural = self.plural + 'и́'
                self.g[0][1] = self.g[0][1].replace('ы́', 'и́')
            else:
                self.plural = self.plural.rstrip('ы')
                self.plural = self.plural + 'и'
                self.g[0][1] = self.g[0][1].replace('ы', 'и')
        if self.nom_stem[-1] in ylist:
            self.d[0][1] = self.d[0][1].replace('ю', 'у')
            self.d[0][1] = self.d[0][1].replace('ю́', 'у́')
        if self.nom_stem[-1] in alist:
            if self.plural[-1] == 'я́':
                self.plural = self.plural.rstrip('я́')
                self.plural = self.plural + 'а'
            elif self.plural[-1] == 'я':
                self.plural = self.plural.rstrip('я')
                self.plural = self.plural + 'а'
            self.g[0][1] = self.g[0][1].replace('я', 'а')
            self.a[0][1] = self.a[0][1].replace('я', 'а')
            self.p[1][1] = self.p[1][1].replace('я', 'а')
            self.d[1][1] = self.d[1][1].replace('я', 'а')
            self.i[1][1] = self.i[1][1].replace('я', 'а')

            self.g[0][1] = self.g[0][1].replace('я́', 'á')
            self.a[0][1] = self.a[0][1].replace('я́', 'á')
            self.p[1][1] = self.p[1][1].replace('я́', 'á')
            self.d[1][1] = self.d[1][1].replace('я́', 'á')
            self.i[1][1] = self.i[1][1].replace('я́', 'á')
        if self.nom_stem[-1] in olist:
            if self.nom_end != 'á':
                self.i[0][1] = self.i[0][1].replace('о', 'е')
            else:
                pass

        if self.animate is True:
            self.a[1] = self.g[1]
        else:
            self.a[1].append(self.plural[-1])
            if self.gender == 'm':
                self.a[0][1] = self.nom_end

        self.g[0] = ''.join(self.g[0]); self.g[1] = ''.join(self.g[1])
        self.a[0] = ''.join(self.a[0]); self.a[1] = ''.join(self.a[1])
        self.p[0] = ''.join(self.p[0]); self.p[1] = ''.join(self.p[1])
        self.d[0] = ''.join(self.d[0]); self.d[1] = ''.join(self.d[1])
        self.i[0] = ''.join(self.i[0]); self.i[1] = ''.join(self.i[1])

    def translate(self):
        form = questions[all_nouns.index(self)]
        if form == self.plural:
            # see if it's plural; if it is, assign the correct plural form
            vowels_eng = ['a', 'e', 'i', 'o', 'u']
            if self.english[-1] == 'y' and self.english[-2] not in vowels_eng:
                lisst = list(self.english)
                lisst.pop(-1)
                translation = ''.join(lisst) + 'ies'
            elif self.english[-1] == 'f':
                lisst = list(self.english)
                lisst.pop(-1)
                translation = ''.join(lisst) + 'ves'
            elif self.english[-1] == 'e' and self.english[-2] == 'f':
                lisst = list(self.english)
                lisst.pop(-2)
                lisst.insert(2, 'v')
                translation = ''.join(lisst) + 's'
            elif self.english[-1] == 's':
                translation = self.english + 'es'
            elif self.english[-1] == 'h' and (self.english[-2] == 'c' or self.english[-2] == 's'):
                translation = self.english + 'es'
            else:
                translation = self.english + 's'
        else:
            translation = self.english
        return translation

    def print_cases(self):
        print(self.noun, 'in all 6 cases:')
        print('Nominative:', self.noun, self.plural, end='  ')
        print('Genitive:', ''.join(self.g[0]), ''.join(self.g[1]))
        print('Accusative:', ''.join(self.a[0]), ''.join(self.a[1]), end='  ')
        print('Prepositional:', ''.join(self.p[0]), ''.join(self.p[1]))
        print('Dative:', ''.join(self.d[0]), ''.join(self.d[1]), end='  ')
        print('Instrumental:', ''.join(self.i[0]), ''.join(self.i[1]))
        print('\n')

    def case_check(self):
        # figure out whether the answer is singular or plural
        form = questions[all_nouns.index(self)]
        # assign value as answer
        if form == self.plural:
            index = 1
        else:
            index = 0
        if mode == 'genitive':
            a = ''.join(self.g[index])
        elif mode == 'accusative':
             a = ''.join(self.a[index])
        elif mode == 'prepositional':
            a = ''.join(self.p[index])
        elif mode == 'dative':
            a = ''.join(self.d[index])
        else:
            a = ''.join(self.i[index])

        # get input to check against answer
        i = inp[all_nouns.index(self)].get()

        global tried
        global correct_count1
        global correct_count

        nw = Tk()
        correction = ''
        if i != a:
            # did they apply the wrong case?
            nominative = i == self.noun or i == self.plural
            genitive = a not in self.g and i in self.g
            accusative = a not in self.a and i in self.a
            prepositional = a not in self.p and i in self.p
            dative = a not in self.d and i in self.d
            instrumental = a not in self.i and i in self.i

            # did they use the singular form when assigned plural, or vice versa?
            wrong_plurality = False
            if form == self.plural:
                for item in self.cases:
                    if i == item[0]:
                        wrong_plurality = True
            else:
                for item in self.cases:
                    if i == item[1]:
                        wrong_plurality = True

            if nominative or genitive or accusative or prepositional or dative or instrumental:
                correction = 'It looks like you applied the wrong case.' \
                             '\nIf you need a refresher on the ' + str(mode) + ' case, click Learn.'
            elif wrong_plurality:
                correction = 'Make sure you are applying the ' + str(mode) + ' form \nmatching the given nominative form.'
            elif spellcheck(i) is not False:
                error = spellcheck(i)
                correction = error[1] + ' cannot follow ' + error[0] + '.'
            else:
                pass
            if mode == 'genitive':
                if i == self.nom_stem or i == self.nom_stem + 'ь' and i != self.g[1][1]:
                    correction = 'Usually o or e is added to a stem ending in a double consonant.' \
                                 '\nIf you need a refresher on the genitive case, click Learn.'
                aend1 = self.nom_end == 'а' or self.nom_end == 'á'
                aend2 = self.nom_end == 'я' or self.nom_end == 'я́'
                oliststem = self.nom_stem[-2] in olist
                if oliststem:
                    if aend1 and len(i) > 2 and i[-2] == 'о' or aend2 and i[-3] == 'о':
                        correction = 'An unstressed o cannot follow ж, ц, ч, ш, or щ- \ninstead, use e.'
            elif mode == 'accusative':
                if self.gender == 'm' and self.animate is False and i in self.g:
                    correction = 'Inanimate masculine nouns do not change \nin the accusative case.' \
                                 '\nIf you need a refresher on the accusative case, click Learn.'
                elif form == self.plural and self.animate is False and i in self.g:
                    correction = 'Inanimate nouns use their nominative plural in the accusative.' \
                                 '\nIf you need a refresher on the accusative case, click Learn.'
            elif mode == 'prepositional':
                if self.nom_end == 'я' or self.nom_end == 'е' and self.nom_stem[-1] == 'и' and i[-1] == 'е':
                    correction = 'ия and ие become ии, not ие.' \
                                 '\nIf you need a refresher on the prepositional case, click Learn.'
            elif mode == 'dative':
                if self.nom_end == 'я' and self.nom_stem[-1] == 'и' and i[-1] == 'е':
                    correction = 'ия becomes ии, not ие.' \
                                 '\nIf you need a refresher on the dative case, click Learn.'
                elif self.nom_end == 'е' and self.nom_stem[-1] == 'и' and i == ''.join(self.p[0]):
                    correction = 'Unlike the prepositional, ие and е nouns behave the same \nin the dative case. \n' \
                                 'If you need a refresher on the dative case, click Learn.'
            elif mode == 'instrumental':
                if form != self.plural and self.nom_stem[-1] in olist and self.nom_end != 'á' and len(i) > 2 and \
                        i[-2] == 'о':
                    correction = 'An unstressed o cannot follow ж, ц, ч, ш, or щ- \ninstead, use e.'
                elif form != self.plural and self.nom_end == 'я́' and len(i) > 2 and i[-2] == 'е':
                    correction = 'When stressed, е becomes ё.'
            if correction == '':
                correction = 'Incorrect...'
        else:
            correction = 'Correct!'
            correct_count += 1
            if self not in tried:
                correct_count1 += 1

        tried.append(self)
        cc1 = 'Questions correctly answered on first try: ' + str(correct_count1)
        cc_label1 = ttk.Label(nw, text=cc1)
        cc = 'Total correct answers: ' + str(correct_count)
        cc_label = ttk.Label(nw, text=cc)

        correction_label = ttk.Label(nw, text=correction)
        correction_label.place(x=8, y=8)
        cc_label1.place(x=8, y=53)
        cc_label.place(x=8, y=73)
        nw.geometry('350x100+150+150')

class Verb:

    def __init__(self, verb, stem, ending, english):
        self.verb = verb
        self.stem = stem
        self.ending = ending
        self.english = english

        global all_verbs
        all_verbs.append(self)

        self.conjugate()

    def conjugate(self):
        if self.ending == 'ить':
            self.conjugation = 2
        else:
            self.conjugation = 1

        self.i = []
        self.you = []
        self.he = []
        self.we = []
        self.you_p = []
        self.they = []
        self.conjs = [self.i, self.you, self.he, self.we, self.you_p, self.they]

        # in russian, there are first and second conjugation verbs.
        # verbs are conjugated differently based on what group they're in.
        # this is not currently accounting for irregular verbs ...
        # (ones whose infinitives and present tense stems vary in unexpected ways).
        # it isn't accounting for those which are in an unexpected conjugation group either, but it will be!

        if self.conjugation == 1:

            if self.find_mutation() is True:
                for item in self.conjs:
                    item.append(self.mutStem)
            else:
                for item in self.conjs:
                    item.append(self.stem)
            if self.ending == 'ать' and self.find_mutation() is False or \
                    self.ending == 'ять' or self.ending == 'еть':
                for item in self.conjs:
                    item.append(self.ending[0])
            elif self.ending == 'авать':
                for item in self.conjs:
                    item.append('а')
            elif self.ending == 'овать' or self.ending == 'евать':
                for item in self.conjs:
                    item.append('у')
            elif self.ending == 'ыть':
                for item in self.conjs:
                    item.append('о')
            if len(self.i[-1]) > 0 and self.i[-1][-1] in ylist:
                self.i.append('у')
                self.they.append('ут')
            else:
                self.i.append('ю')
                self.they.append('ют')
            self.you.append('ешь')
            self.he.append('ет')
            self.we.append('ем')
            self.you_p.append('ете')
            if self.ending == 'стать' or self.ending == 'деть' or \
                    self.ending == 'нять' or self.ending == 'ереть':
                if self.ending == 'нять':
                    if self.stem[-1] in vowels:
                        if self.stem[-1] == 'и':
                            for item in self.conjs:
                                item.insert(1, 'м')
                        else:
                            for item in self.conjs:
                                item.insert(1, 'йм')
                    else:
                        for item in self.conjs:
                            item.insert(1, 'ним')
                elif self.ending == 'ереть':
                    for item in self.conjs:
                        item.insert(1, 'р')
                else:
                    for item in self.conjs:
                        item.insert(1, (self.ending.replace('ть', 'н')))
                if self.i[-1] == 'ю':
                    self.i[-1] = 'у'
                    self.they[-1] = 'ут'
                else:
                    pass

            # as you can see, there are many ways verbs can be conjugated depending on their infinitive form.
            # i've accounted for all of the regular ways here.
            # unfortunately it is not currently possible to use '-ти', '-зть/сть' or '-чь' verbs,
            # as they are unpredictable :/
            # i think i will make a list or something of irregular verbs once i finish everything else.
            # (second conjugation verbs below- they're much simpler)

        else:
            for item in self.conjs:
                item.append(self.stem)
            if self.find_mutation() is True:
                self.i[0] = self.mutStem
            self.you.append('ишь')
            self.he.append('ит')
            self.we.append('им')
            self.you_p.append('ите')
            if len(self.i[-1]) > 0 and self.i[-1][-1] in ylist:
                self.i.append('у')
            else:
                self.i.append('ю')
            if len(self.they[-1]) > 0 and self.they[-1][-1] in alist:
                self.they.append('ат')
            else:
                self.they.append('ят')

        for item in self.conjs:
            self.conjs[self.conjs.index(item)] = ''.join(item)

        # past tense is formed based on the gender of the subject (masc, fem, neu, or plural).
        self.past_stem1 = self.stem
        self.past_stem2 = list(self.ending)
        self.past_stem2.pop(-1)
        self.past_stem2.pop(-1)
        if self.ending == 'ереть':
            self.past_stem2.pop(-1)
        self.past_stem = self.past_stem1 + ''.join(self.past_stem2)
        if self.ending == 'ереть':
            self.mpast = self.past_stem
            self.fpast = self.past_stem + 'а'
            self.npast = self.past_stem + 'о'
            self.ppast = self.past_stem + 'и'
        else:
            self.mpast = self.past_stem + 'л'
            self.fpast = self.past_stem + 'ла'
            self.npast = self.past_stem + 'ло'
            self.ppast = self.past_stem + 'ли'

    def find_mutation(self):
        # some consonants 'mutate' in certain verb conjugations. this function predicts when they will.
        mutants = ['п', 'б', 'ф', 'м', 'в', 'к', 'т', 'д', 'з', 'г', 'с', 'х']
        if len(self.stem) > 0:
            lc = self.stem[-1]  # last consonant
        else:
            return False
        if self.ending == 'ать' or self.ending == 'ить':
            if lc in mutants:
                # grouping consonants which mutate the same way
                if lc == 'п' or lc == 'б' or lc == 'ф':
                    self.mutStem = self.stem + 'л'
                    return True
                elif lc == 'м' or lc == 'в':
                    self.mutStem = self.stem + 'л'
                    if self.ending == 'ить':
                        return True
                    elif self.ending == 'ать':
                        return False
                elif lc == 'к' or lc == 'т':
                    if self.stem[-2] == 'с':
                        self.mutStem = self.stem.rstrip('с' + lc) + 'щ'
                        return True
                    elif lc == 'т' and self.ending == 'ать':
                        self.mutStem = self.stem.rstrip(lc) + 'ч'
                        return False
                    else:
                        self.mutStem = self.stem.rstrip(lc) + 'ч'
                        return True
                elif lc == 'д' or lc == 'з' or lc == 'г':
                    if lc == 'г' or lc == 'д' and self.ending == 'ать':
                        self.mutStem = self.stem.rstrip(lc) + 'ж'
                        return False
                    else:
                        self.mutStem = self.stem.rstrip(lc) + 'ж'
                        return True
                elif lc == 'с' or lc == 'х':
                    self.mutStem = self.stem.rstrip(lc) + 'ш'
                    return True
            else:
                return False
        else:
            return False

    def translate(self):
        pronoun = questions[all_verbs.index(self)][0]
        translation = pronounsn.get(pronoun)
        if translation == 'i':
            translation = 'I'

        english = self.english

        if mode != 'past tense':
            if translation == 'he' or translation == 'she' or translation == 'it':
                vowels_eng = ['a', 'e', 'i', 'o', 'u']
                if ' ' in english:
                    # if it's two words (like 'put on') it will conjugate the first, then re-add the second at the end
                    lisst1 = list(english)
                    english = lisst1[0]
                    # otherwise ...
                # this will detect whether it's any kind of irregular sort of conjugation
                if english[-1] == 'y' and english[-2] not in vowels_eng:
                    lisst = list(english)
                    lisst.pop(-1)
                    translation = translation + ' ' + ''.join(lisst) + 'ies'
                elif english[-1] == 'h' and (english[-2] == 'c' or english[-2] == 's'):
                    translation = translation + ' ' + english + 'es'
                elif english[-1] == 's':
                    translation = translation + ' ' + english + 'es'
                elif english[-1] == 'o' and english[-2] not in vowels:
                    translation = translation + ' ' + english + 'es'
                elif english == 'have':
                    translation = translation + ' ' + 'has'
                else:
                    translation = translation + ' ' + english + 's'
                try:
                    translation = translation + lisst1[1]
                except NameError:
                    pass
            else:
                translation = translation + ' ' + english
        else:
            translation = translation + ' ' + english
            # if it's in past tense mode i'll just put the english parameter in the past tense form because english
            # has stupid irreuglar past tense.
            # i know it's not totally ideal but it's not so bad imo
        return translation

    def print_conjs(self):
        print(self.verb, 'conjugation:\n' + str(self.conjs), '\n')

    def cm_check(self):
        # if someone uses the wrong letter, not applying consonant mutation or applying it where they shouldn't,
        # this will recognize and explain their mistake.

        pronoun = questions[all_verbs.index(self)][0]
        pronouns = list(pronounsn.keys())
        pronouns.pop(pronouns.index('она'))
        pronouns.pop(pronouns.index('оно'))
        if pronoun == 'она' or pronoun == 'оно':
            pronoun_index = pronouns.index('он')
        else:
            pronoun_index = pronouns.index(pronoun)
        a = self.conjs[pronoun_index]

        i = inp[all_verbs.index(self)].get()
        # more thorough explanation in present_check()

        global tried
        global correct_count1

        nw = Tk()
        nw.withdraw()
        if i != a:
            if self.find_mutation() is True and self.stem in i:
                correction = 'This is an instance of consonant mutation. ' \
                           '\nIf you need a refresher on how it works, click Learn.'
            elif hasattr(self, 'mutStem') and self.mutStem in i and self.find_mutation() is False:
                correction = 'This is NOT an instance of consonant mutation. ' \
                             '\nIf you need a refresher on how it works, click Learn.'
            elif self.present_check() != ':P':
                # if the error isn't related to consonant mutation, it will be corrected here (unless it's just random)
                correction = self.present_check()
            elif spellcheck(i) != False:
                error = spellcheck(i)
                correction = error[1] + ' cannot follow ' + error[0] + '.'
            else:
                correction = 'Incorrect...'
        else:
            correction = 'Correct!'
            if self not in tried:
                correct_count1 += 1

        tried.append(self)
        cc = 'Questions correctly answered on first try: ' + str(correct_count1)
        cc_label = ttk.Label(nw, text=cc)

        correction_label = ttk.Label(nw, text=correction)
        correction_label.place(x=8, y=8)
        cc_label.place(x=8, y=53)
        nw.geometry('350x80+150+150')
        nw.deiconify()

    def present_check(self):
        # fetch the pronoun currently attached to the verb
        pronoun = questions[all_verbs.index(self)][0]
        pronouns = list(pronounsn.keys())
        pronouns.pop(pronouns.index('она'))
        pronouns.pop(pronouns.index('оно'))
        # get rid of she and it pronouns because they're the same as he and mess up the index
        if pronoun == 'она' or pronoun == 'оно':
            pronoun_index = pronouns.index('он')
        else:
            pronoun_index = pronouns.index(pronoun)
        # and, assign the answer to check input against accordingly
        a = self.conjs[pronoun_index]

        # fetch user input
        i = inp[all_verbs.index(self)].get()

        global tried
        global correct_count1

        nw = Tk()
        nw.withdraw()
        if i != a:
            # if someone uses the wrong conjugation:
            wrong_i = a == ''.join(self.i) and i == self.conjs[1] or i == self.conjs[2] or i == self.conjs[3] \
                or i == self.conjs[4] or i == self.conjs[5]
            wrong_you = a == ''.join(self.you) and i == self.conjs[0] or i == self.conjs[2] or i == self.conjs[3] \
                or i == self.conjs[4] or i == self.conjs[5]
            wrong_he = a == ''.join(self.he) and i == self.conjs[0] or i == self.conjs[1] or i == self.conjs[3] \
                or i == self.conjs[4] or i == self.conjs[5]
            wrong_we = a == ''.join(self.we) and i == self.conjs[0] or i == self.conjs[1] or i == self.conjs[2] \
                or i == self.conjs[4] or i == self.conjs[5]
            wrong_youp = a == ''.join(self.you_p) and i == self.conjs[0] or i == self.conjs[1] or i == self.conjs[2] \
                or i == self.conjs[3] or i == self.conjs[5]
            wrong_they = a == ''.join(self.they) and i == self.conjs[0] or i == self.conjs[1] or i == self.conjs[2] \
                or i == self.conjs[3] or i == self.conjs[4]

            wrong_pronoun = wrong_i or wrong_you or wrong_he or wrong_we or wrong_youp or wrong_they

            # if they put it in past tense:
            past = i == self.mpast or i == self.fpast or i == self.npast or i == self.ppast

            # i don't want to have to remove the pronoun if someone enters it so it will just tell them not to (again)
            pronoun_entered = False
            for item in list(pronounsn.keys()):
                if (item + ' ') in i:
                    pronoun_entered = True
                else:
                    pass

            if wrong_pronoun:
                if mode == 'consonant mutation':
                    correction = 'It looks like you used the wrong conjugation.\n If you need a ' \
                               'refresher on present tense conjugation, \ngo to Lessons.'
                    # if they're in consonant mutation mode it says to open the Lessons window
                    # also returns so nothing weird happens with the windows
                    return correction
                else:
                    correction = 'It looks like you used the wrong conjugation.\n If you need a ' \
                               'refresher on present tense conjugation, \nclick Learn.'
                    # otherwise it just says to click Learn
            elif past:
                if mode == 'consonant mutation':
                    correction = 'Consonant mutation only occurs in present tense.' \
                                 '\nIf you need a refresher on how it works, click Learn.'
                    return correction
                else:
                    correction = 'Remember, this is present tense practice!'
            elif pronoun_entered:
                correction = 'Please enter just the verb, not the pronoun.'
                if mode == 'consonant mutation':
                    return correction
            else:
                # if they got it wrong in some other, unpredictable way:
                correction = 'Incorrect...'
            if mode == 'consonant mutation' and wrong_pronoun is False and past is False and pronoun_entered is False:
                return ':P'
        else:
            correction = 'Correct!'
            if self not in tried:
                correct_count1 += 1

        tried.append(self)
        cc = 'Questions correctly answered on first try: ' + str(correct_count1)
        cc_label = ttk.Label(nw, text=cc)

        correction_label = ttk.Label(nw, text=correction)
        correction_label.place(x=8, y=8)
        cc_label.place(x=8, y=53)
        nw.geometry('350x80+150+150')
        nw.deiconify()

    def past_check(self):
        pronoun = questions[all_verbs.index(self)][0]
        if pronoun == 'он':
            a = self.mpast
        elif pronoun == 'она':
            a = self.fpast
        elif pronoun == 'оно':
            a = self.npast
        else:
            a = self.ppast

        i = inp[all_verbs.index(self)].get()

        global tried
        global correct_count1

        nw = Tk()
        if i != a:
            wrong_he = a == self.mpast and i == self.fpast or i == self.npast or i == self.ppast
            wrong_she = a == self.fpast and i == self.mpast or i == self.npast or i == self.ppast
            wrong_it = a == self.npast and i == self.mpast or i == self.fpast or i == self.ppast
            wrong_plural = a == self.ppast and i == self.fpast or i == self.npast or i == self.npast

            present = i in self.conjs

            pronoun_entered = False
            for item in list(pronounsn.keys()):
                if (item + ' ') in i:
                    pronoun_entered = True
                else:
                    pass

            if wrong_he or wrong_she or wrong_it or wrong_plural:
                correction = 'It looks like you used the wrong conjugation.\n If you need a ' \
                             'refresher on past tense conjugation, \nclick Learn.'
                # unlike present_check(), this doesn't have to return anything because i'm not using it elsewhere
            elif present:
                correction = 'Remember, this is past tense practice!'
            elif pronoun_entered:
                correction = 'Please enter just the verb, not the pronoun.'
            else:
                correction = 'Incorrect...'
        else:
            correction = 'Correct!'
            if self not in tried:
                correct_count1 += 1

        tried.append(self)
        cc = 'Questions correctly answered on first try: ' + str(correct_count1)
        cc_label = ttk.Label(nw, text=cc)

        correction_label = ttk.Label(nw, text=correction)
        correction_label.place(x=8, y=8)
        cc_label.place(x=8, y=53)
        nw.geometry('350x80+150+150')

    def conj_check(self):
        if mode == 'consonant mutation':
            self.cm_check()
        elif mode == 'present tense':
            self.present_check()
        elif mode == 'past tense':
            self.past_check()


mw = Tk()

lcmw = Tk()
cmw = Tk()
lgcw = Tk()
gcw = Tk()
lacw = Tk()
acw = Tk()
lpcw = Tk()
pcw = Tk()
ldcw = Tk()
dcw = Tk()
licw = Tk()
icw = Tk()
lprtw = Tk()
prtw = Tk()
lpatw = Tk()
patw = Tk()
lw = Tk()
windows = [lcmw, cmw, lgcw, gcw, lacw, acw, lpcw, pcw, ldcw, dcw, licw, icw, lprtw, prtw, lpatw, patw, lw]
# all of the windows that will be used
# don't hate ! :P

def home():
    for item in windows:
        item.withdraw()
    # closing all of the other windows since they open upon being created
    mw.deiconify()
    # in case the window has previously been withdrawn (if we're coming from the Lessons window or a practice mode)

    greeting = ttk.Label(mw, text='Welcome! What would you like to practice?')

    gogc = ttk.Button(mw, text='Genitive Case', command=gc)
    goac = ttk.Button(mw, text='Accusative Case', command=ac)
    gopc = ttk.Button(mw, text='Prepositional Case', command=pc)
    godc = ttk.Button(mw, text='Dative Case', command=dc)
    goic = ttk.Button(mw, text='Instrumental Case', command=ic)
    gocm = ttk.Button(mw, text='Consonant Mutation', command=cm)
    goprt = ttk.Button(mw, text='Present Tense', command=prt)
    gopat = ttk.Button(mw, text='Past Tense', command=pat)

    lessonslbl = ttk.Label(mw, text='Or, go to')
    golessons = ttk.Button(mw, text='Lessons', command=lessons)

    greeting.place(x=20, y=18)

    gogc.place(x=20,y=50)
    goac.place(x=20,y=80)
    gopc.place(x=20,y=110)
    godc.place(x=20,y=140)
    goic.place(x=20,y=170)
    gocm.place(x=135,y=50)
    goprt.place(x=135, y=80)
    gopat.place(x=135, y=110)

    lessonslbl.place(x=20, y=214)
    golessons.place(x=75, y=210)

    mw.geometry('280x245+485+230')
    mw.title('Русские Упражения') # russian practice (exercises, precisely)
    mw.mainloop()

def tutorial(string):
    # pops up upon opening any mode
    addition = '\n\nHover your cursor over any question to see it in English. ' \
               '\nThere are stress marks in the questions to help with learning and answering questions; ' \
               'enter your answers without stress marks.'
    messagebox.showinfo(message=string + addition)

def lessons():
    mw.withdraw()
    for item in windows:
        item.withdraw()

    greeting = ttk.Label(lw, text='Welcome! What would you like to learn?')

    lgc_button = ttk.Button(lw, text='Genitive case', command=lgc)
    lac_button = ttk.Button(lw, text='Accusative case', command=lac)
    lpc_button = ttk.Button(lw, text='Prepositional case', command=lpc)
    ldc_button = ttk.Button(lw, text='Dative case', command=ldc)
    lic_button = ttk.Button(lw, text='Instrumental case', command=lic)

    lcm_button = ttk.Button(lw, text='Consonant mutation', command=lcm)
    lpresent_button = ttk.Button(lw, text='Present tense', command=lprt)
    lpast_button = ttk.Button(lw, text='Past tense', command=lpat)

    gohome = ttk.Button(lw, text='Home', command=home)

    lgc_button.place(x=20, y=50)
    lac_button.place(x=20, y=80)
    lpc_button.place(x=20, y=110)
    ldc_button.place(x=20, y=140)
    lic_button.place(x=20, y=170)
    lcm_button.place(x=135, y=50)
    lpresent_button.place(x=135,y=80)
    lpast_button.place(x=135, y=110)
    gohome.place(x=20, y=210)
    greeting.place(x=20, y=18)
    lw.geometry('280x245+485+230')
    lw.title('Русские Уроки') # russian lessons
    lw.deiconify()
    lw.mainloop()

mode = None

def casepractice(case, window, learn):
    global tried
    global correct_count1
    global correct_count
    tried = []
    correct_count1 = 0
    correct_count = 0
    # set score to zero

    global mode
    mode = case
    # set the mode

    mw.withdraw()
    for item in windows:
        item.withdraw()

    tut = 'Enter the ' + mode + ' form of the given nominative noun. There are singular and plural nouns given- ' \
          'enter the ' + mode + ' genitive form matching the given nominative form.'
    tutorial(tut)

    lc_frame = ttk.Frame(window)
    lc_lbl = ttk.Label(lc_frame, text='Don\'t know the ' + mode + ' case?')
    golc = ttk.Button(lc_frame, text='Learn', command=learn)
    # in case someone doesn't know the subject yet or needs a refresher,
    # they can open a window anytime with a concise but (hopefully??) clear explanation.
    # it's probably more useful as a refresher for someone who has already learned it than a lesson.

    global inp
    inp1 = ttk.Entry(window)
    inp2 = ttk.Entry(window)
    inp3 = ttk.Entry(window)
    inp4 = ttk.Entry(window)
    inp5 = ttk.Entry(window)
    inp6 = ttk.Entry(window)
    inp7 = ttk.Entry(window)
    inp8 = ttk.Entry(window)
    inp9 = ttk.Entry(window)
    inp10 = ttk.Entry(window)
    inp = [inp1, inp2, inp3, inp4, inp5, inp6, inp7, inp8, inp9, inp10]

    global questions
    questions = []

    for i in range(len(all_nouns)):
        p = rnd.randint(0, 1)
        if p == 0:
            questions.append(all_nouns[i].noun)
        else:
            questions.append(all_nouns[i].plural)
    # randomize whether the noun is singular or plural so user can practice both forms
    # all_nouns will be populated by nouns defined in each case function

    ent1 = ttk.Button(window, command=all_nouns[0].case_check, text='Enter')
    ent2 = ttk.Button(window, command=all_nouns[1].case_check, text='Enter')
    ent3 = ttk.Button(window, command=all_nouns[2].case_check, text='Enter')
    ent4 = ttk.Button(window, command=all_nouns[3].case_check, text='Enter')
    ent5 = ttk.Button(window, command=all_nouns[4].case_check, text='Enter')
    ent6 = ttk.Button(window, command=all_nouns[5].case_check, text='Enter')
    ent7 = ttk.Button(window, command=all_nouns[6].case_check, text='Enter')
    ent8 = ttk.Button(window, command=all_nouns[7].case_check, text='Enter')
    ent9 = ttk.Button(window, command=all_nouns[8].case_check, text='Enter')
    ent10 = ttk.Button(window, command=all_nouns[9].case_check, text='Enter')
    ent = [ent1, ent2, ent3, ent4, ent5, ent6, ent7, ent8, ent9, ent10]

    lbl1 = ttk.Label(window, text=(questions[0] + '\n\n'))
    lbl2 = ttk.Label(window, text=(questions[1] + '\n\n'))
    lbl3 = ttk.Label(window, text=(questions[2] + '\n\n'))
    lbl4 = ttk.Label(window, text=(questions[3] + '\n\n'))
    lbl5 = ttk.Label(window, text=(questions[4] + '\n\n'))
    lbl6 = ttk.Label(window, text=(questions[5] + '\n\n'))
    lbl7 = ttk.Label(window, text=(questions[6] + '\n\n'))
    lbl8 = ttk.Label(window, text=(questions[7] + '\n\n'))
    lbl9 = ttk.Label(window, text=(questions[8] + '\n\n'))
    lbl10 = ttk.Label(window, text=(questions[9] + '\n\n'))
    lbl = [lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7, lbl8, lbl9, lbl10]

    ht1 = Ht(lbl1, text=all_nouns[0].translate())
    ht2 = Ht(lbl2, text=all_nouns[1].translate())
    ht3 = Ht(lbl3, text=all_nouns[2].translate())
    ht4 = Ht(lbl4, text=all_nouns[3].translate())
    ht5 = Ht(lbl5, text=all_nouns[4].translate())
    ht6 = Ht(lbl6, text=all_nouns[5].translate())
    ht7 = Ht(lbl7, text=all_nouns[6].translate())
    ht8 = Ht(lbl8, text=all_nouns[7].translate())
    ht9 = Ht(lbl9, text=all_nouns[8].translate())
    ht10 = Ht(lbl10, text=all_nouns[9].translate())

    lc_lbl.pack(side=LEFT)
    golc.pack(side=RIGHT)
    lc_frame.place(x=5, y=3)
    # i wanted to use a frame for the questions and everything but it looked bad :/
    # anyway this is helpful since lc_lbl will change size depending on the mode

    gohome = ttk.Button(window, text='Home', command=home)
    golessons = ttk.Button(window, text='Lessons', command=lessons)
    gohome.place(x=5, y=330)
    golessons.place(x=83, y=330)

    y1 = 30
    for q in range(len(all_nouns)):
        lbl[q].place(x=5, y=y1)
        inp[q].place(x=85, y=y1)
        ent[q].place(x=215, y=y1 - 1)
        window.update()
        y1 += 30

    window.geometry('300x360+475+170')
    title = list(mode)
    title[0] = title[0].upper()
    title = ''.join(title)
    window.title(title + ' case')
    # geometry and title (i wanted the title uppercase; it looks nicer)
    # the +475+170 sets it to the middle of the screen. there might be a better way of doing that but idrc

    window.deiconify()
    # in case it's been closed
    window.mainloop()

def verbpractice(tense, cm, window, learn):
    global tried
    global correct_count1
    global correct_count
    tried = []
    correct_count1 = 0
    correct_count = 0

    global mode
    if cm is True:
        mode = 'consonant mutation'
    else:
        mode = tense + ' tense'

    mw.withdraw()
    for item in windows:
        item.withdraw()

    tut = 'Enter just the ' + tense + ' tense conjugation of the verb according to the pronoun in front of it' \
          'and press Enter. (Don\'t enter the pronoun, or it won\'t work correctly! Just the verb.)'
    if cm is True:
        tut = tut + '\n\nSome of these conjugations will have consonant mutation, some won\'t.'
    tutorial(tut)

    global inp
    inp1 = ttk.Entry(window)
    inp2 = ttk.Entry(window)
    inp3 = ttk.Entry(window)
    inp4 = ttk.Entry(window)
    inp5 = ttk.Entry(window)
    inp6 = ttk.Entry(window)
    inp7 = ttk.Entry(window)
    inp8 = ttk.Entry(window)
    inp9 = ttk.Entry(window)
    inp10 = ttk.Entry(window)
    inp = [inp1, inp2, inp3, inp4, inp5, inp6, inp7, inp8, inp9, inp10]

    global questions
    questions = []

    pronouns = list(pronounsn.keys())
    for a in range(len(all_verbs)):
        q = []
        q.append(pronouns[rnd.randint(0,len(pronouns)-1)])
        q.append(all_verbs[a].verb)
        questions.append(q)

    ent1 = ttk.Button(window, command=all_verbs[0].conj_check,text='Enter')
    ent2 = ttk.Button(window, command=all_verbs[1].conj_check,text='Enter')
    ent3 = ttk.Button(window, command=all_verbs[2].conj_check,text='Enter')
    ent4 = ttk.Button(window, command=all_verbs[3].conj_check,text='Enter')
    ent5 = ttk.Button(window, command=all_verbs[4].conj_check,text='Enter')
    ent6 = ttk.Button(window, command=all_verbs[5].conj_check,text='Enter')
    ent7 = ttk.Button(window, command=all_verbs[6].conj_check,text='Enter')
    ent8 = ttk.Button(window, command=all_verbs[7].conj_check,text='Enter')
    ent9 = ttk.Button(window, command=all_verbs[8].conj_check,text='Enter')
    ent10 = ttk.Button(window, command=all_verbs[9].conj_check,text='Enter')
    ent = [ent1, ent2, ent3, ent4, ent5, ent6, ent7, ent8, ent9, ent10]

    lbl1 = ttk.Label(window, text=(' '.join(questions[0]) + '\n\n'))
    lbl2 = ttk.Label(window, text=(' '.join(questions[1]) + '\n\n'))
    lbl3 = ttk.Label(window, text=(' '.join(questions[2]) + '\n\n'))
    lbl4 = ttk.Label(window, text=(' '.join(questions[3]) + '\n\n'))
    lbl5 = ttk.Label(window, text=(' '.join(questions[4]) + '\n\n'))
    lbl6 = ttk.Label(window, text=(' '.join(questions[5]) + '\n\n'))
    lbl7 = ttk.Label(window, text=(' '.join(questions[6]) + '\n\n'))
    lbl8 = ttk.Label(window, text=(' '.join(questions[7]) + '\n\n'))
    lbl9 = ttk.Label(window, text=(' '.join(questions[8]) + '\n\n'))
    lbl10 = ttk.Label(window, text=(' '.join(questions[9]) + '\n\n'))
    lbl = [lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7, lbl8, lbl9, lbl10]

    ht1 = Ht(lbl1, text=all_verbs[0].translate())
    ht2 = Ht(lbl2, text=all_verbs[1].translate())
    ht3 = Ht(lbl3, text=all_verbs[2].translate())
    ht4 = Ht(lbl4, text=all_verbs[3].translate())
    ht5 = Ht(lbl5, text=all_verbs[4].translate())
    ht6 = Ht(lbl6, text=all_verbs[5].translate())
    ht7 = Ht(lbl7, text=all_verbs[6].translate())
    ht8 = Ht(lbl8, text=all_verbs[7].translate())
    ht9 = Ht(lbl9, text=all_verbs[8].translate())
    ht10 = Ht(lbl10, text=all_verbs[9].translate())

    if mode == 'present tense':
        inp11 = ttk.Entry(window)
        inp12 = ttk.Entry(window)
        inp.append(inp11)
        inp.append(inp12)

        ent11 = ttk.Button(cmw, command=all_verbs[10].func, text='Enter')
        ent12 = ttk.Button(cmw, command=all_verbs[11].func, text='Enter')
        ent.append(ent11)
        ent.append(ent12)

        lbl11 = ttk.Label(cmw, text=(' '.join(questions[10]) + '\n\n'))
        lbl12 = ttk.Label(cmw, text=(' '.join(questions[11]) + '\n\n'))
        lbl.append(lbl11)
        lbl.append(lbl12)

        ht11 = Ht(lbl11, text=all_verbs[10].translate())
        ht12 = Ht(lbl12, text=all_verbs[11].translate())

    lc_frame = ttk.Frame(window)
    lc_lbl = ttk.Label(lc_frame, text='Don\'t know ' + mode + '?')
    golc = ttk.Button(lc_frame, text='Learn', command=learn)
    lc_lbl.pack(side=LEFT)
    golc.pack(side=RIGHT)
    lc_frame.place(x=5, y=3)

    # to get to the home page or tutorials page
    gohome = ttk.Button(window, text='Home', command=home)
    golessons = ttk.Button(window, text='Lessons', command=lessons)
    gohome.place(x=5, y=330)
    golessons.place(x=83, y=330)

    y1 = 30
    for q in range(len(all_verbs)):
        lbl[q].place(x=5, y=y1)
        inp[q].place(x=85, y=y1)
        ent[q].place(x=215, y=y1-1)
        cmw.update()
        y1 += 30

    yval = 360
    if mode == 'present tense':
        yval += 60
    window.geometry('300x' + str(yval) + '+475+170')
    title = list(mode)
    title[0] = title[0].upper()
    title = ''.join(title)
    window.title(title)

    window.deiconify()
    window.mainloop()

def lcm():
        cmw.withdraw()
        lw.withdraw()
        learn = 'In Russian, some consonants "mutate" in certain verb conjugations.\n' \
                'Most commonly, this happens in -ать verbs (in every conjugation)\nand in -ить and -еть ' \
                'second conjugation verbs (in the я form only).\nSo, which consonants mutate?'
        mutants1 = 'п -> пл\nб -> бл\nф -> фл\nв -> вл*\nм -> мл*\nт -> ч*\nк -> ч'
        mutants2 = 'д -> ж*\nг -> ж*\nз -> ж\nс -> ш\nх -> ш\nст -> щ\nск -> щ'
        exception = '*Consonants with a star next to them\ndo not mutate in -ать verbs.'

        learn_lbl = ttk.Label(lcmw, text=learn)
        m_lbl1 = ttk.Label(lcmw, text=mutants1)
        m_lbl2 = ttk.Label(lcmw, text=mutants2)
        exception_lbl = ttk.Label(lcmw, text=exception)

        cm_button = ttk.Button(lcmw, text='Practice consonant mutation', command=cm)
        golessons = ttk.Button(lcmw, text='All lessons', command=lessons)
        cm_button.place(x=5,y=185)
        golessons.place(x=170,y=185)

        learn_lbl.place(x=5,y=5)
        m_lbl1.place(x=5, y=70)
        m_lbl2.place(x=70, y=70)
        exception_lbl.place(x=150, y=90)
        lcmw.geometry('380x215+435+245')
        lcmw.title('Learn consonant mutation')
        lcmw.deiconify()
        lcmw.mainloop()
def cm():
    global all_verbs
    all_verbs = []

    # 1st conj, no mutation
    read = Verb('читáть', 'чит', 'ать', 'read')
    jump = Verb('при́гать', 'приг', 'ать', 'jump')
    # 1st conj, mutation
    write = Verb('писáть', 'пис', 'ать', 'write')
    cry = Verb('плáкать', 'плак', 'ать', 'cry')
    # 1st conj, no mutation *because it's 1st conj*
    think = Verb('ду́мать', 'дум', 'ать', 'think')
    fall = Verb('пáдать', 'пад', 'ать', 'fall')

    # 2nd conj, no mutation
    speak = Verb('говори́ть', 'говор', 'ить', 'speak')
    mean = Verb('знáчить', 'знач', 'ить', 'mean')
    # 2nd conj, mutation
    prepare = Verb('готóвить', 'готов', 'ить', 'prepare')
    clean = Verb('чи́стить', 'чист', 'ить', 'clean')

    verbpractice('present', True, cmw, lcm)

def lgc():
        lw.withdraw()
        gcw.withdraw()
        learn = 'The genitive case in Russian answers the questions "of what?",\n"whose?", and "what is absent?"' \
                '(Amounts, possession, and negation).\nSo, how is it applied?'
        gen1 = 'Nouns ending in -> become:\n' \
                   'hard consonant -> ADD а \nй -> я \nь (masc) -> я \nа -> ы \nя -> и \nь (fem) -> и \nо -> а \nе -> я'
        gen2 = 'And, plural:\n' \
                   'hard consonant -> ADD ов \nй -> ев \nь (either) -> ей \nа -> drop ending* \n(vowel) я -> й\n' \
                   ' (consonant) я -> ь* \nо -> drop ending* \nие -> ий \nе -> ей\n'
        exception = '*If a noun\'s stem ends in a double consonant, an o or e will be \nadded between ' \
                    'the last two letters when the ending is dropped.'

        learn_lbl = ttk.Label(lgcw, text=learn)
        g_lbl1 = ttk.Label(lgcw, text=gen1)
        g_lbl2 = ttk.Label(lgcw, text=gen2)
        exception_lbl = ttk.Label(lgcw, text=exception)

        gc_button = ttk.Button(lgcw, text='Practice genitive case', command=gc)
        golessons = ttk.Button(lgcw, text='All lessons', command=lessons)
        gc_button.place(x=5, y=260)
        golessons.place(x=130, y=260)

        learn_lbl.place(x=5,y=5)
        g_lbl1.place(x=5, y=60)
        g_lbl2.place(x=170, y=60)
        exception_lbl.place(x=5, y=220)
        lgcw.geometry('380x290+435+205')
        lgcw.title('Learn genitive case')
        lgcw.deiconify()
        lgcw.mainloop()
def gc():
    global all_nouns
    all_nouns = []

    # initializing nouns for the questions
    # each case has different nouns which are specifically picked to illustrate special things about the case
    # (for example, кошка becoming кошек rather than кошк or кошок)

    # -a noun
    cat = Noun('кóшка', 'кошк', 'а', 'f', True, 'cat')
    # -я noun ending in vowel
    snake = Noun('змея́', 'зме', 'я́', 'f', True, 'snake')
    # -я noun ending in consonant
    kitchen = Noun('ку́хня', 'кухн', 'я', 'f', False, 'kitchen')
    # - noun (hard consonant ending)
    wolf = Noun('вóлк', 'волк', '', 'm', True, 'wolf')
    # -й noun
    tea = Noun('чáй', 'ча', 'й', 'm', False, 'tea')
    # -ь noun, masculine
    dictionary = Noun('словáрь', 'словар', 'ь', 'm', False, 'dictionary')
    # -ь noun, feminine
    door = Noun('двéрь', 'двер', 'ь', 'f', True, 'door')
    # -e noun ending in и
    room = Noun('помещéние', 'помещени', 'е', 'n', False, 'room')
    # -e noun ending in consonant
    sea = Noun('морé', 'мор', 'é', 'n', False, 'sea')
    # -o noun
    apple = Noun('я́блоко', 'яблок', 'о', 'n', False, 'apple')

    casepractice('genitive', gcw, lgc)

def lac():
    lw.withdraw()
    acw.withdraw()
    learn = 'The accusative case in Russian is applied to the object\nof a sentence- ' \
            'Something that is having an action performed on it.\nSo, how is it applied?'
    acc1 = 'Nouns ending in -> become:\n' \
           'hard consonant -> ADD а \nй -> я \nь (masc) -> я \nа -> у \nя -> ю\n' \
           'Inanimate* masculine nouns do not change. \nFeminine nouns ending in  do not change. \n' \
           'Neutral nouns do not change.'
    acc2 = 'And, plural:\n' \
           'Animate nouns use their gentive \nplural; inanimate objects use their \nnominative (regular) plural.'
    anim = '*An animate noun can think and perform actions on its own- \nsuch as a human or an animal.\n' \
           'An inanimate noun cannot- such as a plant, table, or rock.'

    learn_lbl = ttk.Label(lacw, text=learn)
    a_lbl1 = ttk.Label(lacw, text=acc1)
    a_lbl2 = ttk.Label(lacw, text=acc2)
    anim_lbl = ttk.Label(lacw, text=anim)

    def goac():
        lacw.withdraw()
        ac()

    ac_button = ttk.Button(lacw, text='Practice accusative case', command=goac)
    golessons = ttk.Button(lacw, text='All lessons', command=lessons)
    ac_button.place(x=5, y=270)
    golessons.place(x=143, y=270)

    learn_lbl.place(x=5, y=5)
    a_lbl1.place(x=5, y=65)
    a_lbl2.place(x=170, y=65)
    anim_lbl.place(x=5, y=215)
    lacw.geometry('380x300+435+200')
    lacw.title('Learn accusative case')
    lacw.deiconify()
    lacw.mainloop()
def ac():
    global all_nouns
    all_nouns = []

    # inanimate masc
    glass = Noun('стакáн', 'стакан', '', 'm', False, 'glass')
    glue = Noun('клéй', 'кле', 'й', 'm', False, 'glue')

    # animate masc
    person = Noun('человéк', 'человек', '', 'm', True, 'person')
    villian = Noun('злодéй', 'злоде', 'й', 'm', True, 'villian')
    king = Noun('корóль', 'корол', 'ь', 'm', True, 'king')

    # fem
    book = Noun('кни́га', 'книиг', 'а', 'f', False, 'book')
    apple_tree = Noun('я́блоня', 'яблон', 'я', 'f', False, 'apple tree')
    bear = Noun('мéдведь', 'медвед', 'ь', 'f', True, 'bear')

    # neu
    heart = Noun('сéрдце', 'сердц', 'е', 'n', False, 'heart')
    window = Noun('окнó', 'окн', 'ó', 'n', False, 'window')

    casepractice('accusative', acw, lac)

def lpc():
    lw.withdraw()
    pcw.withdraw()
    learn = 'The prepositional case in Russian is used to indicate position,\nwith the prepositions ' \
            'в, на, and о (in/at, on/at, and about).\nSo, how is it applied?'
    prep1 = 'Nouns ending in -> become:\n' \
           'hard consonant -> ADD e \nь (fem) -> и \nия -> ии \nие -> ии \nall other nouns -> e'
    prep2 = 'And, plural:\n' \
           'hard consonant, a, o -> ах \nall other nouns -> ях'

    learn_lbl = ttk.Label(lpcw, text=learn)
    p_lbl1 = ttk.Label(lpcw, text=prep1)
    p_lbl2 = ttk.Label(lpcw, text=prep2)

    pc_button = ttk.Button(lpcw, text='Practice prepositional case', command=pc)
    golessons = ttk.Button(lpcw, text='All lessons', command=lessons)
    pc_button.place(x=5, y=160)
    golessons.place(x=160, y=160)

    learn_lbl.place(x=5, y=5)
    p_lbl1.place(x=5, y=60)
    p_lbl2.place(x=170, y=60)
    lpcw.geometry('380x190+435+255')
    lpcw.title('Learn prepositional case')
    lpcw.deiconify()
    lpcw.mainloop()
def pc():
    global all_nouns
    all_nouns = []

    # -a noun
    street = Noun('у́лица', 'улиц', 'а', 'f', False, 'street')
    # -ия noun
    station = Noun('стáнция', 'станци', 'я', 'f', False, 'station')
    # -я noun
    family = Noun('семья́', 'семь', 'я́', 'f', True, 'family')
    # - noun (hard consonant ending)
    store = Noun('магази́н', 'магазин', '', 'm', False, 'store')
    # -й noun
    museum = Noun('музéй', 'музе', 'й', 'm', False, 'museum')
    # -ь noun, masculine
    horse = Noun('кóнь', 'кон', 'ь', 'm', False, 'horse')
    # -ь noun, feminine
    church = Noun('цéрковь', 'церков', 'ь', 'f', False, 'church')
    # -e noun ending in и
    building = Noun('здáние', 'здани', 'е', 'n', False, 'building')
    # -e noun ending in consonant
    sun = Noun('сóлнце', 'солнц', 'е', 'n', False, 'sun')
    # -o noun
    place = Noun('мéсто', 'мест', 'о', 'n', False, 'place')

    casepractice('prepositional', pcw, lpc)

def ldc():
    lw.withdraw()
    dcw.withdraw()
    learn = 'The dative case in Russian is used to refer to the indirect object,\nof a sentence. ' \
            '(ex: "I sent her a letter"- "letter" is the direct object, \n"her" is the indirect object.)\n' \
            'It is also used fot most applications of the prepostion по; with verbs \nпомогать and советовать ' \
            '(to help and to advise: you give \nhelp/advice); with нравиться (to like) and similar verbs; and ' \
            'with \nнужен (to need)- in the last two, what you\'d expect to be the subject \nis in the dative. ' \
            'So, how is it applied?'
    dat1 = 'Nouns ending in -> become:\n' \
           'hard consonant -> ADD у \nй -> ю \nь (masc) -> ю \nа -> е \nя -> е \nия -> ие'
    dat2 = 'ь (fem) -> и \nо -> у \nе -> ю'
    dat3 = 'And, plural:\n' \
           'hard consonant, a, o -> ам \nall other nouns -> ям'

    learn_lbl = ttk.Label(ldcw, text=learn)
    d_lbl1 = ttk.Label(ldcw, text=dat1)
    d_lbl2 = ttk.Label(ldcw, text=dat2)
    d_lbl3 = ttk.Label(ldcw, text=dat3)

    dc_button = ttk.Button(ldcw, text='Practice dative case', command=dc)
    golessons = ttk.Button(ldcw, text='All lessons', command=lessons)
    dc_button.place(x=5, y=250)
    golessons.place(x=120, y=250)

    learn_lbl.place(x=5, y=5)
    d_lbl1.place(x=5, y=135)
    d_lbl2.place(x=67, y=194)
    d_lbl3.place(x=180, y=135)
    ldcw.geometry('380x280+435+210')
    ldcw.title('Learn dative case')
    ldcw.deiconify()
    ldcw.mainloop()
def dc():
    global all_nouns
    all_nouns = []

    # m
    student = Noun('учени́к', 'ученик', '', 'm', True, 'student')
    shed = Noun('сарáй', 'сара', 'й', 'm', False, 'shed')
    guy = Noun('пáрень', 'парен', 'ь', 'm', True, 'guy')

    # f
    head = Noun('головá', 'голов', 'á', 'f', False, 'head')
    earth = Noun('земля́', 'земл', 'я́', 'f', False, 'earth')
    life = Noun('жни́зь', 'жниз', 'ь', 'f', False, 'life')

    # -ия
    party = Noun('пáртия', 'парти', 'я', 'f', False, 'party')

    # n
    happiness = Noun('счáстье', 'счасть', 'е', 'n', False, 'happiness')
    attitude = Noun('отношéние', 'отношени', 'е', 'n', False, 'attitude')
    face = Noun('лицó', 'лиц', 'ó', 'n', False, 'face')

    casepractice('dative', dcw, ldc)

def lic():
    lw.withdraw()
    icw.withdraw()
    learn = 'The instrumental case in Russian is used to indicate the concepts \nwith, by, and by means of. \n' \
            'It is also used with some prepositions (за, над, под, перед, между), \nto indicate season or part of ' \
            'day (утром = in the morning), and with \nбыл (was) & быть (will be). \n' \
            'So, how is it applied?'
    in1 = 'Nouns ending in -> become:\n' \
           'hard consonant -> ADD ом \nй -> ем \nь (masc) -> ем \nа -> ой \nя -> ей \nь (fem) -> ью \nо/e -> ADD м'
    in2 = 'And, plural:\n' \
           'hard consonant, a, o -> ами \nall other nouns -> ями'

    learn_lbl = ttk.Label(licw, text=learn)
    i_lbl1 = ttk.Label(licw, text=in1)
    i_lbl2 = ttk.Label(licw, text=in2)

    ic_button = ttk.Button(licw, text='Practice instrumental case', command=ic)
    golessons = ttk.Button(licw, text='All lessons', command=lessons)
    ic_button.place(x=5, y=240)
    golessons.place(x=155, y=240)

    learn_lbl.place(x=5, y=5)
    i_lbl1.place(x=5, y=105)
    i_lbl2.place(x=180, y=105)
    licw.geometry('380x270+435+215')
    licw.title('Learn instrumental case')
    licw.deiconify()
    licw.mainloop()
def ic():
    global all_nouns
    all_nouns = []

    # m
    sugar = Noun('сáхар', 'сахар', '', 'm', False, 'sugar')
    comrade = Noun('товáрищ', 'товарищ', '', 'm', True, 'comrade')
    sparrow = Noun('воробéй', 'воробе', 'й', 'm', True, 'sparrow')
    shampoo = Noun('шампу́нь', 'шампун', 'ь', 'm', False, 'shampoo')

    # f
    pen = Noun('ру́чка', 'ручк', 'а', 'f', False, 'pen')
    story = Noun('истóрия', 'истори', 'я', 'f', False, 'story')
    week = Noun('недéля', 'недел', 'я', 'f', False, 'week')
    autumn = Noun('óсень', 'осен', 'ь', 'f', False, 'autumn')

    # n
    movement = Noun('движéние', 'движени', 'е', 'n', False, 'movement')
    morning = Noun('у́тро', 'утр', 'о', 'n', False, 'morning')

    casepractice('instrumental', icw, lic)

def lprt():
    lw.withdraw()
    prtw.withdraw()
    learn1 = 'Verbs are conjugated in many different ways in the present tense.\n' \
            'First, there are two conjugation groups:'
    firstconj1 = '1st conjugation: \nя ___ю \nты ___ешь \nон ___ет'
    firstconj2 = 'мы ___ем \nвы ___ете \nони ___ют'
    secondconj1 = '2nd conjugation: \nя ___ю \nты ___ишь \nон ___ит'
    secondconj2 = 'мы ___им \nвы ___ите \nони ___ят'
    learn2 = 'Most verbs with the ending -ить are in the second conjugation,\nwhile most verbs ' \
             'with ending -ать and -еть are in the first. \nThere are some exceptions, but they ' \
             'won\'t be included in this exercise. \nOtherwise, all verbs are in the first conjugation. ' \
             '\n\nVerbs with different endings change differently from their infinitive ' \
             '\nto conjugated form.'

    keep_vowel_l = 'Some verbs keep the vowel \nin their ending:'
    keep_vowel = '-ать \n-ять \n-еть'
    keep_vowel_ex = 'читать -> читаю \nгулять -> гуляю \nсметь -> смею'

    mut_vowel_l = 'While others have mutating vowels:'
    mut_vowel = '-авать \n-овать \n-евать \n-ыть'
    mut_vowel_ex = 'давать -> даю \nцеловать -> целую \nтанцевать -> танцую \nоткрыть -> открою'

    drop_vowel_l = 'Some drop the vowel:'
    drop_vowel = '-ить \n-оть \n-ать* \n* after consonant mutation'
    drop_vowel_ex = 'говорить -> говорю \nколоть -> колю \nплакать -> плачу'

    mut_n_l = 'Some mutate their last consonant to н:'
    mut_n = '-стать \n-деть \nThese use у rather than ю \nin я & они forms.'
    mut_n_ex = 'встать -> встану \nнадеть -> надену'

    nyat_l = 'Then, there\'s -нять verbs... '
    nyat = '-инять -> -им \n-[other vowel]нять -> -[other vowel]йм ' \
           '\n-[consonant]нять -> -[consonant]ним \nLike н verbs, these use у instead of ю.'
    nyat_ex = 'принять -> приму \nпонять -> пойму \nподнять -> подниму'

    eret_l = 'And finally, -ереть:'
    eret = '-ереть -> р \n...which also uses у.'
    eret_ex = 'тереть -> тру'

    learn_lbl1 = ttk.Label(lprtw, text=learn1)
    f_lbl1 = ttk.Label(lprtw, text=firstconj1)
    f_lbl2 = ttk.Label(lprtw, text=firstconj2)
    s_lbl1 = ttk.Label(lprtw, text=secondconj1)
    s_lbl2 = ttk.Label(lprtw, text=secondconj2)
    learn_lbl2 = ttk.Label(lprtw, text=learn2)

    keep_lbl1 = ttk.Label(lprtw, text=keep_vowel_l)
    keep_lbl2 = ttk.Label(lprtw, text=keep_vowel)
    keep_lbl3 = ttk.Label(lprtw, text=keep_vowel_ex)

    mutv_lbl1 = ttk.Label(lprtw, text=mut_vowel_l)
    mutv_lbl2 = ttk.Label(lprtw, text=mut_vowel)
    mutv_lbl3 = ttk.Label(lprtw, text=mut_vowel_ex)

    drop_lbl1 = ttk.Label(lprtw, text=drop_vowel_l)
    drop_lbl2 = ttk.Label(lprtw, text=drop_vowel)
    drop_lbl3 = ttk.Label(lprtw, text=drop_vowel_ex)

    mutn_lbl1 = ttk.Label(lprtw, text=mut_n_l)
    mutn_lbl2 = ttk.Label(lprtw, text=mut_n)
    mutn_lbl3 = ttk.Label(lprtw, text=mut_n_ex)

    nyat_lbl1 = ttk.Label(lprtw, text=nyat_l)
    nyat_lbl2 = ttk.Label(lprtw, text=nyat)
    nyat_lbl3 = ttk.Label(lprtw, text=nyat_ex)

    eret_lbl1 = ttk.Label(lprtw, text=eret_l)
    eret_lbl2 = ttk.Label(lprtw, text=eret)
    eret_lbl3 = ttk.Label(lprtw, text=eret_ex)

    prt_button = ttk.Button(lprtw, text='Practice present tense', command=prt)
    golessons = ttk.Button(lprtw, text='All lessons', command=lessons)

    learn_lbl1.place(x=5, y=5)
    f_lbl1.place(x=5, y=40)
    f_lbl2.place(x=70, y=55)
    s_lbl1.place(x=150, y=40)
    s_lbl2.place(x=215, y=55)
    learn_lbl2.place(x=5, y=105)

    keep_lbl1.place(x=5, y=215)
    keep_lbl2.place(x=5 , y=247)
    keep_lbl3.place(x=40, y=247)

    mutv_lbl1.place(x=165, y=215)
    mutv_lbl2.place(x=165, y=232)
    mutv_lbl3.place(x=210, y=232)

    drop_lbl1.place(x=5, y=300)
    drop_lbl2.place(x=5, y=317)
    drop_lbl3.place(x=40, y=317)

    mutn_lbl1.place(x=165, y=300)
    mutn_lbl2.place(x=165, y=317)
    mutn_lbl3.place(x=210, y=317)

    nyat_lbl1.place(x=5, y=385)
    nyat_lbl2.place(x=5, y=402)
    nyat_lbl3.place(x=228, y=402)

    eret_lbl1.place(x=5, y=470)
    eret_lbl2.place(x=5, y=487)
    eret_lbl3.place(x=80, y=487)

    prt_button.place(x=5, y=525)
    golessons.place(x=132, y=525)

    lprtw.geometry('380x560+435+70')
    lprtw.title('Learn present tense')
    lprtw.deiconify()
    lprtw.mainloop()
def prt():
    global all_verbs
    all_verbs = []

    # 1st conj
    do = Verb('дéлать', 'дел', 'ать', 'do')
    stroll = Verb('гуля́ть', 'гул', 'ять', 'stroll')
    have = Verb('имéть', 'им', 'еть', 'have')
    split = Verb('колóть', 'кол', 'оть', 'split')

    # 2nd conj
    phone = Verb('звони́ть', 'звон', 'ить', 'phone')

    # special 1st conj
    give = Verb('давáть', 'д', 'авать', 'give')
    dance = Verb('танцевáть', 'танц', 'евать', 'dance')
    wash = Verb('мы́ть', 'м', 'ыть', 'wash')
    become = Verb('стáть', '', 'стать', 'become')
    put_on = Verb('надéть', 'на', 'деть', 'put on')
    accept = Verb('приня́ть', 'при', 'нять', 'accept')
    die = Verb('умéреть', 'ум', 'ереть', 'die')

    verbpractice('present', False, prtw, lprt)

def lpat():
    lw.withdraw()
    patw.withdraw()
    learn1 = 'The past tense in Russian is formed according to gender of the subject. \nThe ending (-ть) is removed,' \
             'and one of these endings is added: '
    endings = 'masculine (он): -л \nfeminine (она): -ла \nneutral (оно): -ло \nplural (мы, вы, они): -ли'
    example1 = 'желать -> желал'
    example2 = '-> желала \n-> желало \n-> желали'
    learn2 = 'In я and ты forms, the verb still changes according to the gender of the \nsubject (the person ' \
             'performing the action). \nNotably, вы form always uses plural, even to refer to only one person.'
    learn3 = 'None of the special first conjugation rules apply (нять, ыть, е/овать, etc). \nJust change the ending ' \
             'as shown- EXCEPT for -ереть verbs, in which you \nalso remove the second e and don\'t add л, so that ' \
             'you have \nthe verb stem + ер, ера, еро, ери.'

    learn_lbl1 = ttk.Label(lpatw, text=learn1)
    endings_lbl = ttk.Label(lpatw, text=endings)
    example_lbl1 = ttk.Label(lpatw, text=example1)
    example_lbl2 = ttk.Label(lpatw, text=example2)
    learn_lbl2 = ttk.Label(lpatw, text=learn2)
    learn_lbl3 = ttk.Label(lpatw, text=learn3)

    pat_button = ttk.Button(lpatw, text='Practice past tense', command=pat)
    golessons = ttk.Button(lpatw, text='All lessons', command=lessons)

    learn_lbl1.place(x=5, y=5)
    endings_lbl.place(x=5, y=40)
    example_lbl1.place(x=145, y=40)
    example_lbl2.place(x=187, y=55)
    learn_lbl2.place(x=5, y=110)
    learn_lbl3.place(x=5, y=162)

    pat_button.place(x=5, y=230)
    golessons.place(x=115, y=230)

    lpatw.title('Learn past tense')
    lpatw.geometry('400x260+425+225')
    lpatw.deiconify()
    lpatw.mainloop()
def pat():
    global all_verbs
    all_verbs = []

    # 1st conj
    know = Verb('знáть', 'зн', 'ать', 'knew')
    stand = Verb('стóять', 'сто', 'ять', 'stood')
    sing = Verb('пéть', 'п', 'еть', 'sang')

    # 2nd conj
    ask = Verb('спрóсить', 'спрос', 'ить', 'asked')
    drink = Verb('вы́пить', 'вып', 'ить', 'drank')

    # special 1st conj
    give_back = Verb('отдавáть', 'отд', 'авать', 'gave back')
    kiss = Verb('целовáть', 'цел', 'овать', 'kissed')
    forget = Verb('забы́ть', 'заб', 'ыть', 'forgot')
    reach = Verb('достáть', 'до', 'стать', 'reached')
    understand = Verb('пóнять', 'по', 'нять', 'understood')

    verbpractice('past', False, patw, lpat)

home()
