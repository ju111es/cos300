
from tkinter import *
from tkinter import ttk
import random as rnd
from idlelib.tooltip import Hovertip as Ht

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


class Noun:
    def __init__(self, noun, nom_stem, nom_end, gender, animate, qlist, inplist):
        self.noun = noun
        self.gender = gender
        self.animate = animate
        self.nom_stem = nom_stem
        self.nom_end = nom_end
        self.qlist = qlist
        self.inplist = inplist

        global all_nouns
        all_nouns.append(self)

        self.g = [[self.nom_stem], [self.nom_stem]]
        self.a = [[self.nom_stem], [self.nom_stem]]
        self.p = [[self.nom_stem], [self.nom_stem]]
        self.d = [[self.nom_stem], [self.nom_stem]]
        self.i = [[self.nom_stem], [self.nom_stem]]
        self.plural = self.nom_stem
        # letters stand for genitive, accusative, prepositional, dative, and instrumental (cases).
        # nouns have different endings in each case depending on the letter they end in,
        # as well as different plural endings in both the nominative (default) case and others.
        # in the accusative case, it is relevant whether the noun is animate or not.
        # it is also sometimes relevant where the word is stressed. i'm still figuring out how to incorporate this.
        self.assign_cases()

    def assign_cases(self):
        if self.nom_end == 'а':
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
            self.a[0].append('y')
            self.p[0].append('е')
            self.p[1].append('ах')
            self.d[0].append('е')
            self.d[1].append('ам')

        elif self.nom_end == 'я':
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
            self.i[0].append('ей')
            self.p[1].append('ях')
            self.d[1].append('ям')
            self.i[1].append('ями')

        elif self.nom_end == '':
            self.plural = self.plural + 'ы'
            self.a[0].append('a')
            self.g[0].append('a')
            if self.nom_end == 'ж' or self.nom_end == 'ч' or self.nom_end == 'ш' or self.nom_end == 'щ':
                self.g[1].append('ев')
            else:
                self.g[1].append('ов')
            self.p[0].append('е')
            self.p[1].append('ах')
            self.d[0].append('y')
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

        elif self.nom_end == 'о':
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

        elif self.nom_end == 'е':
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

        # some vowels (ы, ю, я, sometimes o) can't follow certain consonants.
        if self.nom_stem[-1] in ilist:
            self.plural = self.plural.replace('ы', 'и')
            self.g[0][1] = self.g[0][1].replace('ы', 'и')
        if self.nom_stem[-1] in ylist:
            self.d[0][1] = self.d[0][1].replace('ю', 'у')
        if self.nom_stem[-1] in alist:
            self.g[0][1] = self.g[0][1].replace('я', 'а')
            self.a[0][1] = self.a[0][1].replace('я', 'а')
            self.p[1][1] = self.p[1][1].replace('я', 'а')
            self.d[1][1] = self.d[1][1].replace('я', 'а')
            self.i[1][1] = self.i[1][1].replace('я', 'а')

        if self.animate is True:
            self.a[1] = self.g[1]
        else:
            self.a[1].append(self.plural[-1])
            if self.gender == 'm':
                self.a[0][1] = self.nom_end

    def print_cases(self):
        print(self.noun, 'in all 6 cases:')
        print('Nominative:', self.noun, self.plural, end='  ')
        print('Genitive:', ''.join(self.g[0]), ''.join(self.g[1]))
        print('Accusative:', ''.join(self.a[0]), ''.join(self.a[1]), end='  ')
        print('Prepositional:', ''.join(self.p[0]), ''.join(self.p[1]))
        print('Dative:', ''.join(self.d[0]), ''.join(self.d[1]), end='  ')
        print('Instrumental:', ''.join(self.i[0]), ''.join(self.i[1]))
        print('\n')

    def gcase_check(self):
        form = self.qlist[all_nouns.index(self)]
        if form == self.plural:
            a = ''.join(self.g[1])
        else:
            a = ''.join(self.g[0])
        i = self.inplist[all_nouns.index(self)].get()

        nw = Tk()
        if i != a:
            nominative = i == self.noun or i == self.plural
            accusative = i == ''.join(self.a[0]) or i == ''.join(self.a[1])
            prepositional = i == ''.join(self.p[0]) or i == ''.join(self.p[1])
            dative = i == ''.join(self.d[0]) or i == ''.join(self.d[1])
            instrumental = i == ''.join(self.i[0]) or i == ''.join(self.i[1])
            print(i == ''.join(self.p[0]))
            print(''.join(self.p[0]))
            if nominative or accusative or prepositional or dative or instrumental:
                correction = ttk.Label(nw, text='It looks like you applied the wrong case.'
                                                '\nIf you need a refresher on the genitive case, click Learn.')
            elif i == self.nom_stem or i == self.nom_stem + 'ь' and i != self.g[1][1]:
                correction = ttk.Label(nw, text='Usually o or e is added to a stem ending in a double consonant.'
                                                '\nIf you need a refresher on the genitive case, click Learn.')
            else:
                correction = ttk.Label(nw, text='Incorrect...')
        else:
            correction = ttk.Label(nw, text='Correct!')
        correction.place(x=8, y=8)
        nw.minsize(350, 50)
        nw.maxsize(350, 50)
        nw.mainloop()

class Verb:

    def __init__(self, verb, stem, ending, qlist, inplist):
        self.verb = verb
        self.stem = stem
        self.ending = ending
        self.qlist = qlist
        self.inplist = inplist

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
            if self.i[-1][-1] in ylist:
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
            if self.i[-1][-1] in ylist:
                self.i.append('у')
            else:
                self.i.append('ю')
            if self.they[-1][-1] in alist:
                self.they.append('ат')
            else:
                self.they.append('ят')

        for item in self.conjs:
            self.conjs[self.conjs.index(item)] = ''.join(item)

    def find_mutation(self):
        # some consonants 'mutate' in certain verb conjugations. this function predicts when they will.

        mutants = ['п', 'б', 'ф', 'м', 'в', 'к', 'т', 'д', 'з', 'г', 'с', 'х']
        lc = self.stem[-1]  # last consonant
        if self.ending == 'ать' or self.ending == 'ить' and lc in mutants:
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
                    self.mutStem = self.stem.replace('с' + lc, 'щ')
                    return True
                elif lc == 'т' and self.ending == 'ать':
                    self.mutStem = self.stem.replace(lc, 'ч')
                    return False
                else:
                    self.mutStem = self.stem.replace(lc, 'ч')
                    return True
            elif lc == 'д' or lc == 'з' or lc == 'г':
                if lc == 'г' or lc == 'д' and self.ending == 'ать':
                    self.mutStem = self.stem.replace(lc, 'ж')
                    return False
                else:
                    self.mutStem = self.stem.replace(lc, 'ж')
                    return True
            elif lc == 'с' or lc == 'х':
                self.mutStem = self.stem.replace(lc, 'ш')
                return True
        else:
            return False

    def print_conjs(self):
        print(self.verb, 'conjugation:\n' + str(self.conjs), '\n')

    def cm_check(self):

        # if someone uses the wrong letter, not applying consonant mutation or applying it where they shouldn't,
        # this will recognize and explain their mistake.

        pronoun = self.qlist[all_verbs.index(self)][0]
        pronouns = list(pronounsn.keys())
        pronouns.pop(pronouns.index('она'))
        pronouns.pop(pronouns.index('оно'))
        if pronoun == 'она' or pronoun == 'оно':
            pronoun_index = pronouns.index('он')
        else:
            pronoun_index = pronouns.index(pronoun)
        a = self.conjs[pronoun_index]

        i = self.inplist[all_verbs.index(self)].get()

        nw = Tk()
        if i != a:
            try:
                if self.mutStem != None and self.stem in i:
                    correction = ttk.Label(nw,
                        text='This is an instance of consonant mutation. \nIf you need a refresher on how it works, click Learn.')
                elif self.mutStem != None and self.mutStem in i and self.find_mutation() is False:
                    correction = ttk.Label(nw,
                        text='This is NOT an instance of consonant mutation. \nIf you need a refresher on how it works, click Learn.')
                else:
                    correction = ttk.Label(nw, text='Incorrect...')
            except AttributeError:
                correction = ttk.Label(nw, text='Incorrect...')
        else:
            correction = ttk.Label(nw, text='Correct!')
        correction.place(x=8, y=8)
        nw.minsize(290, 50)
        nw.maxsize(290, 50)
        nw.mainloop()

    def present_check(self):
        pass

    def past_check(self):
        pass

class VerbPair(Verb):
    def __init__(self, Verb1, Verb2):
        pass


mw = Tk()
def mainsetup():
    greeting = ttk.Label(mw, text='Welcome! What would you like to practice?')
    gocm = ttk.Button(mw, text='Consonant Mutation', command=cm)
    gogc = ttk.Button(mw, text='Genitive Case', command=gc)
    goac = ttk.Button(mw, text='Accusative Case', command=acsetup)
    gopc = ttk.Button(mw, text='Prepositional Case', command=pcsetup)
    godc = ttk.Button(mw, text='Dative Case', command=dcsetup)
    goic = ttk.Button(mw, text='Instrumental Case', command=icsetup)

    gocm.place(x=135,y=50)
    gogc.place(x=20,y=50)
    goac.place(x=20,y=80)
    gopc.place(x=20,y=110)
    godc.place(x=20,y=140)
    goic.place(x=20,y=170)
    greeting.place(x=20,y=18)
    mw.minsize(280,210)
    mw.title('Home')
    mw.mainloop()

def cm():
    # setting up window
    mw.destroy()
    cmw = Tk()

    # tutorial explaining how to use, user can just close it once they've read it
    tutw = Tk()
    tut = 'Enter just the conjugation of the verb\naccording to the pronoun in front of it\n' \
          'and press Enter.\n(Don\'t enter the pronoun, or it won\'t\nwork correctly! ' \
          'Just the verb.)\n\nSome of these conjugations will have\nconsonant mutation, some won\'t.'
    tut_lbl = ttk.Label(tutw, text=tut)
    tut_lbl.place(x=5, y=5)
    tutw.minsize(220, 135)
    tutw.maxsize(220, 135)
    tutw.title('Tutorial')

    # in case someone doesn't know the subject yet or needs a refresher,
    # they can open a window anytime with a concise explanation.
    # it's probably more useful as a refresher for someone who has already learned it;
    # i might make it more informative once more of the modes are fully functional.

    def lcm():
        lcmw = Tk()
        learn = 'Consonant Mutation\n\nIn Russian, some consonants "mutate" in certain verb conjugations.\n' \
                'Most commonly, this happens in -ать verbs (in every conjugation)\nand in -ить and -еть ' \
                'second conjugation verbs (in the я form only).\nSo, which consonants mutate?'
        mutants1 = 'п -> пл\nб -> бл\nф -> фл\nв -> вл*\nм -> мл*\nт -> ч*\nк -> ч'
        mutants2 = 'д -> ж*\nг -> ж*\nз -> ж\nс -> ш\nх -> ш\nст -> щ\nск -> щ'
        exception = '*Consonants with a star next to them\ndo not mutate in -ать verbs.'
        learn_lbl = ttk.Label(lcmw, text=learn)
        m_lbl1 = ttk.Label(lcmw, text=mutants1)
        m_lbl2 = ttk.Label(lcmw, text=mutants2)
        exception_lbl = ttk.Label(lcmw, text=exception)
        learn_lbl.place(x=5,y=5)
        m_lbl1.place(x=5, y=100)
        m_lbl2.place(x=70, y=100)
        exception_lbl.place(x=150, y=120)
        lcmw.minsize(380,215)
        lcmw.maxsize(380,215)
        lcmw.title('Learn consonant mutation')

    lcm_lbl = ttk.Label(cmw, text='Don\'t know consonant mutation?')
    golcm = ttk.Button(cmw, text='Learn', command=lcm)

    inp1 = ttk.Entry(cmw)
    inp2 = ttk.Entry(cmw)
    inp3 = ttk.Entry(cmw)
    inp4 = ttk.Entry(cmw)
    inp5 = ttk.Entry(cmw)
    inp6 = ttk.Entry(cmw)
    inp7 = ttk.Entry(cmw)
    inp8 = ttk.Entry(cmw)
    inp9 = ttk.Entry(cmw)
    inp10 = ttk.Entry(cmw)
    inp = [inp1, inp2, inp3, inp4, inp5, inp6, inp7, inp8, inp9, inp10]

    questions = []
    # initializing verbs for the questions

    # 1st conj, no mutation
    read = Verb('читать', 'чит', 'ать', questions, inp)
    jump = Verb('пригать', 'приг', 'ать', questions, inp)
    # 1st conj, mutation
    write = Verb('писать', 'пис', 'ать', questions, inp)
    cry = Verb('плакать', 'плак', 'ать', questions, inp)
    # 1st conj, no mutation *because it's 1st conj*
    think = Verb('думать', 'дум', 'ать', questions, inp)
    fall = Verb('падать', 'пад', 'ать', questions, inp)

    # 2nd conj, no mutation
    speak = Verb('говорить', 'говор', 'ить', questions, inp)
    mean = Verb('значить', 'знач', 'ить', questions, inp)
    # 2nd conj, mutation
    prepare = Verb('готовить', 'готов', 'ить', questions, inp)
    clean = Verb('чистить', 'чист', 'ить', questions, inp)

    global all_verbs
    pronouns = list(pronounsn.keys())
    for a in range(len(all_verbs)):
        q = []
        q.append(pronouns[rnd.randint(0,len(pronouns)-1)])
        q.append(all_verbs[a].verb)
        questions.append(q)

    ent1 = ttk.Button(cmw, command=all_verbs[0].cm_check,text='Enter')
    ent2 = ttk.Button(cmw, command=all_verbs[1].cm_check,text='Enter')
    ent3 = ttk.Button(cmw, command=all_verbs[2].cm_check,text='Enter')
    ent4 = ttk.Button(cmw, command=all_verbs[3].cm_check,text='Enter')
    ent5 = ttk.Button(cmw, command=all_verbs[4].cm_check,text='Enter')
    ent6 = ttk.Button(cmw, command=all_verbs[5].cm_check,text='Enter')
    ent7 = ttk.Button(cmw, command=all_verbs[6].cm_check,text='Enter')
    ent8 = ttk.Button(cmw, command=all_verbs[7].cm_check,text='Enter')
    ent9 = ttk.Button(cmw, command=all_verbs[8].cm_check,text='Enter')
    ent10 = ttk.Button(cmw, command=all_verbs[9].cm_check,text='Enter')
    ent = [ent1, ent2, ent3, ent4, ent5, ent6, ent7, ent8, ent9, ent10]

    lbl1 = ttk.Label(cmw, text=(' '.join(questions[0]) + '\n\n'))
    lbl2 = ttk.Label(cmw, text=(' '.join(questions[1]) + '\n\n'))
    lbl3 = ttk.Label(cmw, text=(' '.join(questions[2]) + '\n\n'))
    lbl4 = ttk.Label(cmw, text=(' '.join(questions[3]) + '\n\n'))
    lbl5 = ttk.Label(cmw, text=(' '.join(questions[4]) + '\n\n'))
    lbl6 = ttk.Label(cmw, text=(' '.join(questions[5]) + '\n\n'))
    lbl7 = ttk.Label(cmw, text=(' '.join(questions[6]) + '\n\n'))
    lbl8 = ttk.Label(cmw, text=(' '.join(questions[7]) + '\n\n'))
    lbl9 = ttk.Label(cmw, text=(' '.join(questions[8]) + '\n\n'))
    lbl10 = ttk.Label(cmw, text=(' '.join(questions[9]) + '\n\n'))
    lbl = [lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7, lbl8, lbl9, lbl10]

    lcm_lbl.place(x=5, y=1)
    golcm.place(x=190, y=1)
    cmw.minsize(300, 330)
    cmw.title('Consonant mutation')

    y1 = 30
    for q in range(10):
        lbl[q].place(x=5, y=y1)
        inp[q].place(x=85, y=y1)
        ent[q].place(x=215, y=y1-1)
        cmw.update()
        y1 += 30

    tutw.mainloop()
    cmw.mainloop()
    all_verbs = []

def gc():
    mw.destroy()
    gcw = Tk()

    tutw = Tk()
    tut = 'Enter the genitive form of the given\nnominative noun. There are singular\nand plural nouns given-\n' \
          'enter the genitive form matching the\ngiven nominative form.'
    tut_lbl = ttk.Label(tutw, text=tut)
    tut_lbl.place(x=5, y=5)
    tutw.minsize(220, 100)
    tutw.maxsize(220, 100)
    tutw.title('Tutorial')

    def lgc():
        lgcw = Tk()
        learn = 'The genitive case in Russian answers the questions "of what?",\n"whose?", and "what is absent?"' \
                '(Amounts, possession, and negation).\nSo, how is it applied?'
        gen1 = 'Nouns ending in -> become:\n' \
                   'hard consonant -> ADD а \nй -> я \nь (masc) -> я \nа -> ы \nя -> и \nь (fem) -> и \nо -> а \nе -> я'
        gen2 = 'And, plural:\n' \
                   'hard consonant -> ADD ов \nй -> ев \nь (either) -> ей \nа -> drop ending* \n(vowel) я -> й\n' \
                   ' (consonant) я -> ь* \nо -> drop ending* \nие -> ий \nе -> ей\n'
        exception = '*If a noun\'s stem ends in a double consonant,\nan o or e will be added between' \
                    'the last\ntwo letters when the ending is dropped.'
        learn_lbl = ttk.Label(lgcw, text=learn)
        g_lbl1 = ttk.Label(lgcw, text=gen1)
        g_lbl2 = ttk.Label(lgcw, text=gen2)
        exception_lbl = ttk.Label(lgcw, text=exception)
        learn_lbl.place(x=5,y=5)
        g_lbl1.place(x=5, y=65)
        g_lbl2.place(x=170, y=65)
        exception_lbl.place(x=5, y=225)
        lgcw.minsize(380,280)
        lgcw.maxsize(380,280)
        lgcw.title('Learn genitive case')
        lgcw.mainloop()

    lgc_lbl = ttk.Label(gcw, text='Don\'t know the genitive case?')
    golgc = ttk.Button(gcw, text='Learn', command=lgc)

    inp1 = ttk.Entry(gcw)
    inp2 = ttk.Entry(gcw)
    inp3 = ttk.Entry(gcw)
    inp4 = ttk.Entry(gcw)
    inp5 = ttk.Entry(gcw)
    inp6 = ttk.Entry(gcw)
    inp7 = ttk.Entry(gcw)
    inp8 = ttk.Entry(gcw)
    inp9 = ttk.Entry(gcw)
    inp10 = ttk.Entry(gcw)
    inp = [inp1, inp2, inp3, inp4, inp5, inp6, inp7, inp8, inp9, inp10]

    questions = []

    # -a noun
    cat = Noun('кошка', 'кошк', 'а', 'f', True, questions, inp)
    # -я noun ending in vowel
    snake = Noun('змея', 'зме', 'я', 'f', True, questions, inp)
    # -я noun ending in consonant
    kitchen = Noun('кухня', 'кухн', 'я', 'f', False, questions, inp)
    # - noun (hard consonant ending)
    train = Noun('поезд', 'поезд', '', 'm', False, questions, inp)
    # -й noun
    tea = Noun('чай', 'ча', 'й', 'm', False, questions, inp)
    # -ь noun, masculine
    dictionary = Noun('словарь', 'словар', 'ь', 'm', False, questions, inp)
    # -ь noun, feminine
    church = Noun('церковь', 'церков', 'ь', 'f', False, questions, inp)
    # -e noun ending in и
    room = Noun('помещение', 'помещени', 'е', 'n', False, questions, inp)
    # -e noun ending in consonant
    sea = Noun('море', 'мор', 'е', 'n', False, questions, inp)
    # -o noun
    apple = Noun('яблоко', 'яблок', 'о', 'n', False, questions, inp)

    global all_nouns
    for item in all_nouns:
        item.print_cases()

    for i in range(len(all_nouns)):
        p = rnd.randint(0,1)
        if p == 0:
            questions.append(all_nouns[i].noun)
        else:
            questions.append(all_nouns[i].plural)

    ent1 = ttk.Button(gcw, command=all_nouns[0].gcase_check, text='Enter')
    ent2 = ttk.Button(gcw, command=all_nouns[1].gcase_check, text='Enter')
    ent3 = ttk.Button(gcw, command=all_nouns[2].gcase_check, text='Enter')
    ent4 = ttk.Button(gcw, command=all_nouns[3].gcase_check, text='Enter')
    ent5 = ttk.Button(gcw, command=all_nouns[4].gcase_check, text='Enter')
    ent6 = ttk.Button(gcw, command=all_nouns[5].gcase_check, text='Enter')
    ent7 = ttk.Button(gcw, command=all_nouns[6].gcase_check, text='Enter')
    ent8 = ttk.Button(gcw, command=all_nouns[7].gcase_check, text='Enter')
    ent9 = ttk.Button(gcw, command=all_nouns[8].gcase_check, text='Enter')
    ent10 = ttk.Button(gcw, command=all_nouns[9].gcase_check, text='Enter')
    ent = [ent1, ent2, ent3, ent4, ent5, ent6, ent7, ent8, ent9, ent10]

    lbl1 = ttk.Label(gcw, text=(questions[0] + '\n\n'))
    lbl2 = ttk.Label(gcw, text=(questions[1] + '\n\n'))
    lbl3 = ttk.Label(gcw, text=(questions[2] + '\n\n'))
    lbl4 = ttk.Label(gcw, text=(questions[3] + '\n\n'))
    lbl5 = ttk.Label(gcw, text=(questions[4] + '\n\n'))
    lbl6 = ttk.Label(gcw, text=(questions[5] + '\n\n'))
    lbl7 = ttk.Label(gcw, text=(questions[6] + '\n\n'))
    lbl8 = ttk.Label(gcw, text=(questions[7] + '\n\n'))
    lbl9 = ttk.Label(gcw, text=(questions[8] + '\n\n'))
    lbl10 = ttk.Label(gcw, text=(questions[9] + '\n\n'))
    lbl = [lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7, lbl8, lbl9, lbl10]

    lgc_lbl.place(x=5, y=1)
    golgc.place(x=190, y=1)
    gcw.minsize(300, 330)
    gcw.title('Genitive case')

    y1 = 30
    for q in range(10):
        lbl[q].place(x=5, y=y1)
        inp[q].place(x=85, y=y1)
        ent[q].place(x=215, y=y1 - 1)
        gcw.update()
        y1 += 30

    tutw.mainloop()
    gcw.mainloop()
    all_nouns = []

def acsetup():
    mw.destroy()
    ac = Tk()
    ac.mainloop()

def pcsetup():
    mw.destroy()
    pc = Tk()
    pc.mainloop()

def dcsetup():
    mw.destroy()
    dc = Tk()
    dc.mainloop()

def icsetup():
    mw.destroy()
    ic = Tk()
    ic.mainloop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mainsetup()
