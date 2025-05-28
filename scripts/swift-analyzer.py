import os
import requests
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def analyze_ios_pr():
    github_token = os.environ['GITHUB_TOKEN']
    pr_number = os.environ['PR_NUMBER']
    repo = os.environ['GITHUB_REPOSITORY']

    # Get PR details
    pr_data = get_pr_details(github_token, repo, pr_number)

    # Analyze iOS-specific aspects
    analysis = analyze_ios_changes(pr_data)

    # Post comprehensive analysis
    post_ios_analysis(github_token, repo, pr_number, analysis)

def get_pr_details(token, repo, pr_number):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    pr_url = f'https://api.github.com/repos/{repo}/pulls/{pr_number}'
    pr_response = requests.get(pr_url, headers=headers)

    files_url = f'https://api.github.com/repos/{repo}/pulls/{pr_number}/files'
    files_response = requests.get(files_url, headers=headers)

    return {
        'pr': pr_response.json(),
        'files': files_response.json()
    }

def analyze_ios_changes(pr_data):
    # Categorize iOS files
    swift_files = []
    ui_files = []
    config_files = []
    test_files = []

    for file in pr_data['files']:
        filename = file['filename']
        if filename.endswith('.swift'):
            if 'Test' in filename:
                test_files.append(file)
            else:
                swift_files.append(file)
        elif filename.endswith(('.storyboard', '.xib')):
            ui_files.append(file)
        elif filename.endswith(('.plist', '.xcconfig')) or 'Podfile' in filename:
            config_files.append(file)

    analysis_sections = []

    if swift_files:
        swift_analysis = analyze_swift_files(swift_files)
        analysis_sections.append(f"## 🏎️ Swift Code Analysis\n{swift_analysis}")

    if ui_files:
        ui_analysis = analyze_ui_files(ui_files)
        analysis_sections.append(f"## 🎨 UI/UX Analysis\n{ui_analysis}")

    if config_files:
        config_analysis = analyze_config_files(config_files)
        analysis_sections.append(f"## ⚙️ Configuration Analysis\n{config_analysis}")

    if test_files:
        test_analysis = analyze_test_files(test_files)
        analysis_sections.append(f"## 🧪 Test Analysis\n{test_analysis}")

    return "\n\n".join(analysis_sections)

def analyze_swift_files(files):
    files_info = [{'name': f['filename'], 'changes': f['changes'], 'additions': f['additions']} for f in files]

    prompt = f"""
    Analyze these Swift file changes in an iOS project:
    {json.dumps(files_info, indent=2)}

    Focus on:
    1. Architecture patterns (MVC, MVVM, VIPER)
    2. Memory management concerns
    3. Performance implications
    4. iOS-specific API usage
    5. Potential crash risks
    6. Code organization and maintainability

    Provide specific recommendations for iOS development.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert iOS developer and code reviewer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        temperature=0.2
    )

    return response.choices[0].message.content

def analyze_ui_files(files):
    files_info = [{'name': f['filename'], 'changes': f['changes']} for f in files]

    prompt = f"""
    Analyze these iOS UI file changes:
    {json.dumps(files_info, indent=2)}

    Review for:
    1. Accessibility compliance
    2. Auto Layout best practices
    3. Dynamic Type support
    4. Dark mode compatibility
    5. Device size adaptability
    6. Performance impact

    Provide iOS UI/UX specific recommendations.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert iOS UI/UX developer and code reviewer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.2
    )

    return response.choices[0].message.content

def analyze_config_files(files):
    files_info = [{'name': f['filename'], 'changes': f['changes']} for f in files]

    prompt = f"""
    Analyze these iOS configuration changes:
    {json.dumps(files_info, indent=2)}

    Check for:
    1. Security implications
    2. App Store compliance
    3. Performance settings
    4. Privacy configurations
    5. Build optimization

    Flag any potential issues for iOS app submission.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert iOS developer and code reviewer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.2
    )

    return response.choices[0].message.content

def analyze_test_files(files):
    files_info = [{'name': f['filename'], 'changes': f['changes']} for f in files]

    prompt = f"""
    Analyze these iOS test file changes:
    {json.dumps(files_info, indent=2)}

    Evaluate:
    1. Test coverage adequacy
    2. UI testing best practices
    3. Mock/stub usage
    4. Async testing patterns
    5. Performance test considerations

    Suggest improvements for iOS testing.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert iOS developer and test reviewer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.2
    )

    return response.choices[0].message.content

def post_ios_analysis(token, repo, pr_number, analysis):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    comment = f"""# 📱 iOS Development Analysis

{analysis}

---
### 🔍 Additional Checks Recommended:
- [ ] Run instruments for memory leaks
- [ ] Test on physical devices
- [ ] Verify App Store submission requirements
- [ ] Check accessibility with VoiceOver
- [ ] Test in airplane mode/poor connectivity

*Generated by iOS AI Analyzer*"""

    requests.post(
        f'https://api.github.com/repos/{repo}/issues/{pr_number}/comments',
        json={'body': comment},
        headers=headers
    )

if __name__ == '__main__':
    analyze_ios_pr()