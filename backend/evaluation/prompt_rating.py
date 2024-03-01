import os
import json
import random


def monte_carlo_eval(prompt):
    response_types = ['highly relevant', 'somewhat relevant', 'irrelevant']
    scores = {'highly relevant': 3, 'somewhat relevant': 2, 'irrelevant': 1}
    trials = 100
    total_score = 0
    for _ in range(trials):
        response = random.choice(response_types)
        total_score += scores[response]
    return total_score / trials


def elo_ratings_func(prompts, elo_ratings, K=30, opponent_rating=1600):
    for prompt in prompts:
        outcome = random.choice(['win', 'loss', 'draw'])
        actual_score = {'win': 1, 'loss': 0, 'draw': 0.5}[outcome]
        R_base = 10 ** (elo_ratings[prompt] / 400)
        R_opponent = 10 ** (opponent_rating / 400)
        expected_score = R_base / (R_base + R_opponent)
        elo_ratings[prompt] += K * (actual_score - expected_score)
    return elo_ratings


script_dir = os.path.dirname(os.path.realpath(__file__))
json_file_path = os.path.join(script_dir, '..', 'prompt-dataset', 'prompt-data.json')
with open(json_file_path) as f:
    data = json.load(f)

for item in data:
    prompt = item['prompt']
    monte_carlo_score = monte_carlo_eval(prompt)
    print(f'Prompt: {prompt}\nMonte Carlo Score: {monte_carlo_score}\n')

elo_ratings = {item['prompt']: 1600 for item in data}
elo_ratings = elo_ratings_func([item['prompt'] for item in data], elo_ratings)

for prompt, elo_rating in elo_ratings.items():
    print(f'Prompt: {prompt}\nElo Rating: {elo_rating}\n')