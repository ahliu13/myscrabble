MAX_TRAY_LEN = 7


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.tray = []

    def is_letter_in_tray(self, letter):
        """Checks whether a given letter is in a player's tray"""
        for item in self.tray:
            if item == letter:
                return True
        return False

    def remove_letter(self, letter):
        i = 0
        for i in xrange(0, len(self.tray)):
            item = self.tray[i]
            if item == letter:
                self.tray = self.tray[0: i] + self.tray[i + 1:]
                return  # Early terminating
