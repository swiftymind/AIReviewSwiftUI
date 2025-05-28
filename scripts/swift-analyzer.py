import os
import requests
import json
import time
import openai

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
REPO = os.environ['GITHUB_REPOSITORY']
PR_NUMBER = os.environ['PR_NUMBER']
COMMIT_ID = os.environ['GITHUB_SHA']
MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o')
MAX_TOKENS = 600

def get_pr_files():
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files'
    response = requests.get(url, headers=headers)
    return response.json()

def get_file_type(filename):
    if filename.endswith('.swift'):
        if 'View' in filename or 'SwiftUI' in filename:
            return 'swiftui'
        return 'swift'
    if filename.endswith('.m') or filename.endswith('.h'):
        return 'objc'
    if filename.endswith(('.storyboard', '.xib')):
        return 'ui'
    if filename.endswith(('.plist', '.xcconfig')):
        return 'config'
    if 'Podfile' in filename or 'Package.swift' in filename:
        return 'dependencies'
    return 'swift'

def generate_prompt(file_type, code):
    system_prompts = {
        'swift': "You are a senior iOS developer. Review this Swift code for memory management, architecture, performance, and security.",
        'swiftui': "You are a senior iOS developer and SwiftUI expert. Review this SwiftUI code for state management, view composition, accessibility, and performance.",
        'objc': "You are a senior iOS Objective-C expert. Check for ARC issues, category use, protocols, and legacy compatibility.",
        'ui': "You are an iOS UI/UX expert. Check for Auto Layout, accessibility, Dynamic Type, and dark mode.",
        'config': "You are an iOS build expert. Review for security, App Store compliance, and build settings.",
        'dependencies': "You are an iOS dependency expert. Check for security, version conflicts, performance impact, and license issues."
    }
    return f"{system_prompts.get(file_type, system_prompts['swift'])}\n\nCode:\n{code}\n\nProvide actionable feedback."

def post_inline_comment(path, line, body):
    url = f'https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/comments'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'body': body,
        'commit_id': COMMIT_ID,
        'path': path,
        'line': line,
        'side': 'RIGHT'
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 201:
        print(f"Failed to post comment on {path}:{line} - {response.text}")

def process_files(files):
    for file in files:
        filename = file.get('filename')
        patch = file.get('patch')
        if not patch or not filename:
            continue

        file_type = get_file_type(filename)
        lines = patch.split('\n')
        line_number = None

        for line in lines:
            if line.startswith('@@'):
                # Parse hunk header: @@ -old +new @@
                try:
                    new_info = line.split('+')[1].split(' ')[0]
                    line_number = int(new_info.split(',')[0]) - 1
                except:
                    line_number = None
            elif line.startswith('+') and not line.startswith('+++'):
                if line_number:
                    line_number += 1
                    code_line = line[1:].strip()
                    if code_line:
                        prompt = generate_prompt(file_type, code_line)
                        try:
                            response = client.chat.completions.create(
                                model=MODEL,
                                messages=[
                                    {"role": "system", "content": "You are an expert iOS developer and code reviewer."},
                                    {"role": "user", "content": prompt}
                                ],
                                max_tokens=MAX_TOKENS,
                                temperature=0.2
                            )
                            feedback = response.choices[0].message.content.strip()
                            post_inline_comment(filename, line_number, feedback)
                            print(f"Posted review for {filename}:{line_number}")
                            time.sleep(1)  # rate limit
                        except Exception as e:
                            print(f"AI review error for {filename}:{line_number} - {e}")

def main():
    files = get_pr_files()
    process_files(files)

if __name__ == '__main__':
    main()