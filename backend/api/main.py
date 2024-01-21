from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.insert(0, '/home/mubarek/all_about_programing/10x_projects/Enterprise-Level-Automated-Prompt-Engineering/backend')
from evaluation.prompt_generator import main as generate_prompt_data, file_reader
from evaluation._evaluation import evaluate
from rag.rag_system import get_context_from_rag
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Objective(BaseModel):
    objective: str

@app.post("/generate-and-evaluate-prompts")
async def generate_and_evaluate_prompts(objective: Objective):
    # Generate prompt data
    generate_prompt_data("5", objective.objective)

    # Read the generated prompts
    script_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.dirname(script_dir)
    file_path = os.path.join(base_dir, "prompt-dataset/prompt-data.json")
    with open(file_path, 'r') as f:
        prompts = json.load(f)

    # Evaluate each prompt
    results = []
    for prompt in prompts:
        context_message = get_context_from_rag(objective.objective)
        context = str(context_message)
        prompt_message = file_reader("prompts/generic-evaluation-prompt.txt")
        prompt_text = str(prompt_message)
        evaluation_result = evaluate(prompt_text, prompt['prompt'], context)
        results.append({
            "prompt": prompt['prompt'],
            "classification": evaluation_result['classification'],
            "accuracy": evaluation_result['accuracy'],
            "sufficient_context": context
        })

    return results


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"/home/mubarek/all_about_programing/10x_projects/Enterprise-Level-Automated-Prompt-Engineering/backend/pdfs/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    return {"info": f"file '{file.filename}' stored at location: '{file_location}'"}