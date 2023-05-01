

import tsfunctions
import re
import string
from random import randint



# we want to follow command-query separation here. a function should either act, or return a result, but not both.
# the role of the TSParser class is to parse a text message for meaning and return a reply. It creates an object of the TSSearch class when initialized.
class TSParser:
    def __init__(self):
        self.Search = tsfunctions.TSSearch()
        self.DiceRoller = tsfunctions.DiceRoller()
    
    def randomMessage(self):
        return self.Search.randomMessage()
    
    def parseMessage(self, user, query: str) -> str:
        query = string.capwords(query)

        if query.startswith('Hello Tenser'):
            reply = f'Hello, {user.name}!'

        
        elif re.search(r'Is\sTenser\sReady', query) is not None:
                rand_spell, rand_attr = self.randomMessage()
                reply = f"My identify spell is ready if you see the following random spell and attribute: {rand_spell} {rand_attr}."

        elif query.startswith('Tenser'):
            if query.startswith('Tenser Help'):
                reply = f"I'm tenser, the discord bot created to save you time, tears, and papercuts while looking up information from the DnD5e SRD."\
                        f"\nMy main functions are limited at the moment to {self.version_functions}. Some of the highlights of version {self.version_number} include {self.new_functions}"\
                        f"\nWe might add support for class features and feats, items, monsters, and more in the future."\
                        f"\nTo learn how to use my functions, type 'tenser functions'."\
                        f"\nNote: tenser cannot save, divert, avoid, or otherwise exculpate adventurers from the risks of fireballs, wild magic surges, rogue elementals, falling rocks, metagaming, or a vengeful DM."

            elif re.search(r'[tT]enser(.*)[sS]pells', query) is not None or re.search(r'[tT]enser\s[sS]pells(.*?)', query) is not None or re.search(r'[tT]enser\s(.*?)[cC]antrip(.*?)', query) is not None:
                reply = self.leveledSpellSearch(query)

            elif re.search(r'[rR]oll\s(.*?)[dD]', query) is not None:
                reply = self.DiceRoller.diceResult(query)

            elif query.startswith('Tenser Functions'):
                rand_spell, rand_attr = self.randomMessage()
                reply = f"\nTo search for a spell, I need your request to be in the form: 'tenser spell' or 'tenser spell attribute'"\
                        f"\nFor example: tenser {rand_spell} {rand_attr}.\nIf you're sure you formatted a spell correctly, then perhaps the archives are incomplete."\
                        f"\nAttributes available for search are the following: \n{self.attributes_string}"\
                        f"\nYou can also list spells by level using the keywords 'spells' or 'cantrips' following this syntax:\ntenser spells cleric 3 (or) tenser druid 5 spells (or) tenser wizard cantrips (or) tenser cantrips artificer." \
                        f"\nYou can roll dice and see the results by putting your request in the following form:\n'tenser roll 1d20', 'tenser roll 8d6-5', 'tenser roll 2d6+3d8+5', or 'tenser roll advantage+6'"\
                        f"\nFinally, you can pull up random facts by typing 'tenser random fact' or 'tenser random spell'"

                ## This one needs to be fixed. How to print a block of 
            elif re.search(r'[rR]andom', query) is not None:
                rand_spell, rand_attr = self.Search.randomMessage()
                if query.startswith('Tenser Random Spell'):
                    random_spell = self.Search.oneSpellAllInfo(rand_spell)
                    reply = f"I've looked into my archives for a random spell and found one just for you:\n{random_spell}"
                elif query.startswith('Tenser Random Fact'):
                    rand_ind_attr = randint(0, 15)
                    if rand_ind_attr > 11 and rand_ind_attr < 16:
                        reply = f"Did you know that there are 355 spells in the PHB, and {self.Search.number_of_items} in this database?"
                    else:
                        rand_attr_result = self.Search.oneSpellOneAttr(rand_spell, rand_attr)
                        reply = f"Did you know that the {rand_attr} of the spell {rand_spell} is {rand_attr_result}?"

            elif re.search(r'Tenser\s(.*)?', query) is None:
                    reply = self.Search.noData()

            else: 
                reply = self.Search.printSpellReply(query)

        return reply


    def leveledSpellSearch(self, line):
        if re.search(r'[cC]antrip', line) is not None:
            level = 0
        elif re.search(r'\d', line) is not None:
            level = re.search(r'\d', line).group()
        else:
            reply = self.Search.noData()
        caster_class = re.search(r'[aA]rtificer|[bB]ard|[cC]leric|[dD]ruid|[pP]aladin|[rR]anger|[sS]orcerer|[wW]arlock|[wW]izard', line).group().capitalize()
        
        sql = f'SELECT name FROM spells WHERE level = {level} AND classes LIKE \'%{caster_class}%\''
        result = self.Search.search(sql)

        if len(result) == 0:
            reply = f"No entries found for the {caster_class} class and spell level {level}."
        else:
            if level == 0:
                level = "cantrips"
            else:
                level = f"level {level} spells"
            reply = f"Here are the results for {caster_class} {level}:\n"
            reply += self.Search.returnMultipleLineResult(result)
        return reply


