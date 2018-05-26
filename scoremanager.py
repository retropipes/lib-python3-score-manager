import pickle

class Score(object):
    # Constructor
    def __init__(self, new_score=0, new_name="Nobody"):
        self.score = new_score
        self.name = new_name

    # Methods
    def get_score(self):
        return self.score

    def get_name(self):
        return self.name

    def set_score(self, new_score):
        self.score = new_score

    def set_name(self, new_name):
        self.name = new_name

class ScoreTable(object):
    # Constructor
    def __init__(self, length=10, custom_unit=""):
        self.table = list()
        self.table.append(Score()) * length
        if custom_unit == None:
            self.unit = ""
        else:
            self.unit = " " + custom_unit

    # Methods
    def get_entry_score(self, pos):
        return self.table[pos].get_score()

    def get_entry_name(self, pos):
        return self.table[pos].get_name()

    def get_length(self):
        return len(self.table)

    def get_unit(self):
        return self.unit

    def set_entry_score(self, pos, new_score):
        self.table[pos].set_score(new_score)

    def set_entry_name(self, pos, new_name):
        self.table[pos].set_name(new_name)

class SortedScoreTable(ScoreTable):
    # Constructor
    def __init__(self, length=10, ascending=True, starting_score=0, custom_unit=""):
        ScoreTable.__init__(self, length, custom_unit)
        self.ascending = ascending
        for x in range(0, len(self.table) - 1):
            self.table[x].set_score(starting_score)

    def set_entry_score(self, pos, new_score):
        pass

    def set_entry_name(self, pos, new_name):
        pass

    def add_score(self, new_score, new_name):
        new_entry = Score(new_score, new_name)
        self.table.append(new_entry)
        self.table.sort()
        if not self.ascending:
            self.table.reverse()
        del self.table[-1]

    def check_score(self, new_score):
        if self.ascending:
            for x in range(0, len(self.table) - 1):
                if new_score > self.table[x].get_score():
                    break
            if x == len(self.table):
                return False
        else:
            for x in range(0, len(self.table) - 1):
                if new_score < self.table[x].get_score():
                    break
            if x == len(self.table):
                return False
        return True

class ScoreManager(object):
    # Constructor
    def __init__(self, length=10, ascending=True, starting_score=0, custom_unit=""):
        self.table = SortedScoreTable(length, ascending, starting_score, custom_unit)
        self.name = ""

    # Methods
    def add_score(self, new_score, new_name="Nobody"):
        success = self.table.check_score(new_score)
        if success:
            self.table.add_score(new_score, new_name)
        return success

    def check_score(self, new_score):
        return self.table.check_score(new_score)

class SavedScoreManager(ScoreManager):
    # Constructor
    def __init__(self, scores_file, length=10, ascending=True, starting_score=0, custom_unit=""):
        ScoreManager.__init__(self, length, ascending, starting_score, custom_unit)
        self.scores_filename = scores_file
        self.read_scores()

    # Methods
    def add_score(self, new_score, new_name="Nobody"):
        success = ScoreManager.add_score(self, new_score, new_name)
        self.write_scores()
        return success

    def read_scores(self):
        try:
            f = open(self.scores_filename)
            self.table = pickle.load(f)
            f.close()
        except IOError:
            pass

    def write_scores(self):
        try:
            f = open(self.scores_filename)
            pickle.dump(self.table, f)
            f.close()
        except IOError:
            pass