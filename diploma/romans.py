from num2t4ru import num2text
from pymorphy2 import MorphAnalyzer as morph
import roman


def rom2arab(rom):
	return str(roman.fromRoman(rom))

def isroman(word):
	return True if str(morph().parse(word)[0].tag) == "ROMN" else False

def isroman2(words):
	if len(words) == 2:
		if isroman(words[0]) and isroman(words[1]):
			return True
	return False

def num2anum(dig, gender, number, case):
	result = dig
	try:
		result = morph().parse(dig)[0].inflect({'ADJF', 'Anum', gender, number, case}).word
	except AttributeError:
		result = morph().parse(dig)[0].inflect({case}).word
	return result

def default_anum(gen, sing_plur, cas):
	if gen == None:
		gen = "masc"
	if sing_plur == None:
		sing_plur = "sing"
	if cas == None:
		cas = "nomn"
	return (gen, sing_plur, cas)

def anum2text(word, gen, sing_plur, cas):
	anum = None
	num = num2text(int(rom2arab(word)))
	num_lst = num.split()
	if len(num_lst) == 1:
		anum = num2anum(num, gen, sing_plur, cas)
	else:
		anum = " ".join(num_lst[:-1]) + " " + num2anum(num_lst[-1], gen, sing_plur, cas)
	return anum

def isprep(prep):
	preps = ['из', 'от', 'до', 'после', 'начале', 'около', 'кроме', 'протяжении', 'нет',
	         'к', 'благодаря', 'вопреки', 'согласно',
	         'с', 'со', 'за', 'над', 'между', 'перед',
	         'о', 'об', 'в', 'на']
	return True if prep.lower() in preps else False

def preps(preposition):
	gent = ['из', 'от', 'до', 'после', 'начале', 'около', 'кроме', 'протяжении', 'нет'] # родительный
	datv = ['к', 'благодаря', 'вопреки', 'согласно'] # дательный
	ablt = ['с', 'со', 'за', 'над', 'между', 'перед'] # творительный
	loct = ['о', 'об', 'в', 'на'] # предложный
	cases = {g:"gent" for g in gent}
	cases.update({d:"datv" for d in datv})
	cases.update({a:"ablt" for a in ablt})
	cases.update({i:"loct" for i in loct})
	return cases.get(preposition.lower())

def rom2text(lst_words):
	for word in lst_words:
		if isroman(word):
			gen, sing_plur, cas = None, None, None

			if lst_words.index(word) != len(lst_words)-1:
				next_word = lst_words[lst_words.index(word)+1]
				gen = morph().parse(next_word)[0].tag.gender
				sing_plur = morph().parse(next_word)[0].tag.number
				cas = morph().parse(next_word)[0].tag.case

			if lst_words.index(word) != 0 and isprep(lst_words[lst_words.index(word)-1]):
				cas = preps(lst_words[lst_words.index(word)-1])

			gen, sing_plur, cas = default_anum(gen, sing_plur, cas)
			
			# print(gen, sing_plur, cas)

			lst_words[lst_words.index(word)] = anum2text(word, gen, sing_plur, cas)
	return lst_words

def rom2text2(lst_words):
	for word in lst_words:
		words_dashes = word.split("-")
		if isroman2(words_dashes):
			rom1, rom2 = words_dashes[0], words_dashes[1]
			gen, sing_plur, cas = None, None, None

			if lst_words.index(word) != 0 and isprep(lst_words[lst_words.index(word)-1]):
				cas = preps(lst_words[lst_words.index(word)-1])

			gen, sing_plur, cas = default_anum(gen, sing_plur, cas)

			anum1 = anum2text(rom1, gen, sing_plur, cas)
			anum2 = anum2text(rom2, gen, sing_plur, cas)

			lst_words[lst_words.index(word)] = "{} {}".format(anum1, anum2)
	return lst_words


def test_roman(s):
	print(s)
	new_s = " ".join(rom2text2(rom2text(s.split())))
	return new_s
 
# print(test_roman("В XX и XXI веке случилось что-то. На протяжении XX-XXI вв."))
