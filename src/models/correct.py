import itertools
from copy import deepcopy


def correction(ori_text, sys_out):
	sys_words = sys_out.split()
	sys_words.insert(0, '<SOS>')
	sys_words.append('<EOS>')
	ori_words = ori_text.split()
	ori_words.insert(0, '<SOS>')
	ori_words.append('<EOS>')

	# print('trigrams')
	ori_trigrams = []
	c = 2
	while c < len(ori_words) - 2:
		ori_trigrams.append((ori_words[c], ori_words[c + 1], ori_words[c + 2]))
		c += 1

	# print('start unk')
	n_unk = 0
	for i, sys_word in enumerate(sys_words):
		if sys_word == '[UNK]':
			n_unk += 1
			prev_word = sys_words[i - 1]
			next_word = sys_words[i + 1]
			for tri in ori_trigrams:
				if tri[0] == prev_word and tri[2] == next_word:
					sys_words[i] = tri[1]
					break
	# print('start repeat')
	n_repeat = 0
	for i, sys_word in enumerate(sys_words):
		candidates = candidate_words(sys_word)
		if candidates != []:
			n_repeat += 1
		for candidate in candidates:
			if candidate in ori_words:
				sys_words[i] = candidate
				break
	# print(sys_words)
	return ' '.join(sys_words[1:-1])

def candidate_words(sys_word):
	items = list(sys_word)
	group = [(k, sum(1 for _ in vs)) for k, vs in itertools.groupby(items)]
	check_index = []
	for j, g in enumerate(group):
		if g[1] > 2:
			check_index.append(j)
	if not check_index:
		return []

	comb = [[]]
	for j in check_index:
		count = group[j][1]
		length = len(comb)
		tmp = []
		for c in range(count):
			tmp += deepcopy(comb)
			for l in range(length):
				tmp[l + length * c].append(c + 1)
		comb = tmp

	candidates = []
	for c in comb:
		word = ''
		for i, alpha in enumerate(group):
			if i in check_index:
				word += alpha[0] * c[check_index.index(i)]
			else:
				word += alpha[0] * alpha[1]
		candidates.append(word)
	return candidates


if __name__ == '__main__':
	# ori = '대한항공의 한 승무원은 승객들에게 욕설이나 협박하는 말을 자주 듣지만, 이에 대해 문제제기를 하기는 쉽지 않다.'
	# sys = '대한항공의 한 승무원은 [UNK] 욕설이나 협박하는 말을 자주 듣지만, 이에 대해 문제제제제제제제제제제제제제제제제제제제제기를 하기는 쉽지 않다.'
	# correction(ori, sys)

	n_unk = 0
	n_repeat = 0
	with open('./inputs/korean.20000.candidate', 'r', encoding='utf-8') as f:
		lines = f.readlines()
		for line in lines:
			tmp = correction('', line)
			n_unk += tmp[0]
			n_repeat += tmp[1]
	print(n_unk, n_repeat)
