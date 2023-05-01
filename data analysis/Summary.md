

## Overview/Motivation

To reiterate, tenser.io is a project which allows players of the Wizards of the Coast game Dungeons & Dragons, Fifth Edition, to use a text interface to request information about magic spells, which are a resource in the game. Tenser.io consists of a module of python software and a SQL database containing 479 entries collected from several books.

About a year after starting this project, I realized that collecting data for tenser and bundling it into a convenient SQL database actually presents a great opportunity to do data analysis and present the results visually. In essence, we have a dataset of spells with their properties in a readily accessible format and now have an opportunity to query some descriptive statistics about this body of data and make conclusions about the work.

1. Which base classes have access to the most spells?
2. What proportions of spells are associated with which schools? Are there any surprising results?
3. Are the proportions of spells by school the same for all classes? Where are the differences from the average large?
4. Which classes received buffs (increases in scope) in expansions?
5. Are there correlations across levels (eg. higher level spells having longer names)?


## Methodology

I used SQLite3 to peruse and select features from the data. Exploratory data analysis was carried out in Excel. 

Figures were generated using Plotly's python library.


## Findings



##### Complications
The


## Conclusion


## Glossary

- buff: A slang-ish term for when developers of a game increase the abilities of one of the classes or roles a player can take on. 
- class: A bundle of specialties, properties, and flaws which define a player's character, similar to a vocation.
- school: Short for 'school of magic', a property spells have in the game which determines their use. By analogy, this is similar to how a starter pistol and a rifle are both firearms, but with vastly different uses.
- spell: A resource in the game which can be used to create effects of all kinds.
- subclass: A specialty which extends and specializes the abilities of class.