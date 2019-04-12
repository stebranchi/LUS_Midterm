from string import ascii_lowercase, ascii_uppercase
import math

f = open('lex.lex', 'w')
train = open('NL2SparQL4NLU.train.conll.txt', 'r')
i = 1
s = set()

f.write('epsilon\t0\n')

for l in train:
	words = l.split()
	if words:
		s.add(words[0])
		tag = words[1]
		if tag[len(tag)-1] == '$':
			tag = tag[:len(tag)-1]
		s.add(tag)

for item in s:
	f.write(item + '\t' + str(i) +'\n')
	i+=1

f.write('<space>\t' + str(i) + '\n')
i+=1
f.write('<unk>\t' + str(i))

f.close()
train.close()

f = open('POS.counts', 'w')
train = open('NL2SparQL4NLU.train.conll.txt', 'r')
i = 1
lex_pos = dict()

for l in train:
	words = l.split()
	if words:
		tag = words[1]
		if tag[len(tag)-1] == '$':
			tag = tag[:len(tag)-1]
		if tag in lex_pos:
			lex_pos[tag] += 1
		else:
			lex_pos[tag] = 1

for key, value in lex_pos.items():
	f.write(key + '\t' + str(value) + '\n')
	i+=1

f.close()
train.close()

f = open('TOK_POS.counts', 'w')
train = open('NL2SparQL4NLU.train.conll.txt', 'r')
i = 1
lex_tok_pos = dict()

for l in train:
	words = l.split()
	if words:
		tag = words[1]
		if tag[len(tag)-1] == '$':
			tag = tag[:len(tag)-1]
		concat = words[0] + ' ' + tag
		if concat in lex_tok_pos:
			lex_tok_pos[concat] += 1
		else:
			lex_tok_pos[concat] = 1

for key, value in lex_tok_pos.items():
	f.write(key + '\t' + str(value) + '\n')
	i+=1

f.close()
train.close()

f = open('TOK_POS.probs','w')

for key, value in lex_tok_pos.items():
	pos_tag = key.split()
	prob = float(lex_tok_pos[key] / lex_pos[pos_tag[1]])
	f.write(str(key) + '\t' + str(prob) + '\n')

f.close()

f = open('TOK_POS.probs','r')
out = open('probs_fst.txt', 'w')

for l in f:
	words = l.split()
	out.write('0\t0\t' + str(words[0]) + '\t' + str(words[1]) + '\t' + str(-math.log(float(words[2]))) + '\n')
out.write('0')

f.close()
out.close()

out = open('unk.txt', 'w')

prob = -math.log(1/38)

for key, value in lex_pos.items():
	out.write('0\t0\t<unk>\t' + key + '\t' + str(prob) + '\n')
out.write('0')
out.close()

out = open('test1.txt', 'w')
out.write('star of Thor')
out.close()
