# The fighter class with the fighter and its attributes
import random


class Fighter:
    """The fighter competes against other fighters. Has multiple skills and several attributes.
    Skills can be improved with training."""

    def __init__(self, name, weight, height, punch=None, kick=None, grappling=None, luck=None, speed=None,
                 endurance=None, wins=None, losses=None, champion=None):
        # fighter attributes
        self.name = name
        self.weight = weight
        self.height = height
        self.reach = self.height // 2

        # wins of the fighter
        if wins is None:
            self.wins = 0
        else:
            self.wins = self.wins

        # losses of the fighter
        if losses is None:
            self.losses = 0
        else:
            self.losses = self.wins

        # fighter skills
        self.punch = punch
        self.kick = kick
        self.grappling = grappling
        self.luck = luck
        self.speed = speed
        self.endurance = endurance
        self.total_skill_score = self.get_total_skill_score()

        # energy level of the fighter
        self.energy = 10

        # champion status
        if champion is None:
            self.champion = False

        # determine the salary
        self.salary = self.calculate_salary()

    def __str__(self):
        name_adjusted = f'{self.name}{self.display_champion_status()}'.ljust(12)
        total_skill_adjusted = f' ({self.total_skill_score}):'.ljust(6)
        salary_adjusted = f'${self.salary:,}'.rjust(10)
        stats_adjusted = f'{self.weight}KG // {self.height}CM'.rjust(15)
        total_stats_adjusted = f'(P: {self.punch} // K: {self.kick} // G: {self.grappling} // ' \
                               f'S: {self.speed})'.rjust(40)
        base_string = f'{name_adjusted} {total_skill_adjusted} {salary_adjusted} {stats_adjusted} '
        full_fighter_string = base_string + total_stats_adjusted
        return full_fighter_string

    def display_champion_status(self):
        """Simple function to show the champion status of a fighter"""
        champ_string = ""
        if self.champion:
            champ_string = " (C)"
        else:
            print("  ", end="")
        return champ_string

    def get_skills(self):
        """Return the skills of the fighter"""
        return [self.punch, self.kick, self.grappling, self.speed]

    def calculate_salary(self):
        """Determines the salary of a fighter depending on the skills and the fights won"""
        champion_bonus = 1
        if self.champion:
            champion_bonus = 2
        if not self.champion:
            champion_bonus = 1
        skill_factor = 1_000
        win_factor = 25_000
        salary = (self.punch + self.grappling + self.kick + self.speed) * skill_factor \
                 + self.wins * win_factor * champion_bonus
        return salary

    def reset_energy(self):
        """Reset the energy of the fighter back to the normal level (100)"""
        self.energy = 10

    def get_total_skill_score(self):
        """Calculate the total skill score of the fighter"""
        total = self.punch + self.kick + self.grappling + self.speed + self.endurance
        return total

    def get_ranking_string(self):
        """The string that is used to display the fighter in the ranking"""
        champ_status = self.display_champion_status()
        ranking_string = f'{self.name}{champ_status} ({self.total_skill_score})'.ljust(21) \
                         + f'{self.wins} wins // {self.losses} losses'.rjust(20)
        return ranking_string


def generate_fighter():
    """Generate random fighters."""
    first_names = ['Liam', 'Noah', 'James', 'Logan', 'Mason', 'Lucas', 'Henry', 'David', 'Wyatt', 'John', 'Owen',
                   'Dylan', 'Luke', 'Jack', 'Levi', 'Mateo', 'Ryan', 'Jaxon', 'Aaron', 'Asher', 'Leo', 'Nolan', 'Ezra',
                   'Angel', 'Ian', 'Adam', 'Elias', 'Jason', 'Chase', 'Gavin', 'Kevin', 'Tyler', 'Micah', 'Cole',
                   'Luis', 'Ryder', 'Kai', 'Max', 'Diego', 'Luca', 'Ryker', 'Juan', 'Jayce', 'Rowan', 'Jesus', 'Abel',
                   'King', 'Amir', 'Blake', 'Alex', 'Brody', 'Beau', 'Jude', 'Alan', 'Finn', 'Grant', 'Joel', 'Gael',
                   'Rhett', 'Avery', 'Jesse', 'Dean']

    last_names = ['Smith', 'Smith', 'Jones', 'Brown', 'Davis', 'Moore', 'White', 'Clark', 'Lee', 'Allen', 'Young',
                  'Hill', 'Scott', 'Green', 'Adams', 'Baker', 'Perez', 'Reed', 'Cook', 'Gray', 'Kelly', 'Diaz', 'Hayes']

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    first_names.remove(first_name)
    last_names.remove(last_name)

    full_name = f'{first_name} {last_name}'

    # generate their attributes and skills
    height = 100 + random.randint(70, 100)
    weight = height // 3 + random.randint(10, 50)
    reach = height // 2
    punch = reach // 2 + random.randint(20, 60)
    kick = reach // 2 + random.randint(20, 60)
    grappling = 50 + random.randint(10, 50)
    luck = 50 + random.randint(10, 80)
    speed = 50 + random.randint(10, 50) - weight // 3
    endurance = 50 + random.randint(0, 50)
    return Fighter(full_name, weight, height, punch, kick, grappling, luck, speed, endurance)
