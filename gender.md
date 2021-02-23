# gender
Figure out someone’s gender by first or last name,  salutation, or email address.

### Key Advantages

* Very simple to use
* Relies on a dataset of 221,000+ unique names
* Covers [hypocorisms](https://en.wikipedia.org/wiki/Hypocorism) (English only at this time)
* Makes use of a person’s email address (if available) via searching for names and [grammatical gender](https://en.wikipedia.org/wiki/Grammatical_gender) words in the prefix
* Doesn’t care if the input has bad formatting

### Latest Update (22/02/2021)

* added new female names, now 221,647 names in the database

### Previous Update (17/02/2021)

* added new female names, now 193,613 names in the database

### Previous Update (30/07/2020)

* more new names, now 153,508 names in the database

### Previous Update (26/07/2020)

* added new male names, now 144,047 names in the database

### Previous Update (22/11/2019)

* more new names, mostly variations of spelling - now 135,269 names in the database

### Previous Update (21/08/2019)

* added 14 new female names - now 135,167 names in the database

### Previous Update (20/08/2019)

* added 1,034 new male names from fifaindex.com

### Previous Update (26/06/2019)

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