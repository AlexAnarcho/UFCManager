# The manager class that manages one fighter in a league
import inquirer
import random


class Manager:

    def __init__(self, available_fighters, league, fighter=None, money=None):
        self.league = league
        self.available_fighters = available_fighters
        self.active_flag = False
        self.training_flag = True
        self.training_factor = 1

        # Give the manager a starting budget
        if money is None:
            self.money = 1_000_000
        else:
            self.money = money

        # Let the manager pick a starting fighter
        if fighter is None:
            self.fighter = self.pick_fighter()
        else:
            self.fighter = self.fighter

        self.wins = 0
        self.losses = 0

    def __str__(self):
        return f'You are managing {self.fighter}'

    def main_menu(self):
        """The main menu to select various options"""
        options = [
            'Fight Round',
            'Overview',
            'Train Fighter',
            'Heal Fighter',
            'View Ranking',
            'Switch Fighter',
                   ]
        menu = options
        question = [
            inquirer.List('main_choice',
                          message='What do you want to do? ',
                          choices=menu,
                          carousel=True
                          ),
        ]
        answer = inquirer.prompt(question)
        choice = answer["main_choice"]

        # process the choice
        if choice == "Fight Round":
            self.check_fighter_health()
            self.active_flag = True
            self.training_flag = True
        elif choice == "Train Fighter":
            self.train_fighter()
            self.training_flag = False
            self.fighter.salary = self.fighter.calculate_salary()
        elif choice == 'Overview':
            self.view_stats()
        elif choice == 'Heal Fighter':
            self.heal_fighter()
        elif choice == 'Switch Fighter':
            self.switch_fighter()
        elif choice == 'View Ranking':
            self.league.menu_of_league_fighters()

    def pick_fighter(self):
        """In the beginning of the game, pick a fighter with a menu"""
        menu = self.available_fighters
        question = [
            inquirer.List('fighter_choice',
                          message='Pick your fighter',
                          choices=menu,
                          carousel=True,
                          validate=True,
                          ),
        ]
        answer = inquirer.prompt(question)
        choice = answer["fighter_choice"]
        print(f'You chose to manage {choice}')
        return choice

    def train_fighter(self):
        """Improve one skill of the fighter"""
        if self.training_flag:
            menu = ['Punching', 'Kicking', 'Grappling', 'Speed', 'Endurance']
            question = [
                inquirer.List('skill_choice',
                              message='What skill do you want to train?',
                              choices=menu,
                              carousel=True
                              ),
            ]
            answer = inquirer.prompt(question)
            choice = answer["skill_choice"]
            training_string = '--- TRAINING ' + choice.upper() + ' ---'
            print(training_string.center(40))
            trained_skill = 0
            improvement = random.randint(1, 5)
            if answer["skill_choice"] == 'Punching':
                self.fighter.punch += improvement
                trained_skill = self.fighter.punch
            elif answer["skill_choice"] == 'Kicking':
                self.fighter.kick += improvement
                trained_skill = self.fighter.kick
            elif answer["skill_choice"] == 'Grappling':
                self.fighter.grappling += improvement
                trained_skill = self.fighter.grappling
            elif answer["skill_choice"] == 'Speed':
                self.fighter.speed += improvement
                trained_skill = self.fighter.speed
            elif answer["skill_choice"] == 'Endurance':
                self.fighter.endurance += improvement
                trained_skill = self.fighter.endurance
            self.fighter.salary = self.fighter.calculate_salary()
            print(f'Your fighter increased their {choice} by {improvement}.\n'
                  f'Now the {choice} is {trained_skill}.\n'
                  f"Your fighter's salary is now ${self.fighter.salary:,}")
            print(training_string.center(40))
            self.fighter.total_skill_score = self.fighter.get_total_skill_score()
        else:
            print("--- TRAINING ERROR ---".center(40))
            print("Sorry, you already trained your fighter this round.")
            print("--- TRAINING ERROR ---\n".center(40))
            self.pay_training_premium()

    def pay_training_premium(self):
        training_premium = self.fighter.salary // 6 * self.training_factor
        if not self.money - training_premium < 0:
            question = [
                inquirer.List('pay_premium',
                              message=f"Would you like to pay ${training_premium:,} to continue training?",
                              choices=['Yes', 'No'],
                              default='Yes',
                              ),
            ]
            answer = inquirer.prompt(question)
            choice = answer['pay_premium']
            if choice == 'Yes':
                self.money -= training_premium
                self.training_flag = True
                self.train_fighter()
                self.training_factor += 1
            self.check_money()
        else:
            print("--- YOU ARE ALMOST BROKE! ---".center(40))
            print("Careful, not enough money left for the training.")
            print(f"Money in the bank: ${self.money:,}")
            print("--- YOU ARE ALMOST BROKE! ---\n".center(40))

    def pick_opponent(self):
        """Choosing who to fight against"""
        menu = self.league.fighters
        question = [
            inquirer.List('opponent_choice',
                          message='Pick your opponent ',
                          choices=menu,
                          carousel=True
                          ),
        ]
        answer = inquirer.prompt(question)
        choice = answer['opponent_choice']
        print(f'You chose to fight {choice}\nPrepare for war...\n')
        return choice

    def boost_stat_during_fight(self):
        """Give your fighter a temporary boost to one stat"""
        menu = ['Punching', 'Kicking', 'Grappling', 'Speed']
        question = [
            inquirer.List('boost_choice',
                          message='Pick a skill to boost ',
                          choices=menu,
                          carousel=True
                          ),
        ]
        answer = inquirer.prompt(question)
        choice = answer['boost_choice']
        improvement = random.randint(1, 10)  # boost will give a random number
        if choice == 'Punching':
            self.fighter.punch += improvement
        elif choice == 'Kicking':
            self.fighter.kick += improvement
        elif choice == 'Grappling':
            self.fighter.grappling += improvement
        elif choice == 'Speed':
            self.fighter.speed += improvement
        print(f'Boosting {choice} by {improvement}.\n')
        return choice, improvement

    def deboost_fighter_stats(self, boosted_stat, improvement):
        """Deboost the fighters stats after the fight"""
        if boosted_stat == 'Punching':
            self.fighter.punch -= improvement
        elif boosted_stat == 'Kicking':
            self.fighter.kick -= improvement
        elif boosted_stat == 'Grappling':
            self.fighter.grappling -= improvement
        elif boosted_stat == 'Speed':
            self.fighter.speed -= improvement

    def pay_fighter(self):
        """Pay the fighter their salary"""
        self.money -= self.fighter.salary

    def check_money(self):
        """Determine if the manager is broke or not"""
        if self.money <= 0:
            print()
            print(f'--- GAME OVER ---'.center(40))
            print(f'--- YOU ARE BROKE ---'.center(40))
            print(f'--- GAME OVER ---\n'.center(40))
            exit()

    def view_stats(self):
        """Show the stats of the fighter and the manager"""
        total_skill_string = f'Total Skill:'.ljust(13) + str(self.fighter.total_skill_score).rjust(4)
        punching_string = f'Punching:'.ljust(13) + str(self.fighter.punch).rjust(4)
        kicking_string = f'Kicking:'.ljust(13) + str(self.fighter.kick).rjust(4)
        grappling_string = f'Grappling:'.ljust(13) + str(self.fighter.grappling).rjust(4)
        speed_string = f'Speed:'.ljust(13) + str(self.fighter.speed).rjust(4)
        endurance_string = f'Endurance:'.ljust(13) + str(self.fighter.endurance).rjust(4)

        print(f'--- {self.fighter.name.upper()} ---'.center(40))
        print('Height:'.ljust(14) + str(self.fighter.height) + ' CM' .ljust(3))
        print('Weight:'.ljust(14) + str(self.fighter.weight) + ' KG'.ljust(3))
        print('Salary:'.ljust(14) + '$ ' + f'{self.fighter.salary:,}'.ljust(3))
        print('Energy Level:'.ljust(14) + str(self.fighter.energy).ljust(3))
        print('Champion:'.ljust(14) + str(self.fighter.champion).ljust(3))
        print()
        print('--- Fighting Record ---'.center(40))
        print('Wins:'.ljust(8) + str(self.fighter.wins).rjust(3))
        print('Losses:'.ljust(8) + str(self.fighter.losses).rjust(3))
        print()
        print('--- Fighter Skills ---'.center(40))
        print()
        print(total_skill_string)
        print()
        print(punching_string)
        print(kicking_string)
        print(grappling_string)
        print(speed_string)
        print(endurance_string)
        print()
        print('--- Manager View ---'.center(40))
        print(f'Money in the Bank: ${self.money:,}')
        print(f'Wins:'.ljust(8) + str(self.wins).rjust(3))
        print(f'Losses:'.ljust(8) + str(self.losses).rjust(3))

    def heal_fighter(self):
        """Heal the players energy"""
        if self.fighter.energy < 10:
            price = round((10 - self.fighter.energy) * self.fighter.salary // 5)
            self.money -= price
            self.fighter.energy = 10
            print(f'Your fighter is back to full energy. This cost you ${price:,}.')
            print(f'You have ${self.money:,} left.')
        else:
            print('Your fighter is already fully healed.')
            self.check_money()

    def switch_fighter(self):
        """Allows the manager to switch the fighter"""
        new_fighter = self.pick_fighter()
        menu = ['Yes', 'No']
        question = [
            inquirer.List('confirm',
                          message='Are you sure you want to switch the fighter?',
                          choices=menu,
                          default='No')
        ]
        answer = inquirer.prompt(question)
        choice = answer['confirm']
        if choice == 'Yes':
            old_fighter = self.fighter
            print(f'Switching {old_fighter.name} for {new_fighter.name}...')
            self.league.fighters.append(old_fighter)
            self.money += self.fighter.salary
            self.league.fighters.remove(new_fighter)
            self.fighter = new_fighter

    def check_fighter_health(self):
        """Before the fight starts, if the fighter is not full energy, ask the manager if he really wants to fight"""
        if self.fighter.energy != 10:
            price = round((10 - self.fighter.energy) * 20_000) + 100_000
            print('--- WARNING ---')
            print('Your fighter is not full energy.')
            if self.money > price:
                menu = ['Heal fighter', 'Fight with lower energy']
                question = [
                    inquirer.List('confirm',
                                  message=f'Do you want to heal your fighter before the fight for ${price:,}?',
                                  choices=menu,
                                  ),
                ]
                answer = inquirer.prompt(question)
                choice = answer['confirm']
                if choice == 'Heal fighter':
                    self.heal_fighter()
            else:
                print(f"You don't have enough money to heal fighter")
                print(f"Your fighter will fight with an energy level of {self.fighter.energy}.\n")

    def training_camp(self):
        """At the end of the season the manager can boost one stat"""
        menu = ['Punching', 'Kicking', 'Grappling', 'Speed', 'Endurance']
        question = [
            inquirer.List('Training Camp',
                          message=f'Choose one stat to boost in training camp ',
                          choices=menu,
                          carousel=True,
                          ),
        ]
        answer = inquirer.prompt(question)
        choice = answer['Training Camp']
        improvement = 10 + random.randint(5, 15)
        if choice == 'Punching':
            self.fighter.punch += improvement
        elif choice == 'Kicking':
            self.fighter.kick += improvement
        elif choice == 'Grappling':
            self.fighter.grappling += improvement
        elif choice == 'Speed':
            self.fighter.speed += improvement
        elif choice == 'Endurance':
            self.fighter.endurance += improvement
        print(f'Training camp improved {choice} by {improvement}\n')
