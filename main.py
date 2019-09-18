# This is a game where you manage a UFC Fighter
from fighter import generate_fighter
from manager import Manager
from league import League
from game import MatchUp
import os
import inquirer


def display_help():
    """Give new players an introduction into the game"""
    question = [
        inquirer.List('help',
                      message='Do you want to read the help information? ',
                      choices=['Show me the help', 'Play the game'],
                      default='Play the game',
                      ),
    ]
    answer = inquirer.prompt(question)
    choice = answer['help']
    if choice == 'Show me the help':
        print('--- HELP INFORMATION ---'.center(40))
        print('This is a manager-style game, where you manage a fighter in the UFC.')
        print('Your goal is to win as many fights as possible and end the game as champion.')
        print()
        print(f"Your fighter has 5 stats: \n* Punching, \n* Kicking, \n* Grappling, \n* Speed \n* Endurance.")
        print(f"In a fight all stats count, but one random skill will be emphasised.")
        print()
        print(f"You have the option of boosting one particular stat before the fight for the duration of the fight.")
        print(f"In between fights you can heal your fighter from the injuries of the fight and train a stat.")
        print(f"One training between fights is free of cost, further training will cost you money.")
        print()
        print(f"Normal fights are 3 rounds long, Championship fights last 5 rounds.")
        print(f"If a fighters energy is too low, he will be knocked out and the fight is immediately over.")
        print()
        print(f"A fighting season lasts 10 fights, after which new fighters "
              f"replace the 7 worse fighters of the league.")
        print(f"You can send your fighter to a training camp after a season, training one stat intensively.")
        print(f"If your fighter did not make the top 3 after a season ends, you have to choose a new fighter.")
        print()
        print(f"Finally, watch your money - if you are broke, the game is over.")
        print('--- GOOD LUCK! ---'.center(40))
        input()


def main():
    """Main Program"""
    display_help()
    manager, ufc_league = initalize_the_league()
    num_season = 0
    end_num_season = ufc_league.get_num_end_season()
    while num_season != end_num_season:
        playing_season(manager, ufc_league)
        print()
        print(f'--- END OF SEASON {num_season + 1} ---'.center(40))
        ufc_league.print_champions()
        ufc_league.remove_fighters_from_league()
        print('\nNew talent is entering the league!')
        ufc_league.add_new_fighters()
        ufc_league.boost_league()
        manager.training_camp()
        manager.training_factor = 5
        input()
        if manager.fighter not in ufc_league.league_fighters:
            print(f'\nYour fighter {manager.fighter.name} did not make the cut.')
            print('Pick a new fighter')
            manager.fighter = manager.pick_fighter()
            ufc_league.fighters.remove(manager.fighter)
        num_season += 1


def playing_season(manager, ufc_league):
    """Logic of the season"""
    rounds = 0
    while rounds != 3:
        manager.check_money()
        manager.main_menu()
        if manager.active_flag:
            # pick an opponent to fight against
            opponent = manager.pick_opponent()
            clear()
            # create the game instance for both fighters
            game = MatchUp(manager.fighter, opponent)
            opp_boosted_skill, opp_improvement = game.boost_random_stat()
            boosted_skill, improvement = manager.boost_stat_during_fight()
            score_fighter_1, score_fighter_2 = game.weighted_skills()
            # carry out the fight
            rounds_won = game.carry_out_manager_fight(score_fighter_1, score_fighter_2)
            # store the winner for reward payout
            winner = game.resolve_fight()
            # remove the boost from the fighter skill
            manager.deboost_fighter_stats(boosted_skill, improvement)
            game.deboost_random_stat(opp_boosted_skill, opp_improvement)
            # pay winning reward to manager in case of win
            if winner:
                manager.money += game.payout_winning_reward(rounds_won)
                manager.wins += 1
            else:
                manager.money += game.payout_loosing_reward(rounds_won)
                manager.losses += 1
            # pay the wage of the fighter
            manager.pay_fighter()
            manager.active_flag = False
            input()
            ufc_league.automatic_fight_against_each_other(opponent)
            input()
            ufc_league.league_ladder()
            game.fighter_2.reset_energy()
            ufc_league.automatic_training_fighters()
            rounds += 1
        input()
        clear()


def initalize_the_league():
    """When the programm starts, the league and manager is created"""
    # generate some fighters
    fighters = []
    for i in range(10):
        fighters.append(generate_fighter())

    # instantiate the league
    ufc_league = League(fighters)

    # let the Manager choose a fighter
    manager = Manager(fighters, ufc_league)

    # remove the chosen fighter from the league
    while manager.fighter in ufc_league.fighters:
        ufc_league.fighters.remove(manager.fighter)
        ufc_league.get_league_fighters(manager.fighter)

    return manager, ufc_league


def show_end_screen(manager):
    """When the game is finished, show one final screen with stats"""
    # Message that the game is over
    print('--- END OF THE GAME ---'.center(40))
    # Stats of the manager
    print(f'You won {manager.fighter.wins} fights.')
    print(f'You lost {manager.fighter.losses} fights.')
    if manager.fighter.champion:
        print('You are currently managing the champion!')
        print('Well done!')
    else:
        print('You did not manage to end the season as champion.')
        print('Better luck next time.')
    print('--- END OF THE GAME ---'.center(40))


def clear():
    """Clear the screen"""
    os.system('clear')


if __name__ == '__main__':
    main()
