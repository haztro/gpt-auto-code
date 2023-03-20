import subprocess
import openai
import json
import backoff
from openai_config import API_KEY

# Get api key from file
openai.api_key = API_KEY

# Load prompt from human readable file
prompt = ''
with open("prompt.txt", "r") as file:
    prompt = file.read()
    prompt = prompt.replace('\n', '\\n').replace('\t', '\\t')

#TODO: Load task description from human readable file
task_description = {
    'problem_definition': 'Create a website that allows me to track and visualise the location of ferries on the Brisbane river in real-time.',
    'existing_work': 'https://gtfsrt.api.translink.com.au/api/realtime/SEQ/VehiclePositions has been identified as a suitable source', 
    'success_metrics': 'The note will read "satisfied"'
}


def get_output_string(stdout, stderr, note):
    return '{{"stdout": \'{}\', "stderr": \'{}\', "note": \'{}\'}}'.format(str(stdout), str(stderr), str(note))


def get_task_string(td):
    pd = td['problem_definition']
    ew = td['existing_work']
    sm = td['success_metrics']
    return '{{"problem_definition": \'{}\', "existing_work": "{}", "success_metrics": \'{}\'}}'.format(str(pd), str(ew), str(sm))


def print_history(history):
    string = ""
    for entry in history:
        string += entry['role']
        string += "\n"
        string += entry['content']
        string += "\n\n"
    return string


def save_history(history):
    with open("history.txt", "w") as file:
        file.write(print_history(history))

    with open("history.json", "w") as file:
        json_history = {"history": history}
        json.dump(json_history, file)


@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)
 

complete = False
use_existing_history = False
history = []

if use_existing_history:
    with open("history.json", "r") as file:
        data = file.read()
        history = json.loads(data)["history"]
else:
    history = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": get_task_string(task_description)}
    ]



# Start self iteration
while not complete:

    response = completions_with_backoff(model="gpt-4", messages=history)

    response_content = response['choices'][0]['message']['content']
    history.append({"role": "assistant", "content": response_content})

    save_history(history)

    json_response = json.loads(response_content)
    description = json_response['description']
    code = json_response['code']

    with open("code.py", "w") as file:
        file.write(code)

    if description == "COMPLETE":
        break

    print("----DESCRIPTION----")
    print(description)
    print()

    input("Proceed?")

    result = subprocess.run(['python3', 'code.py'], capture_output=True, text=True)

    print("----OUTPUT----")
    print(result.stdout)
    print("----ERRORS----")
    print(result.stderr)
    print()

    note = input("Notes?")

    error_output = get_output_string(result.stdout, result.stderr, note)
    history.append({"role": "user", "content": error_output})

    save_history(history)
