import os
import sys
sys.path.insert(0, '/home/mubarek/all_about_programing/10x_projects/Enterprise-Level-Automated-Prompt-Engineering/backend')

import json
from openai import OpenAI
from math import exp
import numpy as np
from utility.env_manager import get_env_manager
from evaluation._data_generation import get_completion
from evaluation._data_generation import file_reader
from rag.rag_system import get_context_from_rag


env_manager = get_env_manager()
client = OpenAI(api_key=env_manager['openai_keys']['OPENAI_API_KEY'])

def evaluate(prompt: str, user_message: str, context: str, use_test_data: bool = False) -> str:
    """Return the classification of the hallucination.
    @parameter prompt: the prompt to be completed.
    @parameter user_message: the user message to be classified.
    @parameter context: the context of the user message.
    @returns classification: the classification of the hallucination.
    """
    num_test_output = str(10)
    API_RESPONSE = get_completion(
        [
            {
                "role": "system", 
                "content": prompt.replace("{Context}", context).replace("{Question}", user_message)
            }
        ],
        model=env_manager['vectordb_keys']['VECTORDB_MODEL'],
        logprobs=True,
        top_logprobs=1,
    )

    system_msg = str(API_RESPONSE.choices[0].message.content)

    for i, logprob in enumerate(API_RESPONSE.choices[0].logprobs.content[0].top_logprobs, start=1):
        accuracy = np.round(np.exp(logprob.logprob)*100,2)
        output = f'\nhas_sufficient_context_for_answer: {system_msg}, \nlogprobs: {logprob.logprob}, \naccuracy: {np.round(np.exp(logprob.logprob)*100,2)}%\n'
        print(output)
        if system_msg == 'true' and np.round(np.exp(logprob.logprob)*100,2) >= 95.00:
            classification = 'true'
        elif system_msg == 'false' and np.round(np.exp(logprob.logprob)*100,2) >= 95.00:
            classification = 'false'
        else:
            classification = 'false'
    result = {'classification': classification, 'accuracy': f'{accuracy}%'}
    return result

if __name__ == "__main__":
    user_objective = str(input("objective: "))
    context_message = get_context_from_rag(user_objective)
    prompt_message = file_reader("prompts/generic-evaluation-prompt.txt")
    context = str(context_message)
    prompt = str(prompt_message)
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.dirname(script_dir)
    file_path = os.path.join(base_dir, "prompt-dataset/prompt-data.json")
    with open(file_path, 'r') as f:
        prompts = json.load(f)

    questions = [prompt['prompt'] for prompt in prompts]
    for question in questions:
        print(evaluate(prompt, question, context))