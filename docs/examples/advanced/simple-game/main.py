"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib import console, getCurrentTime, processData

from mlpy.stdlib.collections import collections as ml_collections

from mlpy.stdlib.random import random as ml_random

from mlpy.stdlib.math import math as ml_math

def createGameConfig():
    config = {}
    config['max_number'] = 100
    config['max_guesses'] = 10
    config['difficulty_levels'] = 3
    config['points_per_game'] = 100
    return config

def createPlayer(name):
    player = {}
    player['name'] = name
    player['total_score'] = 0
    player['games_played'] = 0
    player['games_won'] = 0
    player['total_guesses'] = 0
    player['best_score'] = 0
    player['current_streak'] = 0
    player['best_streak'] = 0
    return player

def createGameSession(player, config, difficulty):
    session = {}
    session['player'] = player
    session['config'] = config
    session['difficulty'] = difficulty
    session['target_number'] = generateTargetNumber(config['max_number'], difficulty)
    session['guesses_made'] = []
    session['guesses_remaining'] = (config['max_guesses'] - difficulty)
    session['game_over'] = False
    session['won'] = False
    session['score'] = 0
    session['hints_used'] = 0
    session['start_time'] = 0
    return session

def generateTargetNumber(max_number, difficulty):
    if (difficulty == 1):
        return ml_random.randomInt(1, 50)
    elif (difficulty == 2):
        return ml_random.randomInt(1, 75)
    else:
        return ml_random.randomInt(1, max_number)

def makeGuess(session, guess_number):
    max_for_difficulty = getDifficultyMaxNumber(session['difficulty'])
    if ((guess_number < 1) or (guess_number > max_for_difficulty)):
        return createGuessResult(False, (str('Invalid guess! Must be between 1 and ') + str(max_for_difficulty)), session)
    if ml_collections.contains(session['guesses_made'], guess_number):
        return createGuessResult(False, (str((str('You already guessed ') + str(guess_number))) + str('!')), session)
    session['guesses_made'] = ml_collections.append(session['guesses_made'], guess_number)
    session['guesses_remaining'] = (session['guesses_remaining'] - 1)
    if (guess_number == session['target_number']):
        session['won'] = True
        session['game_over'] = True
        session['score'] = calculateScore(session)
        message = (str((str('Congratulations! You guessed ') + str(session['target_number']))) + str(' correctly!'))
        return createGuessResult(True, message, session)
    if (session['guesses_remaining'] <= 0):
        session['game_over'] = True
        message = (str('Game over! The number was ') + str(session['target_number']))
        return createGuessResult(False, message, session)
    hint = generateHint(session, guess_number)
    return createGuessResult(False, hint, session)

def getDifficultyMaxNumber(difficulty):
    if (difficulty == 1):
        return 50
    elif (difficulty == 2):
        return 75
    else:
        return 100

def createGuessResult(correct, message, session):
    result = {}
    result['correct'] = correct
    result['message'] = message
    result['session'] = session
    result['guesses_remaining'] = session['guesses_remaining']
    result['game_over'] = session['game_over']
    return result

def generateHint(session, guess_number):
    target = session['target_number']
    difference = ml_math.abs((guess_number - target))
    base_hint = ''
    if (guess_number < target):
        base_hint = 'Too low! '
    else:
        base_hint = 'Too high! '
    if (difference <= 5):
        base_hint = (str(base_hint) + str('Very close!'))
    elif (difference <= 15):
        base_hint = (str(base_hint) + str('Getting warm!'))
    elif (difference <= 30):
        base_hint = (str(base_hint) + str('Getting warmer...'))
    else:
        base_hint = (str(base_hint) + str('Way off!'))
    base_hint = (str((str((str(base_hint) + str(' ('))) + str(session['guesses_remaining']))) + str(' guesses left)'))
    if (ml_collections.length(session['guesses_made']) >= 3):
        advanced_hint = generateAdvancedHint(session)
        base_hint = (str((str(base_hint) + str(' '))) + str(advanced_hint))
    return base_hint

def generateAdvancedHint(session):
    target = session['target_number']
    low_guess = findClosestLowGuess(session['guesses_made'], target)
    high_guess = findClosestHighGuess(session['guesses_made'], target)
    if ((low_guess != 1) and (high_guess != 1)):
        return (str((str((str('Hint: Between ') + str(low_guess))) + str(' and '))) + str(high_guess))
    elif (low_guess != 1):
        return (str('Hint: Higher than ') + str(low_guess))
    elif (high_guess != 1):
        return (str('Hint: Lower than ') + str(high_guess))
    if ((target % 2) == 0):
        return 'Hint: The number is even'
    else:
        return 'Hint: The number is odd'

def findClosestLowGuess(guesses, target):
    closest = 1
    guesses_length = ml_collections.length(guesses)
    i = 0
    while (i < guesses_length):
        guess = guesses[i]
        if ((guess < target) and (guess > closest)):
            closest = guess
        i = (i + 1)
    return closest

def findClosestHighGuess(guesses, target):
    closest = 999
    guesses_length = ml_collections.length(guesses)
    i = 0
    while (i < guesses_length):
        guess = guesses[i]
        if ((guess > target) and (guess < closest)):
            closest = guess
        i = (i + 1)
    return 1 if (closest == 999) else closest

def calculateScore(session):
    base_score = 1000
    guesses_made = ml_collections.length(session['guesses_made'])
    guess_bonus = ((session['config']['max_guesses'] - guesses_made) * 50)
    difficulty_multiplier = session['difficulty']
    hint_penalty = (session['hints_used'] * 25)
    score = (((base_score + guess_bonus) * difficulty_multiplier) - hint_penalty)
    return ml_math.max(0, score)

def updatePlayerStats(player, session):
    player['games_played'] = (player['games_played'] + 1)
    player['total_guesses'] = (player['total_guesses'] + ml_collections.length(session['guesses_made']))
    if session['won']:
        player['games_won'] = (player['games_won'] + 1)
        player['current_streak'] = (player['current_streak'] + 1)
        player['total_score'] = (player['total_score'] + session['score'])
        if (session['score'] > player['best_score']):
            player['best_score'] = session['score']
        if (player['current_streak'] > player['best_streak']):
            player['best_streak'] = player['current_streak']
    else:
        player['current_streak'] = 0
    return player

def createAIPlayer():
    ai = {}
    ai['name'] = 'AI Player'
    ai['strategy'] = 'binary_search'
    ai['min_range'] = 1
    ai['max_range'] = 100
    ai['last_guess'] = 1
    return ai

def getAIGuess(ai, session, last_result):
    if (ai['strategy'] == 'binary_search'):
        return binarySearchGuess(ai, session, last_result)
    else:
        return randomGuess(ai, session)

def binarySearchGuess(ai, session, last_result):
    if (last_result != None):
        if (ai['last_guess'] < session['target_number']):
            ai['min_range'] = (ai['last_guess'] + 1)
        else:
            ai['max_range'] = (ai['last_guess'] - 1)
    guess = ml_math.floor(((ai['min_range'] + ai['max_range']) / 2))
    ai['last_guess'] = guess
    return guess

def randomGuess(ai, session):
    max_num = getDifficultyMaxNumber(session['difficulty'])
    return ml_random.randomInt(1, max_num)

def displayGameStatus(session):
    print('=== Number Guessing Game ===')
    print((str('Player: ') + str(session['player']['name'])))
    print((str('Difficulty: ') + str(getDifficultyName(session['difficulty']))))
    print((str('Range: 1-') + str(getDifficultyMaxNumber(session['difficulty']))))
    print((str('Guesses remaining: ') + str(session['guesses_remaining'])))
    print((str('Previous guesses: ') + str(formatGuessList(session['guesses_made']))))
    print('')

def getDifficultyName(difficulty):
    if (difficulty == 1):
        return 'Easy'
    elif (difficulty == 2):
        return 'Medium'
    else:
        return 'Hard'

def formatGuessList(guesses):
    if (ml_collections.length(guesses) == 0):
        return 'None'
    result = ''
    guesses_length = ml_collections.length(guesses)
    i = 0
    while (i < guesses_length):
        if (i > 0):
            result = (str(result) + str(', '))
        result = (result + guesses[i])
        i = (i + 1)
    return result

def displayPlayerStats(player):
    print('=== Player Statistics ===')
    print((str('Name: ') + str(player['name'])))
    print((str('Games played: ') + str(player['games_played'])))
    print((str('Games won: ') + str(player['games_won'])))
    if (player['games_played'] > 0):
        win_rate = ml_math.floor(((player['games_won'] * 100) / player['games_played']))
        print((str((str('Win rate: ') + str(win_rate))) + str('%')))
    if (player['games_won'] > 0):
        avg_guesses = ml_math.floor((player['total_guesses'] / player['games_won']))
        print((str('Average guesses per win: ') + str(avg_guesses)))
    print((str('Total score: ') + str(player['total_score'])))
    print((str('Best score: ') + str(player['best_score'])))
    print((str('Current streak: ') + str(player['current_streak'])))
    print((str('Best streak: ') + str(player['best_streak'])))
    print('')

def runAITournament():
    print('Running AI Tournament...')
    config = createGameConfig()
    ai_player = createAIPlayer()
    total_games = 15
    difficulties = [1, 2, 3]
    tournament_results = []
    difficulty_index = 0
    while (difficulty_index < ml_collections.length(difficulties)):
        difficulty = difficulties[difficulty_index]
        games_per_difficulty = 5
        wins = 0
        total_score = 0
        game_num = 0
        while (game_num < games_per_difficulty):
            ai_player['min_range'] = 1
            ai_player['max_range'] = getDifficultyMaxNumber(difficulty)
            ai_player['last_guess'] = 1
            session = createGameSession(ai_player, config, difficulty)
            last_result = None
            while session['game_over']:
                guess = getAIGuess(ai_player, session, last_result)
                last_result = makeGuess(session, guess)
                session = last_result['session']
            if session['won']:
                wins = (wins + 1)
                total_score = (total_score + session['score'])
            game_num = (game_num + 1)
        result = {}
        result['difficulty'] = difficulty
        result['wins'] = wins
        result['games'] = games_per_difficulty
        result['total_score'] = total_score
        result['avg_score'] = (total_score / wins) if (wins > 0) else 0
        tournament_results = ml_collections.append(tournament_results, result)
        print((str((str((str((str((str((str((str('Difficulty ') + str(getDifficultyName(difficulty)))) + str(': '))) + str(wins))) + str('/'))) + str(games_per_difficulty))) + str(' wins, Avg Score: '))) + str(result['avg_score'])))
        difficulty_index = (difficulty_index + 1)
    return tournament_results

def runSinglePlayerGame(difficulty):
    config = createGameConfig()
    player = createPlayer('Demo Player')
    print((str((str('Starting single player game (Difficulty: ') + str(getDifficultyName(difficulty)))) + str(')')))
    session = createGameSession(player, config, difficulty)
    displayGameStatus(session)
    guessing_strategy = createGuessingStrategy(difficulty)
    while session['game_over']:
        guess = getNextStrategicGuess(guessing_strategy, session)
        print((str('Guessing: ') + str(guess)))
        result = makeGuess(session, guess)
        session = result['session']
        print(result['message'])
        if session['game_over']:
            updateGuessingStrategy(guessing_strategy, guess, result['message'])
        print('')
    player = updatePlayerStats(player, session)
    print('Game completed!')
    if session['won']:
        print((str('Final score: ') + str(session['score'])))
    displayPlayerStats(player)
    return session['won']

def createGuessingStrategy(difficulty):
    strategy = {}
    strategy['min_bound'] = 1
    strategy['max_bound'] = getDifficultyMaxNumber(difficulty)
    strategy['approach'] = 'binary'
    strategy['eliminated_numbers'] = []
    return strategy

def getNextStrategicGuess(strategy, session):
    if (strategy['approach'] == 'binary'):
        return ml_math.floor(((strategy['min_bound'] + strategy['max_bound']) / 2))
    else:
        return ml_random.randomInt(strategy['min_bound'], strategy['max_bound'])

def updateGuessingStrategy(strategy, last_guess, result_message):
    if (ml_collections.indexOf(result_message, 'Too low') != 1):
        strategy['min_bound'] = (last_guess + 1)
    elif (ml_collections.indexOf(result_message, 'Too high') != 1):
        strategy['max_bound'] = (last_guess - 1)

def runNumberGuessingGame():
    print('Number Guessing Strategy Game - Advanced ML Demo')
    print('================================================')
    ml_random.setSeed(123)
    print('Running demonstration games...')
    print('')
    difficulties = [1, 2, 3]
    wins = 0
    total_games = ml_collections.length(difficulties)
    i = 0
    while (i < total_games):
        difficulty = difficulties[i]
        won = runSinglePlayerGame(difficulty)
        if won:
            wins = (wins + 1)
        print('----------------------------------------')
        i = (i + 1)
    print('')
    print((str((str((str((str('Demo Results: ') + str(wins))) + str('/'))) + str(total_games))) + str(' games won')))
    print('')
    print('Running AI tournament for comparison...')
    tournament_results = runAITournament()
    return wins

def main():
    print('Advanced Number Guessing Game')
    print('============================')
    result = runNumberGuessingGame()
    print('')
    print('Game demonstration completed successfully!')
    print("This showcases ML's object-oriented patterns, state management,")
    print('functional programming, and complex game logic implementation.')
    return 0

# End of generated code