import os
import json
import sys
sys.path.insert(0, '/home/mubarek/all_about_programing/10x_projects/Enterprise-Level-Automated-Prompt-Engineering/backend')
from openai import OpenAI
from math import exp
import numpy as np
from utility.env_manager import get_env_manager
from rag.rag_system import get_context_from_rag
env_manager = get_env_manager()
client = OpenAI(api_key=env_manager['openai_keys']['OPENAI_API_KEY'])


def get_completion(
    messages: list[dict[str, str]],
    model: str = env_manager['vectordb_keys']['VECTORDB_MODEL'],
    max_tokens=500,
    temperature=0,
    stop=None,
    seed=123,
    tools=None,
    logprobs=None,
    top_logprobs=None,
) -> str:
    """Return the completion of the prompt.
    @parameter messages: list of dictionaries with keys 'role' and 'content'.
    @parameter model: the model to use for completion. Defaults to 'davinci'.
    @parameter max_tokens: max tokens to use for each prompt completion.
    @parameter temperature: the higher the temperature, the crazier the text
    @parameter stop: token at which text generation is stopped
    @parameter seed: random seed for text generation
    @parameter tools: list of tools to use for post-processing the output.
    @parameter logprobs: whether to return log probabilities of the output tokens or not.
    @returns completion: the completion of the prompt.
    """

    params = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stop": stop,
        "seed": seed,
        "logprobs": logprobs,
        "top_logprobs": top_logprobs,
    }
    if tools:
        params["tools"] = tools

    completion = client.chat.completions.create(**params)
    return completion


def file_reader(path: str) -> str:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.dirname(script_dir)
    file_path = os.path.join(base_dir, path)
    with open(file_path, 'r') as f:
        system_message = f.read()
    return system_message
            

def generate_prompt_data(prompt: str, context: str, num_test_output: str) -> str:
    """Return the classification of the hallucination.
    @parameter prompt: the prompt to be completed.
    @parameter user_message: the user message to be classified.
    @parameter context: the context of the user message.
    @returns classification: the classification of the hallucination.
    """
    API_RESPONSE = get_completion(
        [
            {
                "role": "user", 
                "content": prompt.replace("{context}", context).replace("{num_test_output}", num_test_output)
            }
        ],
        model=env_manager['vectordb_keys']['VECTORDB_MODEL'],
        logprobs=True,
        top_logprobs=1,
    )

    system_msg = API_RESPONSE.choices[0].message.content
    return system_msg


def main(num_test_output: str, objective: str):
    context_message = context = get_context_from_rag(objective)
    prompt_message = file_reader("prompts/prompt-generation-prompt.txt")
    context = str(context_message)
    prompt = str(prompt_message)
    prompt_data = generate_prompt_data(prompt, context, num_test_output)
    
    def save_json(prompt_data) -> None:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Get the parent directory
        parent_dir = os.path.dirname(script_dir)

        # Specify the file path relative to the parent directory
        file_path = os.path.join(parent_dir, "prompt-dataset/prompt-data.json")

        # Check if the directory exists and create it if it does not
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        json_object = json.loads(prompt_data)
        with open(file_path, 'w') as json_file:
            json.dump(json_object, json_file, indent=4)
            
        print(f"JSON data has been saved to {file_path}")

    save_json(prompt_data)

    print("===========")
    print("Prompt Data")
    print("===========")
    print(prompt_data)


if __name__ == "__main__":

    user_objective = str(input("objective: "))
    main("1", user_objective)  # n number of test data to generate