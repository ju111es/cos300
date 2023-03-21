
from tkinter import *
from tkinter import ttk
import random as rnd
from idlelib.tooltip import Hovertip as Ht

all_verbs = []

pronounsn = {'я':'i', 'ты':'you', 'он':'he', 'она':'she', 'оно':'it',
             'мы':'we', 'вы':'you (polite/plural)', 'они':'they'}
ilist = ['г', 'к', 'х', 'ж', 'ч', 'ш', 'щ']
ylist = ilist
ylist.append('ц')
alist = ylist
olist = ['ж', 'ч', 'ш', 'щ', 'ц']
vowels_list = ['а', 'я', 'у', 'ю', 'о', 'е', 'ё', 'и', 'ы']

class Noun:
    def __init__(self, noun, gender, animate):
        self.gender = gender
        self.animate = animate
        self.g = '-'
        self.a = '-'
        self.p = '-'
        self.d = '-'
        self.i = '-'
        # letters stand for genitive, accusative, prepositional, dative, and instrumental (cases).
        # nouns have different endings in each case depending on the letter they end in.
        # in the accusative case, it is relevant whether the noun is animate or not.
        # it is also sometimes relevant where the word is stressed. i'm still figuring out how to incorporate this.
        if noun[-1] == 'a':
            if noun.index(-2) in ilist:
                # some vowels (ы, ю, я) can't follow certain consonants.
                self.g = 'и'
            else:
                self.g = 'ы'
            if noun.index(-2) in olist:
                self.i = 'ей'
            else:
                self.i = 'ой'
            self.a = 'y'
            self.p = 'e'
            self.d = 'e'
        elif noun[-1] == 'я':
            if noun.index(-2) in ylist:
                self.a = 'у'
            else:
                self.a = 'ю'
            if noun.index(-2) == 'и':
                self.p = 'и'
                self.d = 'и'
            else:
                self.p = 'e'
                self.d = 'e'
            self.g = 'и'
            self.i = 'ей'
        elif noun[-1] != 'а' and noun[-1] != 'я' and noun[-1] != 'й' \
                and noun[-1] != 'ь' and noun[-1] != 'о' and noun[-1] != 'е':
            self.a = 'a'
            self.g = 'a'
            self.p = 'e'
            self.d = 'y'
            self.i = 'ом'
        elif noun[-1] == 'й':
            self.a = 'я'
            self.g = 'я'
            self.p = 'e'
            self.d = 'ю'
            self.i = 'ем'
        elif noun[-1] == 'ь':
            # this letter (the 'soft sign') can indicate either a masculine or feminine noun.
            # case endings differ based on the noun's gender.
            if self.gender == 'm':
                self.a = 'я'
                self.g = 'я'
                self.p = 'е'
                if noun[-2] in ylist:
                    self.d = 'у'
                else:
                    self.d = 'ю'
                self.i = 'ем'
            elif self.gender == 'f':
                self.a = noun[-1]
                self.g = 'и'
                self.p = 'e'
                self.d = 'и'
                self.i = 'ью'
        elif noun[-1] == 'о':
            self.a = noun[-1]
            self.g = 'а'
            self.p = 'е'
            self.d = 'у'
            self.i = 'ом'
        elif noun[-1] == 'е':
            self.a = noun[-1]
            self.g = 'я'
            if noun[-2] == 'и':
                self.p = 'и'
            else:
                self.p = 'е'
            if noun[-2] in ylist:
                self.d = 'у'
            else:
                self.d = 'ю'
            self.i = 'ем'
        if self.gender == 'm' and self.animate is False:
            self.a = noun[-1]

class Verb:

    def __init__(self, verb, stem, ending, qlist, inplist):
        self.verb = verb
        self.stem = stem
        self.ending = ending
        self.qlist = qlist
        self.inplist = inplist

        global all_verbs
        all_verbs.append(self)

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
                    if self.stem[-1] in vowels_list:
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
                if self.ending == 'ить':
                    self.mutStem = self.stem + 'л'
                    return True
                elif self.ending == 'ать':
                    return False
            elif lc == 'к' or lc == 'т':
                if self.stem[-2] == 'с':
                    self.mutStem = self.stem.replace('с' + lc, 'щ')
                    return True
                elif lc == 'т' and self.ending == 'ать':
                    return False
                else:
                    self.mutStem = self.stem.replace(lc, 'ч')
                    return True
            elif lc == 'д' or lc == 'з' or lc == 'г':
                if lc == 'г' or lc == 'д' and self.ending == 'ать':
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
        cc = 0
        if i != a:
            try:
                if self.mutStem != None and self.stem in i:
                    correction = ttk.Label(nw,
                        text='This is an instance of consonant mutation. \nIf you need a refresher on how it works, click Learn.')
            except AttributeError:
                if self.stem not in i:
                    correction = ttk.Label(nw,
                        text='This is NOT an instance of consonant mutation. \nIf you need a refresher on how it works, click Learn.')
                else:
                    correction = ttk.Label(nw, text='Incorrect...')
        else:
            correction = ttk.Label(nw, text='Correct!')
            cc += 1
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
    gogc = ttk.Button(mw, text='Genitive Case', command=gcsetup)
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

    tutw = Tk()
    tut = 'Enter just the conjugation of the verb\naccording to the pronoun in front of it.' \
          '(Don\'t enter the pronoun, or it won\'t work correctly!\nJust the verb.)'
    tutw.minsize(290, 50)
    tutw.maxsize(290, 50)

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

    # initializing verbs for the questions
    lcm_lbl = ttk.Label(cmw, text='Don\'t know consonant mutation?')
    golcm = ttk.Button(cmw, text='Learn', command=NONE)

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
        inp[q].place(x=80, y=y1)
        ent[q].place(x=215, y=y1-1)
        cmw.update()
        y1 += 30

    cmw.mainloop()
    all_verbs = []

def gcsetup():
    mw.destroy()
    gc = Tk()
    gc.mainloop()

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
