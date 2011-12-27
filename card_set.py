# card_set.py
# A class for representing a set of Flashcards
# STARTED: 10/14/11
# EDIT: Added Flashcard class based on tuple to keep track of 
#       statistics for individuals flashcards
import random
import codecs

class Flashcard(tuple):
    """Is a subclass of tuple. Represents a single flashcard with front and back
    Has correct and incorrect statistics"""
    def __new__(self, front, back):
        start = [front, back]
        self.correct = 0
        self.incorrect = 0
        return super(Flashcard, self).__new__(self, start)
    
    def percentage(self):
        if (self.incorrect + self.correct > 0):
            return float(self.correct) / (self.correct + self.incorrect)
        else:
            return False
    
    def save(self):
        save_string = u"%s,%s,%d,%d" % (self[0], self[1], self.correct,
                                       self.incorrect)
        return save_string 
        
class FlashcardSet:
    """A class representing a set of flashcards. The data is stored
       in a list of tuples"""
    @staticmethod
    def load_set(filename):
        file = codecs.open(filename, mode="r", encoding='utf-8')
        text = file.read()
        file.close()
        cards_list = text.split("\n")
        final_set = FlashcardSet()
        for line in cards_list:
            L = line.split(",")
            card = Flashcard(L[0], L[1])
            card.correct = int(L[2])
            card.incorrect = int(L[3])
            final_set.cards.append(card)
        return final_set
        
    def __init__(self, cards=None):
        if cards:
            self.cards = cards
        else:
            self.cards = []

    def add(self, front, back):
        self.cards.append(Flashcard(front, back))

    def shuffle(self):
        random.shuffle(self.cards)

    def delete(self, card):
        self.cards.remove(card)

    def replace(self, index, new_front, new_back):
        del self.cards[index]
        self.cards.insert(index, Flashcard(new_front, new_back))
    
    def save_text(self):
        save_list = [card.save() for card in self.cards]
        save_string = u"\n".join(save_list) 
        return save_string
    
    def save(self, filename):
        save_string = self.save_text()
        file = codecs.open(filename, mode="w", encoding='utf-8')
        file.write(save_string)
        file.close()
    
    def sort_by_percentage(self, reverse=False):
        sort_d = {}
        for card in self.cards:
            percent = card.percentage()
            if percent not in sort_d.keys():
                sort_d[percent] = card
            else:
                sort_d[percent + random.random() / 1000] = card
        keys = sort_d.keys()
        keys.sort(reverse=reverse)
        sorted_list = []
        for card_key in keys:
            sorted_list.append(sort_d[card_key])
        self.cards = sorted_list
                
    def __getitem__(self, index):
        return self.cards[index]

    def __delitem__(self, index):
        del self.cards[index]

    def __iter__(self):
        for item in self.cards:
            yield item

    def __str__(self):
        return str(self.cards)

    def __len__(self):
        return len(self.cards)

if __name__ == "__main__":
    import copy
    c = Flashcard('water', 'agua')
    cards = FlashcardSet()
    cards.add("vencer", "to defeat")
    cards.add("conseguir", "to achieve")
    cards.add("perseguir", "to chase")
    print cards
    print cards[1]
    cards.replace(1, "ganar", "to win") 
    #cards.shuffle()
    print cards
    #saved = cards.save_text()
    #print saved
    #loaded = FlashcardSet.load_set(saved)
    #print loaded
    
    print "Begin copying testing"
    print "Old cards: " + str(cards)
    new_cards = FlashcardSet()
    new_cards.cards = cards.cards[:]
    new_cards.add("Hello", "World")
    new_cards.shuffle()
    print "New cards: " + str(new_cards)
    print "Old cards: " + str(cards)
