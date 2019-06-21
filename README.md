# gender
Have a name and possibly an email address and wondering whether it’s a male or a female? This package gives you the answer. 

### Key Advantages

* Very simple to use
* Accepts a single string or a list of strings as input
* Relies on a dataset of 130,000+ unique names
* Covers [hypocorisms](https://en.wikipedia.org/wiki/Hypocorism) (English only at this time)
* Makes use of a person’s email address (if available) via searching for names and [grammatical gender](https://en.wikipedia.org/wiki/Grammatical_gender) words in the prefix
* Doesn’t care if the input has bad formatting

### Latest Update (21/06/2019)
* added 1,155 new names (now 133,987 names in the database)
* added many new hypocorism 

### Installation
`pip3 install gender`

### Quickstart
Import and initialise the GenderDetector class:

```
from gender import GenderDetector
gd = GenderDetector()
```

Then use its *gender* method:
```
gd.gender('jaeden collins')
```
Note that you can give it a string with some rubbish in it, like
```
gd.gender('dr.. arian ChiA ,%%%achia58@hotmail.com')
```
Having an email address could make difference. Suppose that you want to figure out gender of someone whose description is 
```
customer_info = 'b w roberts -- roboking@yahoo.co.uk'
```
Both the initials and surname don’t tell you whether this is a male or a female. However, the email prefix robo*king* does look like it’s probably a male because the word *king* always points to a male.

Also note that you can feed a **list**  into the **gender** method in which case you will get a list of identified genders as an output:
```
gd.gender(['steve risotto', 'ana kowalski'])
>> ['m', 'f']
```