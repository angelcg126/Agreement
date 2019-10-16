# -*- coding: utf-8 -*-
#French
#global variables
disjonction = {"onze", "onzième", "oui", "ouitisti"} #words starting with vowel but blocking elision
h_muet_raw = open("res\\h_muet.txt", mode="r")
h_muet = set(h_muet_raw.readlines()) #words starting with h but enabling elision
h_muet_raw.close()

#French definite articles
fr_def_art = {
	"singular": {
		"elision": ["l'"],
		"masculine": ["le"],
		"feminine": ["la"], 
		"neuter": []
	}, "plural": {
		"default": ["les"],
		"masculine": [],
		"feminine": [], 
		"neuter": []
	} 
}
#noun class
class Noun:
	def __init__ (self, value, gender, number, case=None):
		#all value types are string
		self.value = value
		self.gender = gender #values can be masculine, feminine
		self.number = number #values can be singular, plural
		self.case = case

	#method to affix determined article
	def affix_def_art (self):
		if self.number == "singular":
			if (self.value[0] in "aâeiîoôu" and self.value not in disjonction) or self.value in h_muet:
				return "{article}{noun}".format(article = fr_def_art[self.number]["elision"][0], noun = self.value)
			else:
				return "{article} {noun}".format(article = fr_def_art[self.number][self.gender][0], noun = self.value)
		elif self.number == "plural":
			return "{article} {noun}".format(article = fr_def_art[self.number]["default"][0],noun = self.value)

#sentence class with verbs
class Sentence:
	def __init__(self, tense):
		self.tense = tense #value type is a string, possible values are present, past, future

	def subject_arrive_opt_time (self, subject, subj_art, time=None):
		#subject value type is Noun class
		#subj_art value type is string, it can be def, und or any possessive
		#time value type is a string
		if time:
			time_output = " à {time}".format(time=time)
		else:
			time_output = ""

		if subj_art == "def":
			selected_subj = subject.affix_def_art()
		elif subj_art == "und":
			selected_subj = subject.affix_und_art()
		elif subj_art == "2si":
			selected_subj = subject.affix_2si_possesive()
		elif subj_art == "2pi":
			selected_subj = subject.affix_2pi_possesive()
		else:
			selected_subj = subject

		#output table
		sents = {
			"present": 
				{"singular": "{subject} arrive{time}",
				"plural": "{subject} arrivent{time}"},
			"future":
				{"singular": "{subject} arrivera{time}",
				"plural": "{subject} arrivont{time}"},
			"past":
				{"feminine":
					{"singular": "{subject} est arrivée{time}",
					"plural": "{subject} sont arrivées{time}"},
				"masculine":
					{"singular": "{subject} est arrivé{time}",
					"plural": "{subject} sont arrivés{time}"}
				}
			}

		if self.tense == "past":
			return sents[self.tense][subject.gender][subject.number].format(subject = selected_subj, time = time_output)
		else:
			return sents[self.tense][subject.number].format(subject = selected_subj, time = time_output)

	def det_subject_buy_und_object (self, subject, subj_art, object_, object_art, time=None):
		#subject and object_ value type is  Noun class
		#subj_art and object_art value type is string, it can be def, und or any possessive
		#time value type is a string
		if time:
			time_output = " à {time}".format(time=time)
		else:
			time_output = ""

		if subj_art == "def":
			selected_subj = subject.affix_def_art()
		else:
			selected_subj = subject

		if object_art == "def":
			selected_obj = object_.affix_def_art()
		else:
			selected_obj = object_

		sents = {
			"present": 
				{"singular": "{subject} achète {object}{time}",
				"plural": "{subject} achètent {object}{time}"},
			"future":
				{"singular": "{subject} achetera {object}{time}",
				"plural": "{subject} acheteront {object}{time}"},
			"past":
				{"singular": "{subject} a acheté {object}{time}",
				"plural": "{subject} ont acheté {object}{time}"}
		}

		return sents[self.tense][subject.number].format(subject = selected_subj, object = selected_obj, time = time_output)

airplane = Noun("avion", "masculine", "singular")
woman = Noun("femme", "feminine", "singular")
boy = Noun("garçon", "masculine", "singular")
doctors = Noun("médécins", "masculine", "plural")
people = Noun("héritières", "feminine", "plural")
cars = Noun("voitures", "feminine", "plural")
presents = Noun("cadeaux", "masculine", "plural")
girlfriend = Noun("amie", "feminine", "plural")

past = Sentence("past")
future = Sentence("future")
present = Sentence("present")

print (past.subject_arrive_opt_time(woman, subj_art = "def"))
print (past.subject_arrive_opt_time(airplane, "def", "15:30 h"))
print (future.subject_arrive_opt_time(boy, "def", "18:00 h"))
print (past.det_subject_buy_und_object(woman, "def", airplane, "def", "20 h"))
print (present.det_subject_buy_und_object(doctors, "def", presents, "def"))
print (past.subject_arrive_opt_time(people, "def"))
print (present.subject_arrive_opt_time(people, "def"))