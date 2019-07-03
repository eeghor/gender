import json
from unidecode import unidecode
from string import ascii_lowercase
import os
import re
from collections import defaultdict

from typing import NamedTuple

# when the ASCII flag is used, \w is [a-zA-Z0-9_]
email_exp = re.compile(r'^[a-z]+[\w\.\-]+[a-z0-9]+\@{1}[a-z0-9]+[\w\.]+[a-z]$', flags=re.ASCII)

saluts = json.load(open('data/data_salutations_.json'))
first_names = json.load(open('data/data_names_.json'))

class Customer(NamedTuple):

	title: str
	first_name: str
	last_name: str
	email: str

	@classmethod
	def from_string(cls, st):

		title = None
		first_name = None
		last_name = None
		email = None

		st_ = str(st).lower().strip()

		# try to find the email address first
		noemail_ = []

		for _ in st_.split():
			try:
				email = re.search(email_exp, _).group(0)
			except:
				pass
			if not email:
				noemail_.append(_)

		# what's not an email address goes in here;
		# replace any non-white space separators with white spaces
		# and then replace all non-single white spaces with a single one
		st_ = re.sub(r'\s+', ' ', re.sub(r'[\.\,\-\_]', ' ', ' '.join(noemail_)))

		# try to find salutation

		def find_title(s):

			for type_ in 'common uncommon'.split():
				for g in saluts[type_]:
					tt_ = set(saluts[type_][g]) & set(s.split())
					if tt_:
						return tt_.pop()

		title = find_title(st_)

		if title:
			st_ = ' '.join([c for c in [re.sub(r'[^' + ascii_lowercase + r']', '', _).strip() 
												for _ in st_.split() if _ != title] if c])
		
		# now to the first name; assume that first name is more likely to stand before the last name
		fnms = []
		for _ in st_.split():
			if _ in first_names:
				if first_names[_] in 'm f'.split():
					first_name = _
					break
				else:
					# it's a unisex name, add to candidates
					fnms.append(_)

		if (not first_name) and fnms:
			first_name = fnms.pop()

		if first_name:
			st_ = ' '.join([_ for _ in st_.split() if _ != first_name]).strip()

		# what's the last name then? assume it's more likely to come last
		if st_:
			last_name = st_.split().pop()

		return cls(title=title, first_name=first_name,  last_name=last_name, email=email)

class Person:
	pass

class GenderDetector:

	"""
	figure out a customer's gender from her name, self-reported salutation or email address
	"""

	DATA = defaultdict()

	DATA['name_db'], DATA['title_db'], DATA['hypoc_db'], DATA['grammg_db'] = \
				[json.load(open(f,'r')) for f in [os.path.join(os.path.dirname(__file__),'data/data_names_.json'), 
				 								  os.path.join(os.path.dirname(__file__),'data/data_salutations_.json'), 
				 								  os.path.join(os.path.dirname(__file__),'data/data_hypocorisms_.json'),
				 								  os.path.join(os.path.dirname(__file__),'data/data_grammgender_.json')]]

	info = f'dictionaries: {len(DATA["grammg_db"]):,} names, {len(DATA["grammg_db"]):,} hypocorisms, {len(DATA["grammg_db"]):,} grammatical gender words'
																	 
	def __init__(self, priority='name'):

		self.title_gender = None
		self.name_gender = None
		self.email_gender = None
		likely_gender = None

		self.PRIORITY = priority


	def _is_string(self, st):

		"""
		is st a string (and NOT an empty string or white space)?
		"""
		
		if not isinstance(st, str):
			return False
		elif not st.strip():
			return False
		else:
			return True

	def _normalize(self):
		
		"""
		normalize (full) name and email address
		"""

		self.title, self.name, self.email = [unidecode(_) if self._is_string(_) else None 
													for _ in [self.title, self.name, self.email]]  
		
		if self.title:

			if self.title.strip():
				self.title = ''.join([c for c in self.title if c in ascii_lowercase])
			if not self.title:
				self.title = None
		
		if self.name:
			# name: only keep letters, white spaces (reduced to a SINGLE white space) and hyphens
			self.name = ' '.join(''.join([c for c in self.name.lower() 
										if (c in ascii_lowercase) or (c in [' ','-'])]).split()).strip()
			if not (set(self.name) & set(ascii_lowercase)):
				self.name = None

		if self.email:
			self.email = ''.join([c for c in self.email.split('@')[0].lower().strip() if (c in ascii_lowercase) or (c in ['.','-','_'])])
			if not self.email:
				self.email = None

		return self

	def _gend_from_title(self):

		"""
		suggest gender based on salutation (title) if the title points to either male or female
		"""

		self.title_gender = None
	
		for g in 'm f'.split():
			if self.title and (self.title.lower() in self.GenderDetector.DATA['grammg_db']['title_db']['common'][g] + self.GenderDetector.DATA['grammg_db']['title_db']['uncommon'][g]):
				self.title_gender = g

		return self

	def _longest_common(self, set_a, set_b):

		"""
		helper to find the longest common word for sets a and b
		"""
		_ = set_a & set_b
		
		return max(_, key=len) if _ else None

	def _gend_from_name(self):

		self.name_gender = None

		if not self.name:
			self.name_gender = None
			return self

		nameparts = {_ for w in self.name.split() for _ in w.split('-')}

		_ = self._longest_common(nameparts, set(self.GenderDetector.DATA['grammg_db']['name_db']) | set(self.GenderDetector.DATA['grammg_db']['hypoc_db']))

		if not _:
			return self

		if _ in self.GenderDetector.DATA['grammg_db']['name_db']:
			self.name_gender = self.GenderDetector.DATA['grammg_db']['name_db'][_]
		else:
			# find what names corresp.to hypocorism and are in the name database
			_ = self._longest_common(set(self.GenderDetector.DATA['grammg_db']['hypoc_db'][_]), set(self.GenderDetector.DATA['grammg_db']['name_db']))
			if _ and (self.GenderDetector.DATA['grammg_db']['name_db'][_] != 'u'):
				self.name_gender = self.GenderDetector.DATA['grammg_db']['name_db'][_]
		if self.name_gender not in 'm f'.split():
			self.name_gender = None
		
		return self

	def _gend_from_email(self):

		self.email_gender = None

		if not self.email:
			self.email_gender = None
			return self
		
		# find any names in the email prefix; ONLY those separated by _, - or . count
		emailparts = set(q.strip() for w in self.email.split('_') 
										for v in w.split('.') 
											for q in v.split('-') if q.strip())

		_ = self._longest_common(emailparts, set(self.GenderDetector.DATA['grammg_db']['name_db']))

		if _ and (self.GenderDetector.DATA['grammg_db']['name_db'][_] != 'u'):
			self.email_gender = self.GenderDetector.DATA['grammg_db']['name_db'][_]
			return self

		_ = self._longest_common(emailparts, set(self.GenderDetector.DATA['grammg_db']['hypoc_db']))

		if _ and (_ in self.GenderDetector.DATA['grammg_db']['name_db']) and (self.GenderDetector.DATA['grammg_db']['name_db'][_]!= 'u'):
			self.email_gender = self.GenderDetector.DATA['grammg_db']['name_db'][longest_hyp]
			return self

		# last resort: grammatical gender

		_ = self._longest_common(emailparts, set(self.GenderDetector.DATA['grammg_db']['grammg_db']))

		if _:
			self.email_gender = self.GenderDetector.DATA['grammg_db']['grammg_db'][_]

		return self

	def get_gender(self, customers):

		"""
		detect gender by first name, title and email and then decide which one to pick as the likeliest gender
		"""

		for c in customers:

			self.title, self.name, self.email = c.title, c.name, c.email	
	
			self._normalize()
	
			self._gend_from_title()
			self._gend_from_name()
			self._gend_from_email()
			
			likely_gender = None

			# the title based suggestion is available and the same as the name based one
			if all([self.title_gender, self.name_gender, self.title_gender == self.name_gender]):
				likely_gender = self.name_gender
			# both are available but NOT the same
			elif all([self.name_gender, self.title_gender]):
				if self.PRIORITY == 'name':
					likely_gender = self.name_gender
				else:
					likely_gender = self.title_gender
			# what is only one is available
			elif all([self.title_gender, not self.name_gender]):
				likely_gender = self.title_gender
	
			elif all([self.name_gender, not self.title_gender]):
				likely_gender = self.name_gender
			# finally, if the email based is the only one we have, use it
			elif self.email_gender:
				likely_gender = self.email_gender
		
			c.gender = likely_gender

			yield c	

	def _keep_letters(self, s):

		return ''.join([c for c in s if c.isalpha()])

	def _parse_input(self, s):
		"""
		s is presumably a string expected to contain name, email address and possibly title; find all of these
		"""
		_allowed_chars = {'.','@','_','-',' '}  # chars of possible value, we keep them

		s = ''.join([ch for ch in s.lower() if (ch in _allowed_chars) or ch.isalnum()]).strip()

		# find possible title matches
		_titles = ({self._keep_letters(_) for _ in s.split() if '@' not in _} & 
					{t for l in [self.GenderDetector.DATA['grammg_db']['title_db']['common'][g] + self.GenderDetector.DATA['grammg_db']['title_db']['uncommon'][g] 
							for g in 'm f u'.split()] for t in l})
		
		title = max(_titles, key=len) if _titles else None

		_emails = [_ for _ in s.split() if '@' in _]

		if _emails:
			emails = _emails[0]
		else:
			emails = None

		name = ' '.join([_ for _ in s.split() if (_ not in _emails) and (self._keep_letters(_) != title)])

		return (title, ' '.join([self._keep_letters(w) for w in name.split()]), emails)

	def _create_person(self, s):

		c = Person()

		c.title, c.name, c.email = self._parse_input(s)

		return c

	def gender(self, s):

		if isinstance(s, list):
			_s = s
		elif isinstance(s, str):
			# make it a list
			_s = [s]
		else:
			return None

		_genders = [x.gender if x.gender else None for x in self.get_gender((self._create_person(_) for _ in _s))]


		return _genders if len(_genders) > 1 else _genders[0]
