import sys
import math

"""A Shakespeare Compiler written in Python, splc.py
This is a compiler that implements the majority of the Shakespeare programming language
invented by Kalle Hasselstrom and Jon Aslund, I take no credit for inventing the language.
This software is free to edit or use, and though I doubt anyone would use this for many projects,
I guess I would appreciate some degree of acknowledgment if you do.
(c) Sam Donow 2013
sad3@williams.edu
drsam94@gmail.com"""
#missing features

#full support for multi-word nouns/names
#other restrictions: e.g need for well-numbered scenes
#Stacks (eh, I may never add these), who needs them?

pos_adj    = []
neg_adj    = []
pos_comp   = []
neg_comp   = []
pos_nouns  = []
neg_nouns  = []
valid_names= []
zero_nouns = ['nothing', 'zero']
src        = ""
N          = 0
vartable   = set([])
speaker    = ""
target     = ""
stage      = set([])
actnum     = 0

#report a compile-time error, then exit
def Assert(b, s):
	global N
	if not b:
		sys.stderr.write(s + " at line " + str(N) + "\n")
		exit()

def isNoun(word):
	return word in pos_nouns or word in neg_nouns or word in zero_nouns

def isAdjective(word):
	return word in pos_adj or word in neg_adj

def isComparative(word):
	return word in pos_comp or word in neg_comp

#returns 1 for "nice" and neutral nouns, -1 for nasty ones
def nounValue(word):
	Assert(isNoun(word), "Tried to find the nounvalue of a non-noun")
	return 1 if word in pos_nouns else -1 if word in neg_nouns else 0

#return s with all whitespace characters removed
def trimWhitespace(s):
	trimmed = ""
	for c in s:
		if c not in ['\t', '\r', '\n', ' ']:
			trimmed += c
	return trimmed

#return s with all whitespace characters before the first non-whitedspace character removed
def trimLeadingWhitespace(s):
	trimIndex = 0
	for c in s:
		if c in ['\t', '\r', '\n', ' ']:
			trimIndex +=1
		else:
			break
	return s[trimIndex:]

#A whitespace-agnositic beginswith method
def beginsWithNoWhitespace(s, pattern):
	return beginsWith(trimWhitespace(s), pattern)

def beginsWith(s, pattern):
	return s[:len(pattern)] == pattern 

def loadFileIntoList(filename, list):
	f = open(filename, 'r')
	for word in f.readlines():
		list.append(word.split(" ")[-1][:-1])
	f.close()

#load initial noun and adjective lists
def loadWordLists():
	loadFileIntoList("include/neutral_adjective.wordlist" , pos_adj)
	loadFileIntoList("include/positive_adjective.wordlist", pos_adj)
	loadFileIntoList("include/negative_adjective.wordlist", neg_adj)
	loadFileIntoList("include/positive_noun.wordlist", pos_nouns)
	loadFileIntoList("include/neutral_noun.wordlist" , pos_nouns)
	loadFileIntoList("include/negative_noun.wordlist", neg_nouns)
	loadFileIntoList("include/positive_comparative.wordlist", pos_comp)
	loadFileIntoList("include/positive_comparative.wordlist", neg_comp)
	loadFileIntoList("include/character.wordlist", valid_names)

roman_values = { 'M': 1000, 'D': 500, 'C': 1000, 'L': 50, 'X': 10, 'V': 5, 'I': 1 }
def parseRomanNumeral(roman_string):
	roman_string = roman_string.upper() 
	strindex = 0
	roman_sum = 0
	while strindex < len(roman_string) - 1:
		if(roman_values[roman_string[strindex]] < roman_values[roman_string[strindex+1]]):
			roman_sum -= roman_values[roman_string[strindex]]
		else:
			roman_sum += roman_values[roman_string[strindex]]
		strindex += 1
	return roman_sum + roman_values[roman_string[strindex]]

def isNumber(s):
	words = s.split(" ")
	for word in words:
		if isNoun(word):
			return True
	return False

#parse a string that is supposed to evaluate to a number
def parseNum(s):
	words = s.split(" ")
	nounIndex = len(words)
	for i in range(0,len(words)):
		if isNoun(words[i]):
			nounIndex = i
			break
	Assert (nounIndex < len(words), str(words) + "\nExpected a number, but found no noun")
	value = nounValue(words[nounIndex])
	for word in words[:nounIndex]:
		if isAdjective(word):
			value *= 2
	return value

def parseEnterOrExit():
	global stage
	endBracket = src[N].find(']')
	Assert(endBracket >= 0, "[ without matching ]")
	enterOrExit = src[N][src[N].find('[')+1:src[N].find(']')]
	if beginsWithNoWhitespace(enterOrExit, "Enter"):
		names = enterOrExit[enterOrExit.find(" ") + 1:].split(" and ")
		for namestr in names:
			name = namestr.split(" ")[-1]
			Assert(name in vartable, "Undeclared actor entering a scene")
			stage.add(name)
		Assert(len(stage) < 3, "Too many actors on stage")
	elif beginsWithNoWhitespace(enterOrExit, "Exit"):
		names = enterOrExit[enterOrExit.find(" ") + 1:].split(" and ")
		for namestr in names:
			name = namestr.split(" ")[-1]
			Assert(name in stage, "Trying to make an actor who is not in the scene exit")
			stage.remove(name)
	elif beginsWithNoWhitespace(enterOrExit, "Exeunt"):
		stage = set([])
	else:
		Assert(False, "Bracketed clause without Enter, Exit, or Exeunt")

#returns the index of the leftmost punctuation mark in s
def findPunctuation(s):
	valids = []
	for val in [s.find('.'), s.find('!'), s.find('?')]:
		if val >= 0:
			valids.append(val)
	return -1 if len(valids) == 0 else min(valids)

#returns an array of the punctuation-delimited statements at the current location in the parsing
def getStatements():
	global N
	statements = []
	line = trimLeadingWhitespace(src[N])
	unfinished = False
	while line.find(':') < 0 and line.find('[') < 0:
		punctuation = findPunctuation(line)
		if punctuation < 0:
			if unfinished == False:
				statements.append(line[:-1])
			else: 
				statements[-1] += line[:-1]
			N += 1
			line = src[N]
			unfinished = True
		elif punctuation > 0:
			if not unfinished:
				statements.append("")
			statements[-1] += line[:punctuation]
			line = line[punctuation + 1:]
			unfinished = False
	retval = []
	for stat in statements:
		if len(trimWhitespace(stat)) > 0:
			retval.append(stat)
	#print retval
	return retval


class Tree:
	def __init__(self, v, l, r):
		self.value = v
		self.left  = l
		self.right = r

def wordToOperator(op):
	if op == "sum":
		return "+"
	elif op == "difference":
		return "-"
	elif op == "quotient":
		return "/"
	elif op == "product":
		return "*"
	else:
		Assert(False, "Illegal Operator")

binop = ["sum", "difference", "quotient", "product"]
unop  = ["square", "cube", "twice"]
def buildExpressionTree(expr):
	Assert (len(expr) > 0, "Ill-formed Expression in " + str(expr))
	if expr[0] == "square":
		if expr[1] == "root":
			op = "(int)sqrt"
			expr = expr[2:]
			num, expr = buildExpressionTree(expr)
			return Tree(op, num, ""), expr
	elif expr[0] == "remainder":
		if expr[1] == "of" and expr[2] == "the" and expr[3] == "quotient":
			expr = expr[4:]
			op = "%"
			left, expr  = buildExpressionTree(expr)
			right, expr = buildExpressionTree(expr)
			return Tree(op, left, right), expr
	if expr[0] in binop:
		op = wordToOperator(expr[0])
		expr  = expr[1:]
		left, expr  = buildExpressionTree(expr)
		right, expr = buildExpressionTree(expr)
		return Tree(op, left, right), expr
	elif expr[0] in unop:
		op = expr[0]
		expr = expr[1:]
		num, expr = buildExpressionTree(expr)
		return Tree(op, num, ""), expr

	if True:
		i = 1 if expr[0] == "and" else 0
		numstr = ""
		while expr[i] not in binop and expr[i] not in unop and expr[i] not in ["and", "remainder"]:
			if expr[i] in ["you", "thee", "yourself", "thyself", "thou"]:
				expr = expr[i + 1:]
				return Tree(target, "", ""), expr
			elif expr[i] in ["me", "myself", "i"]:
				expr = expr[i + 1:]
				return Tree(speaker, "", ""), expr
			elif expr[i].capitalize() in vartable:
				name = expr[i]
				expr = expr[i + 1:]
				return Tree(name.capitalize(), "", ""), expr
			elif i == len(expr) - 1:
				numstr += expr[i]
				i = len(expr)
				break
			else:
				numstr += expr[i] + " "
				i += 1
		if i == len(expr):
			expr = []
		else:
			expr = expr[i:]
		if not isNumber(numstr):
			return buildExpressionTree(expr)
		else:
			return Tree(str(parseNum(numstr)), "", ""), expr

def TreeToString(tree):
	if tree.left == "":
		#just a value
		return str(tree.value)
	elif tree.right == "":
		#unary operator
		return str(tree.value) + "(" + TreeToString(tree.left) + ")"
	else:
		#binary operator
		return "(" + TreeToString(tree.left) + " " + str(tree.value) + " " + TreeToString(tree.right) + ")"

def parseExpr(expr):
	tree = buildExpressionTree(expr.split(" "))[0]
	return TreeToString(tree)

def firstWord(statment):
	words = statement.split(" ")
	for word in words:
		if len(word) > 0:
			return word

def parseStatement(stat):
	statement = trimLeadingWhitespace(stat).lower()
	first = statement.split(" ")[0]
	trimmed = trimWhitespace(statement)
	if first in ["you", "thou"]:
		#this is an assignment of the form Prounoun [as adj as] expression
		expr = ""
		if statement.rfind("as") >= 0:
			expr = statement[statement.rfind("as") + 3:]
		else:
			expr = statement[len(first) + 1:]
		return target + " = " + parseExpr(expr) + " ;\n"
	elif trimmed == "openyourheart" or trimmed == "openthyheart":
		#numerical output
		return 'fprintf(stdout, "%d", ' + target + ');\n'
	elif trimmed == "speakyourmind" or trimmed == "speakthymind":
		#character output
		return 'fprintf(stdout, "%c", (char)' + target + ');\n'
	elif trimmed == "listentoyourheart" or trimmed == "listentothyheart":
		#numerical input
		return 'fgets(inputbuffer, sizeof inputbuffer, stdin);\nsscanf(inputbuffer, "%d", &' + target + ');\n' #" = getchar() - '0';\n"
	elif trimmed == "openyourmind" or trimmed == "openyourmind":
		#character input
		return target + " = getchar();\n"
	elif first in ["am", "are", "art", "be", "is"]:
		#questions - do not yet support "not"
		left  = ""
		kind  = ""
		right = ""
		if statement.find("as") >= 0:
			left, kind, right = statement.split(" as ")
			Assert(isAdjective(kind), "Ill-formed conditional in " + statement)
			kind = "equal"
		elif statement.find("more") >= 0:
			words = statement.split(" ")
			moreloc = 0
			for i in range(0, len(words)):
				if words[i] == "more":
					moreloc = i
					break
			Assert(isAdjective(words[moreloc + 1]), "Ill-formed conditional in " + statement)
			kind = "greater" if words[moreloc + 1] in pos_adj else "lesser"
			left, right = statement.split(" more " + words[moreloc + 1] + " ")
		else:
			comp = ""
			for word in statement.split(" "):
				if isComparative(word):
					comp = word
					break
			Assert(len(comp) > 0, "Ill-formed conditional in " + statement)
			kind = "greater" if comp in pos_comp else "lesser"
			left, right = statement.split(comp)
		return "condition = (" + parseExpr(left) + ") " + (">" if kind == "greater" else "<" if kind == "lesser" else "==") + " (" + parseExpr(right) + ");\n"
	elif beginsWith(statement, "if so,"):
		#positive condition
		location = statement.find("if so,")
		return "if (condition) {\n " + parseStatement(statement[location + 7:]) + " }\n"
	elif beginsWith(statement, "if not,"):
		#negative condition
		location = statement.find("if not,")
		return "if (!condition) {\n " + parseStatement(statement[location + 8:]) + " }\n"
	elif beginsWith(statement, "let us") or beginsWith(statement, "we shall") or beginsWith(statement, "we must"):
		words = statement.split(" ")
		nextTwo = words[2] + " " + words[3]
		Assert (nextTwo == "return to" or nextTwo == "proceed to", "Ill-formed goto")
		Assert (words[4] == "scene" or words[4] == "act", "Ill-formed goto")
		typeword = words[4] if words[4] == "act" else ("act_" + str(actnum) + "_scene")
		return "goto " + typeword + str(parseRomanNumeral(words[5])) + ";\n"
	else:
		return ""

def writeScenes(scenes, isLast):
	print "act" + str(actnum) + ": {\ngoto act_" + str(actnum) + "_scene1;\n}"
	for j in range(0, len(scenes)):
		print "act_" + str(actnum) + "_scene" + str(j + 1) + ": {"
		print scenes[j]
		if j < len(scenes) - 1:
			print "goto act_" + str(actnum) + "_scene" + str(j + 2) + ";\n"
		elif not isLast:
			print "goto act" + str(actnum + 1) + ";\n"
		print "}"
	
def handleDeclarations():
	global N
	global src
	#variables, declaration syntax:
	#Name, value
	declarations = []
	unfinished = False
	while not beginsWithNoWhitespace(src[N], 'Act'):
		Assert(N < len(src) - 1, "File contains no Acts")
		if len(trimWhitespace(src[N])) > 0:
			#print src[N]
			if not unfinished:
				declarations.append(src[N])
			else:
				declarations[-1] += src[N]
			unfinished = src[N].find('.') < 0
		N += 1

	for dec in declarations:
		commaIndex = dec.find(',')
		Assert(commaIndex > 0, "Improper declaration " + str(declarations))
		wordsInName = trimLeadingWhitespace(dec[:commaIndex]).split(" ")
		varname = wordsInName[-1]
		value = parseNum(dec[commaIndex:-2])
		print "int " + str(varname) + " = " + str(value) + ";"
		Assert(varname in valid_names, "Non-Shakespearean variable name")
		vartable.add(varname)

#-------------------------------Begin Main Program-------------------------#
Assert(len(sys.argv) > 1, "No input file")
filename = sys.argv[1]

f = open(filename, 'r')
src = f.readlines()
f.close()

loadWordLists()

#parse the title - all the text up until the first .
#title is unimportant and is thrown out

while src[N].find('.') < 0:
	N += 1
N += 1
#title is thrown out

print "// " + filename
print "// compiled with splc.py (c) Sam Donow 2013"
print "#include <stdio.h>"
print "#include <math.h>"
print '#include "include/mathhelpers.h"'
print "int condition = 0;"
print "char inputbuffer[20];"
print "int main() {\n"

handleDeclarations()
scenes = []
unfinished = False
while N < len(src):
	if beginsWithNoWhitespace(src[N], 'Act'):
		if actnum > 0:
			writeScenes(scenes, False)
			scenes = []
		actnum += 1
		N += 1
	elif beginsWithNoWhitespace(src[N], 'Scene'):
		N += 1
		speaker = ""
		target  = ""
		while (N < len(src)) and not (beginsWithNoWhitespace(src[N], 'Scene') or beginsWithNoWhitespace(src[N], 'Act')):
			if beginsWithNoWhitespace(src[N], '['):
				parseEnterOrExit()
				if not unfinished:
					scenes.append(";\n")
					unfinished = True
				N += 1
			elif src[N].find(':') >= 0:
				name = (src[N][:src[N].find(':')]).split(" ")[-1]
				Assert (name in stage, "An actor who is not on stage is trying to speak")
				for actor in stage:
					if actor != name:
						target = actor
						speaker = name
				N += 1
				statements = getStatements()
				scenecode = ""
				for statement in statements:
					scenecode += parseStatement(statement)
				if not unfinished:
					scenes.append(scenecode)
					unfinished = True
				else:
					scenes[-1] += scenecode
			else:
				N += 1
		unfinished = False

	else:
		N += 1
writeScenes(scenes, True)
#print "int main() {\n\tgoto act1;\n}"#return act1();\n}"
print "}"
