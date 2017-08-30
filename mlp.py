#!/usr/bin/env python
# encoding=utf8

__author__	= "Brett Chalabian"
__license__	= "GPL"

from textblob import TextBlob
import pickle
import random
import argparse


class chainlink:
	def __init__(self, term):
		self.term = term
		self.dict = {}
		self.transm = {}
		self.count = 0
		self.stale = False

	def add(self, newt):
		self.stale = True
		self.count += 1
		if newt in self.dict:
			self.dict[newt] += 1
		else:
			self.dict[newt] = 1

	def getTransMatrix(self):
		if self.stale:
			self.buildTransMatrix()

		return self.transm

	def buildTransMatrix(self):
		newTransm = {}
		for term in self.dict:
			newTransm[term] = self.dict[term]/self.count

		self.stale = False
		self.transm = newTransm

	def print(self):
		self.buildTransMatrix();
		print(self.term)
		print(self.count)
		print(self.transm)


def trainMarkov(markov, sample, depth = 1):
	blob = TextBlob(sample)
	terms = blob.ngrams(n=(depth + 1))

	for t in terms:
		ht = tuple(t[0:-1])
		if ht not in markov:
			markov[ht] = chainlink(ht)
	
		markov[ht].add(t[-1])

	return markov

def generateText(markov, length, seed = ""):
	if seed == "":
		seed = list(random.choice(list(markov.keys())))


	if (tuple(seed) not in markov):
		print("seed not in markov")
		return

	if (length <= 0):
		return

	transm = markov[tuple(seed)].getTransMatrix()
	transprob = random.random()
	curprob = 0
	nterm = "."

	for term in transm:
		curprob += transm[term]
		if curprob >= transprob:
			nterm = term
			print("Term: " + nterm)
			break

	first, *rest = seed
	rest.append(nterm)
	generateText(markov, length - 1, rest)

	

def test():
	sample = "The way to get startup ideas is not to try to think of startup ideas. It's to look for problems, preferably problems you have yourself. The very best startup ideas tend to have three things in common: they're something the founders themselves want, that they themselves can build, and that few others realize are worth doing. Microsoft, Apple, Yahoo, Google, and Facebook all began this way. Why is it so important to work on a problem you have? Among other things, it ensures the problem really exists. It sounds obvious to say you should only work on problems that exist. And yet by far the most common mistake startups make is to solve problems no one has. I made it myself. In 1995 I started a company to put art galleries online. But galleries didn't want to be online. It's not how the art business works. So why did I spend 6 months working on this stupid idea? Because I didn't pay attention to users. I invented a model of the world that didn't correspond to reality, and worked from that. I didn't notice my model was wrong until I tried to convince users to pay for what we'd built. Even then I took embarrassingly long to catch on. I was attached to my model of the world, and I'd spent a lot of time on the software. They had to want it! Why do so many founders build things no one wants? Because they begin by trying to think of startup ideas. That m. o. is doubly dangerous: it doesn't merely yield few good ideas; it yields bad ideas that sound plausible enough to fool you into working on them. At YC we call these made-up or sitcom startup ideas. Imagine one of the characters on a TV show was starting a startup. The writers would have to invent something for it to do. But coming up with good startup ideas is hard. It's not something you can do for the asking. So (unless they got amazingly lucky) the writers would come up with an idea that sounded plausible, but was actually bad. For example, a social network for pet owners. It doesn't sound obviously mistaken. Millions of people have pets. Often they care a lot about their pets and spend a lot of money on them. Surely many of these people would like a site where they could talk to other pet owners. Not all of them perhaps, but if just 2 or 3 percent were regular visitors, you could have millions of users. You could serve them targeted offers, and maybe charge for premium features. The danger of an idea like this is that when you run it by your friends with pets, they don't say I would never use this. They say Yeah, maybe I could see using something like that. Even when the startup launches, it will sound plausible to a lot of people. They don't want to use it themselves, at least not right now, but they could imagine other people wanting it. Sum that reaction across the entire population, and you have zero users. When a startup launches, there have to be at least some users who really need what they're making—not just people who could see themselves using it one day, but who want it urgently. Usually this initial group of users is small, for the simple reason that if there were something that large numbers of people urgently needed and that could be built with the amount of effort a startup usually puts into a version one, it would probably already exist. Which means you have to compromise on one dimension: you can either build something a large number of people want a small amount, or something a small number of people want a large amount. Choose the latter. Not all ideas of that type are good startup ideas, but nearly all good startup ideas are of that type. Imagine a graph whose x axis represents all the people who might want what you're making and whose y axis represents how much they want it. If you invert the scale on the y axis, you can envision companies as holes. Google is an immense crater: hundreds of millions of people use it, and they need it a lot. A startup just starting out can't expect to excavate that much volume. So you have two choices about the shape of hole you start with. You can either dig a hole that's broad but shallow, or one that's narrow and deep, like a well. Made-up startup ideas are usually of the first type. Lots of people are mildly interested in a social network for pet owners. Nearly all good startup ideas are of the second type. Microsoft was a well when they made Altair Basic. There were only a couple thousand Altair owners, but without this software they were programming in machine language. Thirty years later Facebook had the same shape. Their first site was exclusively for Harvard students, of which there are only a few thousand, but those few thousand users wanted it a lot. When you have an idea for a startup, ask yourself: who wants this right now? Who wants this so much that they'll use it even when it's a crappy version one made by a two-person startup they've never heard of? If you can't answer that, the idea is probably bad. You don't need the narrowness of the well per se. It's depth you need; you get narrowness as a byproduct of optimizing for depth (and speed). But you almost always do get it. In practice the link between depth and narrowness is so strong that it's a good sign when you know that an idea will appeal strongly to a specific group or type of user. But while demand shaped like a well is almost a necessary condition for a good startup idea, it's not a sufficient one. If Mark Zuckerberg had built something that could only ever have appealed to Harvard students, it would not have been a good startup idea. Facebook was a good idea because it started with a small market there was a fast path out of. Colleges are similar enough that if you build a facebook that works at Harvard, it will work at any college. So you spread rapidly through all the colleges. Once you have all the college students, you get everyone else simply by letting them in. Similarly for Microsoft: Basic for the Altair; Basic for other machines; other languages besides Basic; operating systems; applications; IPO. SelfHow do you tell whether there's a path out of an idea? How do you tell whether something is the germ of a giant company, or just a niche product? Often you can't. The founders of Airbnb didn't realize at first how big a market they were tapping. Initially they had a much narrower idea. They were going to let hosts rent out space on their floors during conventions. They didn't foresee the expansion of this idea; it forced itself upon them gradually. All they knew at first is that they were onto something. That's probably as much as Bill Gates or Mark Zuckerberg knew at first. Occasionally it's obvious from the beginning when there's a path out of the initial niche. And sometimes I can see a path that's not immediately obvious; that's one of our specialties at YC. But there are limits to how well this can be done, no matter how much experience you have. The most important thing to understand about paths out of the initial idea is the meta-fact that these are hard to see. So if you can't predict whether there's a path out of an idea, how do you choose between ideas? The truth is disappointing but interesting: if you're the right sort of person, you have the right sort of hunches. If you're at the leading edge of a field that's changing fast, when you have a hunch that something is worth doing, you're more likely to be right. In Zen and the Art of Motorcycle Maintenance, Robert Pirsig says:You want to know how to paint a perfect painting? It's easy. Make yourself perfect and then just paint naturally. I've wondered about that passage since I read it in high school. I'm not sure how useful his advice is for painting specifically, but it fits this situation well. Empirically, the way to have good startup ideas is to become the sort of person who has them. Being at the leading edge of a field doesn't mean you have to be one of the people pushing it forward. You can also be at the leading edge as a user. It was not so much because he was a programmer that Facebook seemed a good idea to Mark Zuckerberg as because he used computers so much. If you'd asked most 40 year olds in 2004 whether they'd like to publish their lives semi-publicly on the Internet, they'd have been horrified at the idea. But Mark already lived online; to him it seemed natural. Paul Buchheit says that people at the leading edge of a rapidly changing field live in the future. Combine that with Pirsig and you get:Live in the future, then build what's missing. That describes the way many if not most of the biggest startups got started. Neither Apple nor Yahoo nor Google nor Facebook were even supposed to be companies at first. They grew out of things their founders built because there seemed a gap in the world. If you look at the way successful founders have had their ideas, it's generally the result of some external stimulus hitting a prepared mind. Bill Gates and Paul Allen hear about the Altair and think I bet we could write a Basic interpreter for it. Drew Houston realizes he's forgotten his USB stick and thinks I really need to make my files live online. Lots of people heard about the Altair. Lots forgot USB sticks. The reason those stimuli caused those founders to start companies was that their experiences had prepared them to notice the opportunities they represented. The verb you want to be using with respect to startup ideas is not think up but notice. At YC we call ideas that grow naturally out of the founders' own experiences organic startup ideas. The most successful startups almost all begin this way. That may not have been what you wanted to hear. You may have expected recipes for coming up with startup ideas, and instead I'm telling you that the key is to have a mind that's prepared in the right way. But disappointing though it may be, this is the truth. And it is a recipe of a sort, just one that in the worst case takes a year rather than a weekend."
	markov = trainMarkov({}, sample, "testmarkov.p", 1)

	seedWord = list(random.choice(list(markov.keys())))
	print(seedWord)
	generateText(markov, 3300, seedWord)		


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--train", help="train the markov chain on an input")
	parser.add_argument("-l", "--load", help="load existing pickle file for training")
	parser.add_argument("-o", "--output", help="pickle output file containing markov chain")
	args = parser.parse_args()

	markov = {}

	if args.load:
		markov = pickle.load(args.load)

	if args.train:
		with open(args.train, 'r') as file:
			trainMarkov(markov, file.read(), 1)

	while True:
		inp = input("Generate text? (y/n)\n")
		if inp == "n":
			break;
		if inp == "y":
			inp = input("How many words?\n")
			try:
				length = int(inp)
				if length < 1:
					print("Invalid input.\n\n")
				else:
					generateText(markov, length)
			except ValueError:
				print("Invalid input.\n\n")

	if args.output:
		with open(args.output, 'wb') as file:
			pickle.dump(markov, file)
			print("Outputting markov to file: " + args.output)









