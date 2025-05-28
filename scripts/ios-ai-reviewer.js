const axios = require('axios');
const { execSync } = require('child_process');
const parse = require('parse-diff');

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const REPO = process.env.GITHUB_REPOSITORY;
const PR_NUMBER = process.env.PR_NUMBER;
const MODEL = process.env.OPENAI_MODEL || 'gpt-4o';
const MAX_TOKENS = parseInt(process.env.MAX_TOKENS || '600');

// Files to ignore
const IGNORED_PATTERNS = ['.xcodeproj', '.xcworkspace', '.xcuserdata', '.xcscheme', '.plist', '.pbxproj'];

function shouldIgnoreFile(filename) {
  return IGNORED_PATTERNS.some(pattern => filename.includes(pattern));
}

async function getPRHeadSHA() {
  const [owner, repo] = REPO.split('/');
  const url = `https://api.github.com/repos/${owner}/${repo}/pulls/${PR_NUMBER}`;
  const response = await axios.get(url, {
    headers: {
      'Authorization': `token ${GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json'
    }
  });
  return response.data.head.sha;
}

async function main() {
  try {
    // Get diff from the base (more robust than origin/main for forked PRs)
    const diffOutput = execSync('git diff origin/HEAD HEAD', { encoding: 'utf8' });
    const files = parse(diffOutput);

    for (const file of files) {
      const filePath = file.to;
      if (!filePath || filePath === '/dev/null' || shouldIgnoreFile(filePath)) continue;

      for (const chunk of file.chunks) {
        for (const change of chunk.changes) {
          if (change.add && change.position) {  // Use `position` instead of `line`
            const prompt = generatePrompt(filePath, change.content);
            const aiFeedback = await getAIReview(prompt);
            await postInlineComment(filePath, change.position, aiFeedback);
            await new Promise(resolve => setTimeout(resolve, 1000)); // Rate limit safety
          }
        }
      }
    }
  } catch (error) {
    console.error('Error during AI review:', error);
  }
}

function generatePrompt(filePath, code) {
  const fileType = getFileType(filePath);
  const systemPrompts = {
    swift: `You are a senior iOS developer and Swift expert. Review this Swift code for:
- Memory management issues
- iOS best practices
- Performance
- Security
- Threading safety
- App lifecycle considerations`,

    swiftui: `You are a senior iOS developer and SwiftUI expert. Review this SwiftUI code for:
- View composition
- State management
- Accessibility
- Performance optimizations
- Animations
- Responsiveness across devices
- Concurrency and MainActor issues`,

    objc: `You are a senior iOS Objective-C expert. Check for:
- Memory management (ARC)
- Categories, protocols
- Legacy issues
- Interop concerns`,

    ui: `You are an iOS UI/UX expert. Check for:
- Auto Layout
- Accessibility
- Dynamic Type
- Dark mode
- Performance`,

    config: `You are an iOS build expert. Check for:
- Build settings
- Privacy permissions
- App Store compliance`,

    dependencies: `You are an iOS dependency expert. Review for:
- Security vulnerabilities
- Version conflicts
- Performance impact
- License issues`
  };

  return `${systemPrompts[fileType] || systemPrompts.swift}\n\nReview this code change:\n${code}\n\nProvide specific, actionable feedback.`;
}

function getFileType(filePath) {
  if (filePath.endsWith('.swift')) {
    if (filePath.toLowerCase().includes('view') || filePath.toLowerCase().includes('swiftui')) {
      return 'swiftui';
    }
    return 'swift';
  }
  if (filePath.endsWith('.m') || filePath.endsWith('.h')) return 'objc';
  if (filePath.endsWith('.storyboard') || filePath.endsWith('.xib')) return 'ui';
  if (filePath.endsWith('.plist') || filePath.endsWith('.xcconfig')) return 'config';
  if (filePath.includes('Podfile') || filePath.includes('Package.swift')) return 'dependencies';
  return 'swift';
}

async function getAIReview(prompt) {
  try {
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: MODEL,
        messages: [
          { role: 'system', content: 'You are an expert iOS developer and code reviewer.' },
          { role: 'user', content: prompt }
        ],
        max_tokens: MAX_TOKENS,
        temperature: 0.2
      },
      {
        headers: {
          'Authorization': `Bearer ${OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );
    return response.data.choices[0].message.content.trim();
  } catch (error) {
    console.error('Error fetching AI review:', error.response?.data || error.message);
    return 'Error fetching AI review.';
  }
}

async function postInlineComment(path, position, body) {
  try {
    const [owner, repo] = REPO.split('/');
    const url = `https://api.github.com/repos/${owner}/${repo}/pulls/${PR_NUMBER}/comments`;

    const commitSHA = await getPRHeadSHA();  // Dynamically get correct SHA

    await axios.post(
      url,
      {
        body,
        commit_id: commitSHA,  // Use correct commit SHA
        path,
        position
      },
      {
        headers: {
          'Authorization': `token ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json'
        }
      }
    );
    console.log(`Posted comment on ${path} at position ${position}`);
  } catch (error) {
    console.error(`Error posting comment:`, error.response?.data || error.message);
  }
}

main();