import json
from unidecode import unidecode
from string import ascii_lowercase
import os
import re
from collections import defaultdict

from typing import NamedTuple

# when the ASCII flag is used, \w is [a-zA-Z0-9_]
email_exp = re.compile(r'^[a-z]+[\w\.\-]+[a-z0-9]+\@{1}[a-z0-9]+[\w\.]+[a-z]$', flags=re.ASCII)

saluts = json.load(open(os.path.join(os.path.dirname(__file__),'data/data_salutations_.json')))
fnames = json.load(open(os.path.join(os.path.dirname(__file__), 'data/data_names_.json')))
lnames = [l.strip() for l in open(os.path.join(os.path.dirname(__file__), 'data/data_last_names_.txt')) if l.strip()]
hypocs = json.load(open(os.path.join(os.path.dirname(__file__), 'data/data_hypocorisms_.json')))
gramms = json.load(open(os.path.join(os.path.dirname(__file__),'data/data_grammgender_.json')))

class Person(NamedTuple):

	title: str
	first_name: str
	last_name: str
	email: str
	gender: str

	@classmethod
	def from_string(cls, st):

		title = None
		first_name = None
		last_name = None
		email = None
		gender = None

		st_ = str(st).lower().strip()

		for _ in st_.split():
			try:
				email = re.search(email_exp, _).group(0)
			except:
				pass

		if email:
			st_ = ''.join(st_.split(email)[:-1])

		st_ = re.sub(r'\s+', ' ', re.sub(r'[^' + ascii_lowercase + r']', ' ', st_)).strip()
		
		# try to find salutation
		def find_title(s):

			for type_ in 'common uncommon'.split():
				for g in saluts[type_]:
					tt_ = set(saluts[type_][g]) & set(s.split())
					if tt_:
						return tt_.pop()

		title = find_title(st_)

		if title:
			st_ = ' '.join([_ for _ in st_.split() if _ != title])
		
		# now to the first name; assume that first name is more likely to stand before the last name
		fnms = []
		for _ in st_.split():
			if _ in fnames:
				if fnames[_] in 'm f'.split():
					first_name = _
					break
				else:
					# it's a unisex name, add to candidates
					fnms.append(_)

		if (not first_name) and fnms:
			first_name = fnms[0]
		elif (not first_name):
			for _ in st_.split():
				if _ in hypocs:
					first_name = _
					break

		if first_name:
			st_ = ' '.join([_ for _ in st_.split() if _ != first_name]).strip()

		# what's the last name then? assume it's more likely to come last
		if st_:
			wrds = st_.split()
			known_lnames = set(lnames) & set(wrds)
			if len(known_lnames) == 1:
				last_name = known_lnames.pop()
			elif len(wrds) == 1:
				last_name = wrds[-1]
			elif wrds[-2] not in 'al el de los la van dos del di der ter'.split():
				last_name = wrds[-1]
			else:
				last_name = ' '.join(wrds[-2:])

		return cls(title=title, first_name=first_name,  last_name=last_name, email=email, gender=gender)

class GenderDetector:

	def __init__(self):

		self.GENDS = 'm f'.split()

	def _from_title(self, title):

		for g in self.GENDS:
			if {title} & set(saluts['common'][g] + saluts['uncommon'][g]):
				return g

	def _from_first_name(self, first_name):

		if (first_name in fnames) and (fnames[first_name] in self.GENDS):
			return fnames[first_name]

		if first_name in hypocs:
			gnds = {fnames[nm] for nm in (set(hypocs[first_name]) & set(fnames))}
			return 'm' if {'m'} == gnds else 'f' if {'f'} == gnds else None

	def _from_email(self, email):

		if not email:
			return None

		_email = re.split(r'[\s\-\.\_]', email.split('@')[0])

		# keep potential genders based in first names in here
		first_name_cands = set()
		# similar temporary storage for genders derived from the
		# grammatical gender words found in email address 
		gramm_cands = set()

		for _ in _email:

			_g = self._from_first_name(_)

			if _g:
				first_name_cands.add(_g)

			for w in gramms:
				if (w in _) and (gramms[w] in self.GENDS):
					gramm_cands.add(gramms[w])

		# if one of these candidate sets has a single 
		# candidate then we pick it as gender
		for s in [first_name_cands, gramm_cands]:
			if {'m'} == s:
				return 'm'
			elif {'f'} == s:
				return 'f'

	def get_gender(self, st):

		cust = Person.from_string(st)

		g_title = self._from_title(cust.title)
		g_name = self._from_first_name(cust.first_name)
		g_email = self._from_email(cust.email)

		if all([g_title, g_name, g_title == g_name]):
			return cust._replace(gender=g_title)

		if all([g_title, g_name, g_title != g_name, g_email]):
			if g_email == g_title:
				return cust._replace(gender=g_email)
			elif g_email == g_name:
				return cust._replace(gender=g_email)

		if all([g_title, g_name, not g_email]):
			return cust._replace(gender=g_title)

		if all([not g_title, g_name]):
			return cust._replace(gender=g_name)

		if all([not g_title, not g_name, g_email]):
			return cust._replace(gender=g_email)

		return cust