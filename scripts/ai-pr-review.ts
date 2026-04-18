async function main() {
  const geminiApiKey = process.env.GEMINI_API_KEY;
  const githubToken = process.env.GITHUB_TOKEN;
  const githubRepository = process.env.GITHUB_REPOSITORY;
  const prNumber = process.env.PR_NUMBER;

  if (!geminiApiKey || !githubToken || !githubRepository || !prNumber) {
    console.warn("Skipping AI PR Review: Secrets are not available for PRs submitted from forks.");
    process.exit(0);
  }

  try {
    console.log(`Fetching diff for PR #${prNumber} in ${githubRepository}...`);
    const diffResponse = await fetch(`https://api.github.com/repos/${githubRepository}/pulls/${prNumber}`, {
      headers: {
        "Authorization": `Bearer ${githubToken}`,
        "Accept": "application/vnd.github.v3.diff",
        "X-GitHub-Api-Version": "2022-11-28"
      }
    });

    if (!diffResponse.ok) {
      throw new Error(`Failed to fetch PR diff: ${diffResponse.status} ${diffResponse.statusText}`);
    }

    const diffText = await diffResponse.text();
    
    if (!diffText || diffText.trim() === "") {
      console.log("No diff found or diff is empty. Exiting.");
      process.exit(0);
    }

    console.log("Diff fetched successfully. Sending to Gemini for review...");

    const prompt = `You are a senior cybersecurity engineer and core maintainer reviewing a pull request for an open-source AI Agent Skill Registry.
Your tone must be direct, highly professional, and exactly like a real senior developer leaving a code review comment on GitHub.
DO NOT use any emojis.
DO NOT use large theatrical headers like "GEMINI REVIEW OUTPUT".
DO NOT output any generic AI conversational filler.
Get straight to the point.

The PR contains executable scripts (.sh, .py, .js) that will run on users' local machines.
Look specifically for:
- Malicious payloads (reverse shells, obfuscated code, hidden eval/exec)
- Credential stealing (reading ~/.ssh, scraping .env)
- Suspicious network requests
- Destructive commands (rm -rf, etc.)

If you find ANY malicious intent or high-risk vulnerabilities:
Start your response EXACTLY with: "CRITICAL SECURITY ALERT:"
Then explain exactly what is wrong and why it must not be merged.

If the code is completely safe:
Start your response EXACTLY with: "Security check passed." 
Then provide a brief 1-2 sentence summary of the changes.

PR Diff:
${diffText}`;

    const geminiResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key=${geminiApiKey}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        contents: [{
          parts: [{ text: prompt }]
        }],
        generationConfig: {
          temperature: 0.1
        }
      })
    });

    if (!geminiResponse.ok) {
      const errorText = await geminiResponse.text();
      throw new Error(`Failed to get review from Gemini: ${geminiResponse.status} ${geminiResponse.statusText} - ${errorText}`);
    }

    const geminiData = await geminiResponse.json();
    const reviewText = geminiData.candidates?.[0]?.content?.parts?.[0]?.text;

    if (!reviewText) {
      throw new Error("Failed to extract review text from Gemini response.");
    }

    console.log("Review generated successfully. Posting comment to GitHub...");

    const commentResponse = await fetch(`https://api.github.com/repos/${githubRepository}/issues/${prNumber}/comments`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${githubToken}`,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        body: reviewText
      })
    });

    if (!commentResponse.ok) {
      const errorText = await commentResponse.text();
      throw new Error(`Failed to post comment to GitHub: ${commentResponse.status} ${commentResponse.statusText} - ${errorText}`);
    }

    console.log("Review posted successfully.");
  } catch (error) {
    console.error("An error occurred during the PR review process:", error);
    process.exit(1);
  }
}

main();