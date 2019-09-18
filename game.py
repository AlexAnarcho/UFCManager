# The game class includes the logic for matchups
import random


class MatchUp:
    """Two fighters are involved in a matchup
    The matchup belongs to a league."""

    def __init__(self, fighter_1, fighter_2):
        self.fighter_1 = fighter_1
        self.fighter_2 = fighter_2

        self.round_number = 0
        self.round_win = 0
        self.fighter_1_rounds_won = 0
        self.fighter_2_rounds_won = 0

    def weighted_skills(self):
        """Logic of the fight, who will win which round and so on.
        Weight the different skills, "heavier" skills will be more important.
        Multiply the weigh by the actual skill and add them all up to come up with a final score
        """
        weigh_punch = round(random.random(), 2)
        weigh_kick = round(random.random(), 2)
        weigh_grappling = round(random.random(), 2)
        weigh_speed = round(random.random(), 2)
        if weigh_punch > weigh_kick and weigh_punch > weigh_grappling and weigh_punch > weigh_speed:
            print('\nLooks like this will be a boxing match!')
        if weigh_kick > weigh_punch and weigh_kick > weigh_grappling and weigh_kick > weigh_speed:
            print('\nThe kicking will really matter here!')
        if weigh_grappling > weigh_kick and weigh_grappling > weigh_punch and weigh_grappling > weigh_speed:
            print('\nThe better Jiu-Jitsu Ka has definitely the upper hand!')
        if weigh_speed > weigh_kick and weigh_speed > weigh_grappling and weigh_punch < weigh_speed:
            print('\nSpeed will have a big factor in this fight!')
        print()
        summed_score_fighter_1 = self.fighter_1.punch * weigh_punch + weigh_kick * self.fighter_1.kick \
                                 + self.fighter_1.grappling * weigh_grappling + self.fighter_1.speed * weigh_speed \
                                 + self.fighter_1.luck * 2
        summed_score_fighter_2 = self.fighter_2.punch * weigh_punch + weigh_kick * self.fighter_2.kick \
                                 + self.fighter_2.grappling * weigh_grappling + self.fighter_2.speed * weigh_speed \
                                 + self.fighter_2.luck * 2
        return summed_score_fighter_1, summed_score_fighter_2

    def calculate_stats_with_energy(self, score_fighter_1, score_fighter_2):
        """Includes the energy level in the summed score of the fighters"""
        score_fighter_1 *= self.fighter_1.energy / 10
        score_fighter_2 *= self.fighter_2.energy / 10
        return score_fighter_1, score_fighter_2

    def fight_round(self, score_fighter_1, score_fighter_2):
        """Fight one round and subtract from the fighters energy"""
        energy_consumption = random.randint(50, 120)
        if energy_consumption > 90:
            print('The fighters are going to war!')
        elif energy_consumption < 67:
            print('A rather boring round...')
        else:
            print('A good fight.')

        # compare the fighters scores to find a winner
        if score_fighter_1 > score_fighter_2:
            self.fighter_1_rounds_won += 1
            print(f'{self.fighter_1.name} wins the round!')
        if score_fighter_2 > score_fighter_1:
            self.fighter_2_rounds_won += 1
            print(f'{self.fighter_2.name} wins the round!')

        percentage_energy_fighter_1 = energy_consumption / self.fighter_1.endurance
        percentage_energy_fighter_2 = energy_consumption / self.fighter_2.endurance

        if percentage_energy_fighter_1 > 1:
            self.fighter_1.energy -= percentage_energy_fighter_1
            print(f'This round really took a toll on {self.fighter_1.name}')
        if percentage_energy_fighter_2 > 1:
            self.fighter_2.energy -= percentage_energy_fighter_2
            print(f'This round really took a toll on {self.fighter_2.name}')

    def carry_out_manager_fight(self, score_fighter_1, score_fighter_2):
        """The logic of the actual fight"""
        score_fighter_1 *= self.fighter_1.energy / 100
        score_fighter_2 *= self.fighter_2.energy / 100
        num_rounds = 4
        if self.fighter_1.champion or self.fighter_2.champion:
            num_rounds += 2
            print("THE FIGHT FOR THE CHAMPIONSHIP!".center(40))
        for i in range(1, num_rounds):
            print(f'--- ROUND {i} ---'.center(40))
            winner = ""
            loser = ""
            # logic for knockout
            if abs(self.fighter_1.energy - self.fighter_2.energy) >= 3:
                if self.fighter_1.energy > self.fighter_2.energy:
                    winner = self.fighter_1.name
                    loser = self.fighter_2.name
                    self.fighter_1_rounds_won = 10
                elif self.fighter_1.energy < self.fighter_2.energy:
                    winner = self.fighter_2.name
                    loser = self.fighter_1.name
                    self.fighter_2_rounds_won = 10
                print('OH MY GOD! IT IS ALL OVER!!!')
                print(f'{winner} knocked out {loser}\n')
                break
            self.fight_round(score_fighter_1, score_fighter_2)  # fight one round
            score_fighter_1, score_fighter_2 = self.calculate_stats_with_energy(score_fighter_1, score_fighter_2)
            print(f'--- ROUND {i} ---\n'.center(40))
            input()
        return self.fighter_1_rounds_won

    def resolve_fight(self):
        """Take the rounds won and determine the winner of the match."""
        print(f'--- THE MATCH IS OVER ---'.center(40))
        winner = 0
        if self.fighter_1_rounds_won > self.fighter_2_rounds_won:
            print(f'{self.fighter_1.name} wins the match!')
            self.fighter_1.wins += 1
            self.fighter_2.losses += 1
            winner = self.fighter_1
            if self.fighter_2.champion:
                self.fighter_1.champion = True
                self.fighter_2.champion = False
                print(f'{self.fighter_1.name} takes the championship from {self.fighter_2.name}!')
        else:
            print(f'{self.fighter_2.name} wins the match!')
            self.fighter_2.wins += 1
            self.fighter_1.losses += 1
            if self.fighter_1.champion:
                self.fighter_2.champion = True
                self.fighter_1.champion = False
                print(f'{self.fighter_1.name} looses the championship to {self.fighter_2.name}!')
        print(f'--- THE MATCH IS OVER ---\n'.center(40))
        return winner

    def boost_random_stat(self):
        """Boost a random stat for the opponent fighter"""
        skills = ['Punching', 'Kicking', 'Grappling', 'Speed']
        boost_skill = random.choice(skills)
        improvement = random.randint(1, 10)
        if boost_skill == 'Punching':
            self.fighter_2.punch += improvement
        elif boost_skill == 'Kicking':
            self.fighter_2.kick += improvement
        elif boost_skill == 'Grappling':
            self.fighter_2.grappling += improvement
        elif boost_skill == 'Speed':
            self.fighter_2.speed += improvement
        return boost_skill, improvement

    def deboost_random_stat(self, boosted_skill, improvement):
        """Deboost the random stat after the matchup"""
        if boosted_skill == 'Punching':
            self.fighter_2.punch -= improvement
        elif boosted_skill == 'Kicking':
            self.fighter_2.kick -= improvement
        elif boosted_skill == 'Grappling':
            self.fighter_2.grappling -= improvement
        elif boosted_skill == 'Speed':
            self.fighter_2.speed -= improvement

    def payout_winning_reward(self, rounds):
        """Pay the winning reward based on the salary of the opponent"""
        base = 200_000
        champ_factor = 1
        if self.fighter_2.champion:
            champ_factor = 5
            base = 400_000
        reward = self.fighter_2.salary * champ_factor + random.randint(1, 4) + base * 2 * (rounds + 1) \
                 + self.fighter_2.total_skill_score ** 2
        print(f'Well done, you won ${reward:,}!')
        return reward

    def payout_loosing_reward(self, rounds):
        """Pay out a small amount if the fight is lost"""
        reward = self.fighter_2.salary // 2 + 80_000 * rounds
        print(f'You lost.\nReceiving - ${reward:,}')
        return reward

    # @staticmethod
    # def choose_number_of_rounds():
    #     """Choose whether to fight 3 rounds or 5 rounds"""
    #     menu = ['3 rounds', '5 rounds']
    #     question = [
    #         inquirer.List('rounds',
    #                       message="How many rounds do you want to fight?",
    #                       choices=menu,
    #                       default="3 rounds",
    #                       ),
    #     ]
    #     answer = inquirer.prompt(question)
    #     choice = answer['rounds']
    #     if choice == '3 rounds':
    #         return 4
    #     elif choice == '5 rounds':
    #         return 6

# methods for the ai fights
    def weighted_ai_skills(self):
        """Logic of the fight, who will win which round and so on.
        Weight the different skills, "heavier" skills will be more important.
        Multiply the weigh by the actual skill and add them all up to come up with a final score
        """
        weigh_punch = round(random.random(), 2)
        weigh_kick = round(random.random(), 2)
        weigh_grappling = round(random.random(), 2)
        weigh_speed = round(random.random(), 2)
        summed_score_fighter_1 = self.fighter_1.punch * weigh_punch + weigh_kick * self.fighter_1.kick + \
                                 self.fighter_1.grappling * weigh_grappling + self.fighter_1.speed * weigh_speed + \
                                 self.fighter_1.luck * 2
        summed_score_fighter_2 = self.fighter_2.punch * weigh_punch + weigh_kick * self.fighter_2.kick + \
                                 self.fighter_2.grappling * weigh_grappling + self.fighter_2.speed * weigh_speed + \
                                 self.fighter_2.luck * 2
        return summed_score_fighter_1, summed_score_fighter_2

    def fight_ai_round(self, score_fighter_1, score_fighter_2):
        """Fight one round and subtract from the fighters energy"""
        energy_consumption = random.randint(50, 120)

        # compare the fighters scores to find a winner
        if score_fighter_1 > score_fighter_2:
            self.fighter_1_rounds_won += 1
        if score_fighter_2 > score_fighter_1:
            self.fighter_2_rounds_won += 1

        percentage_energy_fighter_1 = energy_consumption / self.fighter_1.endurance
        percentage_energy_fighter_2 = energy_consumption / self.fighter_2.endurance

        if percentage_energy_fighter_1 > 1:
            self.fighter_1.energy -= percentage_energy_fighter_1
        if percentage_energy_fighter_2 > 1:
            self.fighter_2.energy -= percentage_energy_fighter_2

    def carry_out_ai_fight(self, score_ai_fighter_1, score_ai_fighter_2):
        """The fight between two ai fighters. Same logic, different visual outputs."""
        score_ai_fighter_1 *= self.fighter_1.energy / 100
        score_ai_fighter_2 *= self.fighter_2.energy / 100
        num_rounds = 4
        if self.fighter_1.champion or self.fighter_2.champion:
            num_rounds += 2
        for i in range(1, num_rounds):
            winner = ""
            loser = ""
            # logic for knock out
            if abs(self.fighter_1.energy - self.fighter_2.energy) >= 3:
                if self.fighter_1.energy > self.fighter_2.energy:
                    winner = self.fighter_1.name
                    loser = self.fighter_2.name
                    self.fighter_1_rounds_won = 10
                elif self.fighter_1.energy < self.fighter_2.energy:
                    winner = self.fighter_2.name
                    loser = self.fighter_1.name
                    self.fighter_2_rounds_won = 10
                print(f'\n{winner} knocked out {loser}')
                break
            self.fight_ai_round(score_ai_fighter_1, score_ai_fighter_2)  # fight one round
            score_ai_fighter_1, score_ai_fighter_2 = self.calculate_stats_with_energy(score_ai_fighter_1,
                                                                                      score_ai_fighter_2)

    def resolve_ai_fight(self):
        """Declare the winner of the ai fights"""
        if self.fighter_1_rounds_won > self.fighter_2_rounds_won:
            print(f'{self.fighter_1.name} vs. {self.fighter_2.name} // {self.fighter_1.name} wins')
            self.fighter_1.wins += 1
            self.fighter_2.losses += 1
            if self.fighter_2.champion:
                self.fighter_1.champion = True
                self.fighter_2.champion = False
                print(f'{self.fighter_1.name} takes the championship from {self.fighter_2.name}!')
        else:
            print(f'{self.fighter_2.name} vs. {self.fighter_1.name} // {self.fighter_2.name} wins')
            self.fighter_2.wins += 1
            self.fighter_1.losses += 1
            if self.fighter_1.champion:
                self.fighter_2.champion = True
                self.fighter_1.champion = False
                print(f'{self.fighter_1.name} looses the championship to {self.fighter_2.name}!')
