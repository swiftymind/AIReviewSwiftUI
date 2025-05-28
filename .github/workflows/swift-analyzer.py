{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import requests\
import json\
import subprocess\
from anthropic import Anthropic\
\
def analyze_ios_pr():\
    github_token = os.environ['GITHUB_TOKEN']\
    pr_number = os.environ['PR_NUMBER']\
    repo = os.environ['GITHUB_REPOSITORY']\
    \
    # Get PR details\
    pr_data = get_pr_details(github_token, repo, pr_number)\
    \
    # Analyze iOS-specific aspects\
    analysis = analyze_ios_changes(pr_data)\
    \
    # Post comprehensive analysis\
    post_ios_analysis(github_token, repo, pr_number, analysis)\
\
def get_pr_details(token, repo, pr_number):\
    headers = \{\
        'Authorization': f'token \{token\}',\
        'Accept': 'application/vnd.github.v3+json'\
    \}\
    \
    pr_url = f'https://api.github.com/repos/\{repo\}/pulls/\{pr_number\}'\
    pr_response = requests.get(pr_url, headers=headers)\
    \
    files_url = f'https://api.github.com/repos/\{repo\}/pulls/\{pr_number\}/files'\
    files_response = requests.get(files_url, headers=headers)\
    \
    return \{\
        'pr': pr_response.json(),\
        'files': files_response.json()\
    \}\
\
def analyze_ios_changes(pr_data):\
    client = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])\
    \
    # Categorize iOS files\
    swift_files = []\
    ui_files = []\
    config_files = []\
    test_files = []\
    \
    for file in pr_data['files']:\
        filename = file['filename']\
        if filename.endswith('.swift'):\
            if 'Test' in filename:\
                test_files.append(file)\
            else:\
                swift_files.append(file)\
        elif filename.endswith(('.storyboard', '.xib')):\
            ui_files.append(file)\
        elif filename.endswith(('.plist', '.xcconfig')) or 'Podfile' in filename:\
            config_files.append(file)\
    \
    analysis_sections = []\
    \
    if swift_files:\
        swift_analysis = analyze_swift_files(client, swift_files)\
        analysis_sections.append(f"## \uc0\u55356 \u57294 \u65039  Swift Code Analysis\\n\{swift_analysis\}")\
    \
    if ui_files:\
        ui_analysis = analyze_ui_files(client, ui_files)\
        analysis_sections.append(f"## \uc0\u55356 \u57256  UI/UX Analysis\\n\{ui_analysis\}")\
    \
    if config_files:\
        config_analysis = analyze_config_files(client, config_files)\
        analysis_sections.append(f"## \uc0\u9881 \u65039  Configuration Analysis\\n\{config_analysis\}")\
    \
    if test_files:\
        test_analysis = analyze_test_files(client, test_files)\
        analysis_sections.append(f"## \uc0\u55358 \u56810  Test Analysis\\n\{test_analysis\}")\
    \
    return "\\n\\n".join(analysis_sections)\
\
def analyze_swift_files(client, files):\
    files_info = [\{'name': f['filename'], 'changes': f['changes'], 'additions': f['additions']\} for f in files]\
    \
    prompt = f"""\
    Analyze these Swift file changes in an iOS project:\
    \{json.dumps(files_info, indent=2)\}\
    \
    Focus on:\
    1. Architecture patterns (MVC, MVVM, VIPER)\
    2. Memory management concerns\
    3. Performance implications\
    4. iOS-specific API usage\
    5. Potential crash risks\
    6. Code organization and maintainability\
    \
    Provide specific recommendations for iOS development.\
    """\
    \
    response = client.messages.create(\
        model="claude-3-sonnet-20240229",\
        max_tokens=500,\
        messages=[\{"role": "user", "content": prompt\}]\
    )\
    \
    return response.content[0].text\
\
def analyze_ui_files(client, files):\
    files_info = [\{'name': f['filename'], 'changes': f['changes']\} for f in files]\
    \
    prompt = f"""\
    Analyze these iOS UI file changes:\
    \{json.dumps(files_info, indent=2)\}\
    \
    Review for:\
    1. Accessibility compliance\
    2. Auto Layout best practices\
    3. Dynamic Type support\
    4. Dark mode compatibility\
    5. Device size adaptability\
    6. Performance impact\
    \
    Provide iOS UI/UX specific recommendations.\
    """\
    \
    response = client.messages.create(\
        model="claude-3-sonnet-20240229",\
        max_tokens=400,\
        messages=[\{"role": "user", "content": prompt\}]\
    )\
    \
    return response.content[0].text\
\
def analyze_config_files(client, files):\
    files_info = [\{'name': f['filename'], 'changes': f['changes']\} for f in files]\
    \
    prompt = f"""\
    Analyze these iOS configuration changes:\
    \{json.dumps(files_info, indent=2)\}\
    \
    Check for:\
    1. Security implications\
    2. App Store compliance\
    3. Performance settings\
    4. Privacy configurations\
    5. Build optimization\
    \
    Flag any potential issues for iOS app submission.\
    """\
    \
    response = client.messages.create(\
        model="claude-3-sonnet-20240229",\
        max_tokens=300,\
        messages=[\{"role": "user", "content": prompt\}]\
    )\
    \
    return response.content[0].text\
\
def analyze_test_files(client, files):\
    files_info = [\{'name': f['filename'], 'changes': f['changes']\} for f in files]\
    \
    prompt = f"""\
    Analyze these iOS test file changes:\
    \{json.dumps(files_info, indent=2)\}\
    \
    Evaluate:\
    1. Test coverage adequacy\
    2. UI testing best practices\
    3. Mock/stub usage\
    4. Async testing patterns\
    5. Performance test considerations\
    \
    Suggest improvements for iOS testing.\
    """\
    \
    response = client.messages.create(\
        model="claude-3-sonnet-20240229",\
        max_tokens=300,\
        messages=[\{"role": "user", "content": prompt\}]\
    )\
    \
    return response.content[0].text\
\
def post_ios_analysis(token, repo, pr_number, analysis):\
    headers = \{\
        'Authorization': f'token \{token\}',\
        'Accept': 'application/vnd.github.v3+json'\
    \}\
    \
    comment = f"""# \uc0\u55357 \u56561  iOS Development Analysis\
\
\{analysis\}\
\
---\
### \uc0\u55357 \u56589  Additional Checks Recommended:\
- [ ] Run instruments for memory leaks\
- [ ] Test on physical devices\
- [ ] Verify App Store submission requirements\
- [ ] Check accessibility with VoiceOver\
- [ ] Test in airplane mode/poor connectivity\
\
*Generated by iOS AI Analyzer*"""\
    \
    requests.post(\
        f'https://api.github.com/repos/\{repo\}/issues/\{pr_number\}/comments',\
        json=\{'body': comment\},\
        headers=headers\
    )\
\
if __name__ == '__main__':\
    analyze_ios_pr()}