from string import ascii_lowercase, ascii_uppercase
import math

f = open('lex.lex', 'w')
train = open('NL2SparQL4NLU.train.conll.txt', 'r')
i = 1
s = set()
words_counter = dict()
tags_counter = dict()
wtag_counter = dict()

f.write('epsilon\t0\n')

for l in train:
	words = l.split()
	if words:
		word = words[0]
		s.add(word)
		tag = words[1]
		concat = word + ' ' + tag
		if tag[len(tag)-1] == '$':
			tag = tag[:len(tag)-1]
		s.add(tag)
		if word in words_counter:
			words_counter[word] += 1
		else:
			words_counter[word] = 1
		if tag in tags_counter:
			tags_counter[tag] += 1
		else:
			tags_counter[tag] = 1
		if concat in wtag_counter:
			wtag_counter[concat] += 1
		else:
			wtag_counter[concat] = 1

for key, value in words_counter.items():
	if value == 1:
		s.remove(key)

for item in s:
	f.write(item + '\t' + str(i) +'\n')
	i+=1

f.write('<space>\t' + str(i) + '\n')
i+=1
f.write('<unk>\t' + str(i))

f.close()
train.close()

train = open('NL2SparQL4NLU.train.conll.txt', 'r')

for l in train:
	words = l.split()
	if words:
		word = words[0]
		tag = words[1]
		concat = word + ' ' + tag
		if tag[len(tag)-1] == '$':
			tag = tag[:len(tag)-1]
		if word in s:
			if tag in tags_counter:
				tags_counter[tag] += 1
			else:
				tags_counter[tag] = 1
			if concat in wtag_counter:
				wtag_counter[concat] += 1
			else:
				wtag_counter[concat] = 1

train.close()

out = open('tags.count', 'w')

for key, value in tags_counter.items():
	out.write(str(key) + '\t' + str(value) +'\n')

out.close()

out = open('wtags.count', 'w')

for key, value in wtag_counter.items():
	words = key.split()
	out.write(str(words[0]) + '\t' + str(words[1]) + '\t' + str(value) +'\n')

out.close()

probs_out = open('wtags.probs', 'w')
probs = dict()

for key, value in wtag_counter.items():
	words = key.split()
	tag = words[1]
	prob = float(value/tags_counter[tag])
	probs_out.write(str(words[0]) + '\t' + str(words[1]) + '\t' + str(prob) + '\n')

probs_out.close()
