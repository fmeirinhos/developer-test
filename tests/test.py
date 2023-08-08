import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from backend import solve

examples_dir = os.path.join(os.path.dirname(__file__), '../examples')

# Iterate through the example folders
for example_folder in sorted(os.listdir(examples_dir)):
    example_path = os.path.join(examples_dir, example_folder)
    
    # Ensure it's a folder and matches the expected naming pattern
    if os.path.isdir(example_path) and example_folder.startswith('example'):

        # Paths to the input and expected answer files
        mf_path = os.path.join(example_path, 'millennium-falcon.json')
        e_path = os.path.join(example_path, 'empire.json')
        answer_path = os.path.join(example_path, 'answer.json')

        # Read the expected answer
        with open(answer_path, 'r') as file:
            expected_answer = json.load(file)['odds']

        # Calculate the result using the solve function
        actual_result = solve(mf_path, e_path)

        # Check if the actual result matches the expected answer
        if abs(actual_result - expected_answer) < 1e-12:
            print(f"Test passed for {example_folder}")
        else:
            print(f"Test failed for {example_folder}: Expected {expected_answer}, got {actual_result}")
