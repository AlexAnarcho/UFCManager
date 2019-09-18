# Organizing the project

## Fighter attributes
### Skills
* punch
* kick
* grappling
* luck
* speed

### Attributes
* weight
* height
* reach

# TODOs
* Write a finishing screen when the game is over by end of season
* Create weight classes
* Fix bug after picking a new figther after the season ends the picked fighter needs to be removed from fighter 

# DONEs
* Manager can pick the fighter in the beginning
* Let the other fighters fight each other automatically
* One League has many fighters
* One Fighter has many skills
* Manager can pick matchups
* Manager can train the fighter
* One Matchup has 3 rounds
* Inbetween the rounds the manager can boost one skill
* Give the fighter a temporary boost during the fight for one round
* Manager has money he has to pay to the fighter
* Implement luck into the game
* Matchups give salaries depending on the matchup
* Implement a main menu option where the manager can view the fighters stats
* If the Manager cannot afford any fighter, the game is over
* Implement energy into the game
* Fix View Stats gives "TypeError: unsupported format string passed to list.__format__"
* Implement endurance into the game
* Implement energy level in stats view
* Implement main menu option to reset the fighters energy level
* Implement a correlation between height and weight
* Implement a correlation between speed and weight 
* Implement endurance training and show endurance stats in view stats
* Implement reach into the game for punching and kicking
* Enable the Manager to switch the fighter, selling the current fighter for a new one
* Improve Menu layout
* Implement a KO when the energy difference between the fighters is bigger than 3
* Train all AI fighters automatically after a fighting round
* Implement a winning reward based on the salary of the opponent
* Let the manager choose whether to fight 3 rounds or 5 rounds
* Allow the manager to train the fighter more than once between fighting rounds against a premium
* If the fighters energy level is not full, ask the manager if he really wants to fight before a round
* Fix bug where the salary is not increased properly after training
* Increase the payout money depending on the rounds fought
* Implement a factor for training repeats
* Create a main menu point to show the league (listing all fighters sorted by their record)
* Create Champions
* Implement a win and loss record for the manager
* If the manager does not have enough money to heal the damaged fighter before the fight, he has to fight injured
* Show total skill score in the overview
* Automatically fight 5 rounds if one fighter is a champion
* AI Fighter knockout, no newline in the end, but at the beginning
* Reduce the training factor after a season
* Implement a view menu to view the stats of other fighters
* At the end of 10 rounds keep the 3 best players, give the manager the option to switch fighters (except for best 3), 
    new players have stronger base stats
* At the end of the season the fighter will be sent to training camp where one stat can be boosted
* Mark the champion in the picking opponent menu
* Write an introduction to the game
* Fix bug where total skill score is not accurately shown in ranking ladder
* Make new fighters get stronger over the seasons
* Limit the choice when picking a new fighter to non champion fighters



# Energy Game
Fighters have endurance, better endurance means the fighter will get less exhausted over the fight
Fighters have energy, higher energy means a higher score for the fighter
A round has an energy consumption, that lowers the energy of the fighters

## Approaches
percentages of energy consumption and endurance
    high consumption and low endurance means a high number to reduce the energy level by
    high consumption and high endurance means a low number to reduce the energy level by
    low consumption and low endurance means a low number to reduce the energy level by
    low consumption and high endurance means a low number to reduce the energy level by
    