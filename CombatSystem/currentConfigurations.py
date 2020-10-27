import _pickle
import pickle


class playCombatConfig:
    def __init__(self):
        self.health = 375
        self.stunTime = 1500
        self.maxCapacityStun = 100
        self.maxCapacityMagicBar = 100
        self.moveX = 6
        self.moveY = 20
        self.damageMultiplier = 1
        self.stunMultiplier = 1
        self.autoAim = True
        self.difficulty = 1
        self.gunSlots = 6
        # 1 is the lowest, 10 is highest


class playerConfig:
    def __init__(self, filename):
        self.config = None
        self.filename = filename

    def read(self):
        try:
            with open('assets/' + self.filename, 'rb') as file:
                self.config = pickle.load(file)
        except FileNotFoundError:
            # No previous configurations exist, ie: game files are deleted or no save-file exists
            self.config = playCombatConfig()
            self.write()
        except _pickle.UnpicklingError:
            self.config = playCombatConfig()

        if not isinstance(self.config, playCombatConfig):
            raise Exception('Invalid config File/ Data corrupted')
        return self.config

    def write(self):
        if self.config is not None:
            with open('assets/' + self.filename, 'wb') as file:
                pickle.dump(self.config, file, pickle.HIGHEST_PROTOCOL)
