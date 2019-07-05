# gender

Have a name and possibly an email address and wondering whether it’s a male or a female? This package gives you the answer. 

### Key Advantages

* Very simple to use
* Relies on a dataset of 130,000+ unique names
* Covers [hypocorisms](https://en.wikipedia.org/wiki/Hypocorism) (English only at this time)
* Makes use of a person’s email address (if available) via searching for names and [grammatical gender](https://en.wikipedia.org/wiki/Grammatical_gender) words in the prefix
* Doesn’t care if the input has bad formatting

### Latest Update (26/06/2019)

* added 68 new Dutch names
* updated gender for some names 

### Previous Update (21/06/2019)

* added 1,155 new names (now 133,987 names in the database)
* added many new hypocorism 

### Installation

`pip3 install gender`

### Quickstart

```
import gender
gd = gender.GenderDetector()
gd.get_gender('jeroen van dijk')
```
which gives you 
```
Person(title=None, first_name='jeroen', last_name='van dijk', email=None, gender='m')
```