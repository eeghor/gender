gender
=======================================

Get gender from name and email address

What does it do?
----------------

Suppose you have someone's name and need to find out whether this person is a female (male). The name might come with an email address as it's often the case when you deal with customer records. This package finds the gender for you.

Key Advantages
--------------

- Very simple to use
- Accepts a single string or a list of strings as input
- Relies on a dataset of 130,000+ unique names
- Covers hypocorisms (English only at this time)
- Makes use of a person’s email address (if available) via searching for names and grammatical gender words in the prefix
- Doesn’t care if the input has bad formatting


Installation
------------

.. code-block:: console

	$ pip3 install gender

Quickstart
----------

Import and initialise the GenderDetector class:

.. code-block:: console
	from gender import GenderDetector
	gd = GenderDetector()

Then use its *gender* method:

.. code-block:: pycon

	gd.gender('jaeden collins')

Note that you can give it a string with some rubbish in it, like

.. code-block:: pycon

	gd.gender('dr.. arian ChiA ,%%%achia58@hotmail.com')

Having an email address could make difference. Suppose that you want to figure out gender of someone whose description is 

.. code-block:: pycon
	customer_info = 'b w roberts -- roboking@yahoo.co.uk'

Both the initials and surname don’t tell you whether this is a male or a female. However, the email prefix robo*king* does look like it’s probably a male because the word *king* always points to a male.

Also note that you can feed a **list**  into the **gender** method in which case you will get a list of identified genders as an output:

.. code-block:: pycon
	gd.gender(['steve risotto', 'ana kowalski'])
	>>>['m', 'f']
