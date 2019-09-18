# The league holds multiple players
from game import MatchUp
from fighter import *
import inquirer


class League:
    def __init__(self, fighters, name='UFC Campionship', champion=None):
        self.name = name
        self.fighters = fighters
        self.champion = champion
        self.league_fighters = fighters
        self.rounds_fought = 0
        self.seasonal_boost = 5

    def automatic_training_fighters(self):
        """Automatically train the AI fighters"""
        skills = ['Punching', 'Kicking', 'Grappling', 'Speed', 'Endurance', 'Nothing']
        for fighter in self.fighters:
            improvement = random.randint(1, 3)
            training_skill = random.choice(skills)
            if training_skill == "Punching":
                fighter.punch += improvement
            elif training_skill == "Kicking":
                fighter.kick += improvement
            elif training_skill == "Grappling":
                fighter.grappling += improvement
            elif training_skill == "Speed":
                fighter.speed += improvement
            elif training_skill == "Endurance":
                fighter.endurance += improvement
            elif training_skill == "Nothing":
                continue
            fighter.salary = fighter.calculate_salary()
            fighter.total_skill_score = fighter.get_total_skill_score()

    def automatic_fight_against_each_other(self, opponent):
        """The other fighters fight each other automatically, while the managed fighter fights a picked opponent"""
        self.fighters.remove(opponent)
        ai_fighters = self.fighters[:]
        print()
        print('--- OTHER FIGHTS ---'.center(40))
        while len(ai_fighters) > 1:
            ai_fighter_1 = random.choice(ai_fighters)
            ai_fighters.remove(ai_fighter_1)
            ai_fighter_2 = random.choice(ai_fighters)
            ai_fighters.remove(ai_fighter_2)
            game = MatchUp(ai_fighter_1, ai_fighter_2)
            ai_1_boosted_skill, ai_1_improvement = game.boost_random_stat()
            ai_2_boosted_skill, ai_2_improvement = game.boost_random_stat()
            score_ai_fighter_1, score_ai_fighter_2 = game.weighted_ai_skills()
            # carry out the fight
            game.carry_out_ai_fight(score_ai_fighter_1, score_ai_fighter_2)
            # store the winner for reward payout
            game.resolve_ai_fight()
            # remove the boost from the fighter skill
            game.deboost_random_stat(ai_1_boosted_skill, ai_1_improvement)
            game.deboost_random_stat(ai_2_boosted_skill, ai_2_improvement)
            ai_fighter_1.reset_energy()
            ai_fighter_2.reset_energy()
        self.fighters.append(opponent)
        print('--- OTHER FIGHTS ---\n'.center(40))

    def league_ladder(self):
        """Lists the fighters in the league with their record, most wins is at the top"""
        placement = 1
        print()
        print('--- LADDER OF THE LEAGUE ---'.center(40))
        self.print_champions()
        for fighter in sorted(self.league_fighters, key=lambda t: -t.wins):
            if fighter.champion:
                print('(C) ', end="")
            print(f'{placement}. {fighter.name} ({fighter.total_skill_score})'.ljust(21)
                  + f'{fighter.wins} wins // {fighter.losses} losses'.rjust(20))
            placement += 1
        print()

    def get_league_fighters(self, managed_fighter):
        """Add the managed fighter to the league"""
        self.league_fighters = self.fighters[:]
        if managed_fighter not in self.league_fighters:
            self.league_fighters.append(managed_fighter)

    def print_champions(self):
        """List all the champions in the league (there can be multiple)"""
        champions = 0
        for fighter in self.league_fighters:
            if not champions and not fighter.wins == 0:
                self.make_champion()
            if fighter.champion:
                print(f'{fighter.name} is champion\n'.center(40))
                champions += 1

    def make_champion(self):
        """Name one champion if there are non"""
        placement = 1
        for fighter in sorted(self.league_fighters, key=lambda t: -t.wins):
            if placement == 1:
                fighter.champion = True
            placement += 1

    def remove_fighters_from_league(self):
        """Drop the 7 worse fighters from the league.
        If the managers fighter is dropped, he has to choose a new fighter"""
        placement = 1
        for fighter in sorted(self.league_fighters, key=lambda t: -t.wins):
            if placement > 3:
                print(f'{fighter.name} quits the league.')
                if fighter in self.league_fighters:
                    self.league_fighters.remove(fighter)
                if fighter in self.fighters:
                    self.fighters.remove(fighter)
            placement += 1

    def add_new_fighters(self):
        """Generate new players for the next season"""
        for i in range(7):
            new_fighter = generate_fighter()
            self.after_season_boost(new_fighter)
            self.fighters.append(new_fighter)
            self.league_fighters.append(new_fighter)

    def after_season_boost(self, fighter):
        """Boost the stats of the fighters after the season"""
        fighter.endurance += self.seasonal_boost + random.randint(5, 10)
        fighter.speed += self.seasonal_boost + random.randint(5, 10)
        fighter.punch += self.seasonal_boost + random.randint(5, 10)
        fighter.kick += self.seasonal_boost + random.randint(5, 10)
        fighter.grappling += self.seasonal_boost + random.randint(5, 10)
        fighter.salary = fighter.calculate_salary()
        fighter.total_skill_score = fighter.get_total_skill_score()

    def boost_league(self):
        """Loop through fighters and boost their stats"""
        for fighter in self.fighters:
            self.after_season_boost(fighter)
        self.seasonal_boost += 15

    @staticmethod
    def get_num_end_season():
        """Let the player decide how many seasons he wants to play"""
        question = [
            inquirer.Text('num_end_season',
                          message="How many seasons do you want to play ",)
        ]
        answer = inquirer.prompt(question)
        choice = answer['num_end_season']
        return choice

    def menu_of_league_fighters(self):
        """When the manager views the ranking from the main menu, he has the option to view details of fighters"""
        placement = 1
        fighters = []
        print()
        print('--- LADDER OF THE LEAGUE ---'.center(40))
        for fighter in sorted(self.league_fighters, key=lambda t: -t.wins):
            fighters.append(fighter.get_ranking_string())
            placement += 1
        fighters.append('exit')
        print()
        question = [
            inquirer.List('league_fighter',
                          message="Select a fighter to view in-depth statistics ",
                          choices=fighters,
                          default='exit',
                          carousel=True)
        ]
        answer = inquirer.prompt(question)
        choice = answer['league_fighter']
        if choice != 'exit':
            for fighter in self.league_fighters:
                if choice[:10] in str(fighter):
                    self.show_fighter_stats(fighter)

    @staticmethod
    def show_fighter_stats(fighter):
        """Show the stats of the league fighter"""
        punching_string = f'Punching:'.ljust(13) + str(fighter.punch).rjust(4)
        kicking_string = f'Kicking:'.ljust(13) + str(fighter.kick).rjust(4)
        grappling_string = f'Grappling:'.ljust(13) + str(fighter.grappling).rjust(4)
        speed_string = f'Speed:'.ljust(13) + str(fighter.speed).rjust(4)
        endurance_string = f'Endurance:'.ljust(13) + str(fighter.endurance).rjust(4)

        print(f'--- {fighter.name.upper()} ---'.center(40))
        print('Height:'.ljust(14) + str(fighter.height) + ' CM'.ljust(3))
        print('Weight:'.ljust(14) + str(fighter.weight) + ' KG'.ljust(3))
        print('Salary:'.ljust(14) + '$ ' + f'{fighter.salary:,}'.ljust(3))
        print('Champion:'.ljust(14) + str(fighter.champion).ljust(3))
        print()
        print('--- Fighting Record ---'.center(40))
        print('Wins:'.ljust(8) + str(fighter.wins).rjust(3))
        print('Losses:'.ljust(8) + str(fighter.losses).rjust(3))
        print()
        print(f'--- Fighter Skills ({fighter.get_total_skill_score()}) ---'.center(40))

        print(punching_string)
        print(kicking_string)
        print(grappling_string)
        print(speed_string)
        print(endurance_string)
        print()
