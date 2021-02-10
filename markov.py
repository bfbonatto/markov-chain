from collections import defaultdict
from typing import DefaultDict
from random import choices, choice
from sys import stdin

class Chain:
	"""
	A Markov chain generator for sequences of words
	"""
	def __init__(self, text=None):
		self.chain: DefaultDict[str, DefaultDict[str, int]] = defaultdict(lambda: defaultdict(lambda: 0))
		self.start = None
		if text is not None:
			self.train(text)

	def clear(self):
		"""
		An empty chain
		"""
		self.chain = defaultdict(lambda: defaultdict(lambda: 0))
		self.start = None

	def set_start(self, word: str):
		"""
		Set the starting word for a sequence
		"""
		self.start = word

	def next_word(self):
		"""
		Generate the next word in the sequence, update internal state
		and return generated word
		"""
		population = [k for (k,v) in self.chain[self.start].items() if v != 0]
		if population == []:
			return None
		weights = [self.chain[self.start][k] for k in population]
		chosen =  choices(population, weights=weights, k=1)[0]
		self.start = chosen
		return chosen

	def train(self, text: str):
		"""
		Train the chain in regards to some text
		"""
		self.clear()
		for (prev,after) in zip(text.split(), text.split()[1:]):
			self.insert(prev, after)

	def generate(self, length: int, start=None, reset=False):
		"""
		Generate a sequence with at most specified length
		"""
		if start is None and self.start is None:
			start = choice(list(self.chain.keys()))
		if start is not None:
			self.set_start(start)
		text: list[str] = [self.start]
		while len(text) < length:
			chosen = self.next_word()
			if chosen is None and reset:
				self.set_start(start)
				text.append(start)
			elif chosen is None:
				break
			else:
				text.append(chosen)
		return " ".join(text)

	def insert(self, prev: str, after: str):
		"""
		Add a new edge to the chain
		"""
		self.chain[prev][after] += 1

text = " ".join(stdin.readlines())
c = Chain(text)
print(c.generate(100,reset=True))
