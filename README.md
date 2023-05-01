# tenser.io The 5eSRD Helper Bot

### Spencer G.
### version 0.41 ready 03_21_2022


##### What is Tenser?
Tenser.io is a bot for the text chat application Discord. It consists of a Discord bot, a python module and a SQLite3 database file. The bot itself acts as an autonomous account and can receive and send messages in the rooms which it has been invited to. The python module connects to the Discord API, handles logic and inputs, and returns a response by passing a message object to the bot. The database only exists to hold information, and all of the querying is done by the python module.
Because this involves handling copyrighted data, provided is a small public SQLite3 sandbox database with just the first 100 entries covered under the 5eSRD.

##### Features:
PHB, XGTE, TCoE spell lookups with reasonable wiggle room for upper/lowercase inputs
PHB, XGTE, TCoE spell specifics by keyword
dice rolling function using natural language
  eg. tenser roll 4d6, tenser roll 2d8+4, tenser roll advantage+9
spell lookup by attribute
  eg. tenser spells sorcerer 3, tenser artificer cantrips

##### Changelog:
version_number = 0.01   02_05_2022
"framework in place to retrieve information about spells from the Player's Handbook (PHB)."

version_number = 0.11
"added support for XGTE and TCoE spells. Added behind the scenes web scraping and regex support, so adding and parsing the data is now smoother."

version_number = 0.21   03_16_2022
new: "added support for XGTE and TCoE spells as well as the ability to search by class levels. Added dice rolling feature. Also added additional behind the scenes web scraping and regex support. can now retrieve information about spells from the Player's Handbook (PHB), Xanathar's (XGTE), and Tasha's Cauldron (TCoE) with some attributes missing (such as page numbers)"

version_number = 0.31   03_03_2023
new: "added MYSQL support and migrated data to a MYSQL database. Cleaned up spaghetti code and separated code to make a more pythonic module structure"

version_number = 0.41   began 03_21_2023
new: "created a SQLite compatible variant for public use. Extended data to 17 columns from 13 and cleaned some typos within the data. Began exploratory data analysis.