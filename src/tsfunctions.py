

from random import randint
import re
import sqlite3
import string

db_location: str = 'projects\\tenser w private\\tenser\\src\\data\\tenser_public.db'

class DiceRoller:
    def __init__(self):
        pass

    def singleDieRoll(self, number_of_dice: int, size_of_dice: int) -> tuple:
        string = f""
        x = 0
        roll = 0
        while x < int(number_of_dice):
            each_result = randint(1, int(size_of_dice))
            roll += each_result
            if x == int(number_of_dice) - 1:
                string += f'{each_result}'
            else:
                string += f'{each_result}, '
            x += 1
        return (string, roll)


    def doubleDiceRoll(self, first_number_of_dice: int, first_size_of_dice: int, second_number_of_dice: int, second_size_of_dice: int):
        first_result = self.singleDieRoll(first_number_of_dice, first_size_of_dice)
        second_result = self.singleDieRoll(second_number_of_dice, second_size_of_dice)
        string = f"({first_result[0]} + {second_result[0]})"
        roll = first_result[1] + second_result[1]
        return (string, roll)


    def diceResult(self, query: str) -> str:
        optl_modifier = 0

        if re.search(r'[rR]oll\s(.*?)', query) is None or re.search(r'[rR]oll\s(\d{1,2})[dD]', query) is None:
            reply = "Could not complete dice rolling request. Max length of expression is xdw+ydz+a. eg. 4d6+2d8-2.\nMax dice amount is 2 digits, max dice size is 4 digits, max modifier is 3 digits"

        #advantage, disadvantage
        elif re.search(r'[aA]dvantage', query) is not None:
            roll1, roll2 = randint(1, 20), randint(1, 20)
            # (\+ or \- \d{1,3}) means we are looking for '+/- a 1-3 digit number' as our modifier
            if mod := re.search(r'\+(\d{1,3})', query) is not None:
                optl_modifier = mod.group(1)
            elif mod := re.search(r'-(\d{1,3})', query) is not None:
                optl_modifier = 0 - int(mod.group(1))

            if re.search(r'[dD]is', query) is not None:
                roll = min(roll1, roll2)
                roll += int(optl_modifier)
                reply = f"Result of rolling 1d20 with disadvantage + {optl_modifier}: {roll}\n({roll1}, {roll2}) + {optl_modifier}"
            else:
                roll = max(roll1, roll2)
                roll += int(optl_modifier)
                reply = f"Result of rolling 1d20 with advantage + {optl_modifier}: {roll}\n({roll1}, {roll2}) + {optl_modifier}"
        
        else: 
            actual_query = re.search(r'[rR]oll\s(.*)?', query).group(1)
            number_of_dice = re.search(r'[rR]oll\s(\d{1,2})[dD]', query).group(1)

            if re.search(r'[dD]\d{1,4}\+\d{1,2}[dD]', query) is not None:
                size_of_dice = re.search(r'[dD](\d{1,4})\+', query).group(1)
                second_number_of_dice = re.search(r'\+(\d{1,2})[dD]', query).group(1)
                second_size_of_dice = re.search(r'\+\d{1,2}[dD](\d{1,4})', query).group(1)
                if mod := re.search(r'\+[dD\d]+\+(\d{1,3})', query) is not None:
                    optl_modifier = mod.group(1)
                elif mod := re.search(r'\+[dD\d]+-(\d{1,3})', query) is not None:
                    optl_modifier = 0 - int(mod.group(1))
                result = self.doubleDiceRoll(number_of_dice, size_of_dice, second_number_of_dice, second_size_of_dice)

            else:
                size_of_dice = re.search(r'[dD](\d{1,4})?', query).group(1)
                if mod := re.search(r'\+(\d{1,3})', query) is not None:
                    optl_modifier = mod.group(1)
                elif mod := re.search(r'-(\d{1,3})', query) is not None:
                    optl_modifier = 0 - int(mod.group(1))
                result = self.singleDieRoll(number_of_dice, size_of_dice)
            
            roll = result[1] + int(optl_modifier)
            reply = f"Result of rolling {actual_query}: {roll}\n{result[0]} + {optl_modifier}"
        return reply
    
# The role of the TSSearch class is to carry out a search and return a text answer.
class TSSearch:
    def __init__(self):
        self.db = sqlite3.connect(db_location)
        self.DBCursor = self.db.cursor()
        self.DBCursor.execute('SELECT MAX(id) FROM spells')
        self.number_of_items = self.DBCursor.fetchall()[0][0]

        self.version_number = 0.41
        self.new_functions = "added support for XGTE and TCoE spells as well as the ability to search by class levels. Added dice rolling feature. Also added behind the scenes web scraping and regex support."
        self.version_functions = "retrieving information about spells from the Player's Handbook (PHB), Xanathar's (XGTE), and " \
                        "Tasha's Cauldron (TCoE) with some attributes missing (such as page numbers)"
        self.attributes = ['id', 'name', 'classes', 'level', 'school', "ritual", "casting_time", "spell_range", "components", "materials", "duration", "description", "source", 'page', 'concentration', 'is_ritual', 'additional']
        self.lowercase_words = {"Or": "or", "Of": "of", "To": "to", "And": "and", "The": "the"}
        self.attributes_string = "name, classes, level, school, ritual, casting_time, spell_range, components, materials, duration, description, source, page, concentration, additional"
        self.column_names = ('Name','Classes','Level','School','Ritual','Casting Time','Spell Range','Components','Materials','Duration','Description','Source','Page','Concentration','Additional')


    def search(self, command: str):
        self.DBCursor.execute(command)
        result = self.DBCursor.fetchall()
        return result

    def oneSpellAllInfo(self, name: str) -> str:
        sql = f'SELECT {self.attributes_string} FROM spells WHERE name = \'{name}\';'
        print(sql)
        search_result = self.search(sql)
        if search_result == []:
            reply = self.noData()
        else:
            reply = f'Results for {name}:\n'
            reply += self.oneSpellInfoText(search_result)
        return reply
    
    def oneSpellOneAttr(self, name: str, attr: str) -> str:
        sql = f'SELECT {attr} FROM spells WHERE name = \'{name}\';'
        print(sql)
        search_result = self.search(sql)
        return search_result[0][0]

    def randomMessage(self):
        random_id = randint(1, self.number_of_items)
        sql = f'SELECT name FROM spells WHERE id = {random_id};'
        rand_spell = self.search(sql)[0][0]
        rand_attr = self.column_names[randint(1, 15)]
        return rand_spell, rand_attr
    
    def noData(self) -> str:
        rand_spell, rand_attr = self.randomMessage()
        return f"Seems like I couldn't find that spell or function in my library... By the way, I only have PHB, XGTE, and TCoE support at the moment." \
            f"\nI'm also a bit picky and need your request to be in the form: tenser spell attribute\nFor example: tenser {rand_spell} {rand_attr}" \
            f"\nTo see a list of my functions, type 'tenser functions'"
    

    def printSpellReply(self, msg: str) -> str:
        message = re.search(r'Tenser\s(.*)?', msg).group(1)
        print(message, type(message))
        filler_word = re.search(r'\s(Of|To|And|Or|The)\s', message)
        if filler_word is not None:  # replace prepositions and articles
            filler_word = filler_word.group(1)
            filler_replacement = self.lowercase_words[filler_word]
            message = re.sub(filler_word, filler_replacement, message)
        last_word_search = re.search(r'(Name|Classes|Class|Level|School|Ritual|Casting\s[tT]ime|Spell\sRange|Range|Components|Materials|Duration|Description|Source|Page|Concentration|Additional)', message)
        
        #if we do have a keyword:
        if last_word_search is not None:
            last_word = last_word_search.group(0)
            if re.search(fr'(.*)\s{last_word}', message) is not None:
                loc_1 = re.search(fr'(.*)\s{last_word}', message)
                spell = loc_1.group(1)
            elif loc_1 is None:
                spell = re.search(fr'{last_word}\s(.*)', message).group(1)
            else:
                reply = self.noData()
            
            ## fix this
            last_word = last_word.lower()
            if last_word == "castingtime" or last_word == "time":
                last_word = "casting_time"
            elif last_word == "class":
                last_word = "classes"
            elif last_word == 'range' or last_word == 'spellrange':
                last_word = "spell_range"
            
            result = self.oneSpellOneAttr(spell, last_word)   
            reply = f'Result for {spell} {last_word}: {result}'
        
        #if we dont have a keyword
        elif last_word_search is None:
            reply = self.oneSpellAllInfo(message)
        return reply
    
    def returnMultipleLineResult(self, list_of_tuples: list) -> str:
        reply = ""
        for item in list_of_tuples:
            reply += f"{item[0]}, "
        return reply
    
    def oneSpellInfoText(self, list_with_one_tuple: list) -> str:
        reply = ""
        for i, item in enumerate(list_with_one_tuple[0]):
            reply += f"{self.column_names[i]}: {item}\n"
        return reply
    
