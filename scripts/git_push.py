import subprocess, os, json

GIT = r'C:\Program Files\Git\cmd\git.exe'
GH = r'C:\Program Files\GitHub CLI\gh.exe'
REPO = r'C:\Users\Fariz\OneDrive\Desktop\experiments\opendirectory'

def git(*args):
    r = subprocess.run([GIT, '-C', REPO] + list(args), capture_output=True, text=True)
    if r.returncode != 0:
        print(f'GIT ERROR: {r.stderr.strip()}')
        return None
    return r.stdout.strip()

def gh(*args):
    r = subprocess.run([GH] + list(args), capture_output=True, text=True, cwd=REPO)
    if r.returncode != 0:
        print(f'GH ERROR: {r.stderr.strip()}')
        return None
    return r.stdout.strip()

# Check branch
branch = git('branch', '--show-current')
print(f'Branch: {branch}')

# Check status
status = git('status', '--short')
print(f'Changes:\n{status}')

# Add all changed files
git('add', '-A')
print('Staged all files')

# Commit
r = subprocess.run([GIT, '-C', REPO, 'commit', '-m', 'fix: remove orphaned summary tag from update-readme.ts, add Option D to app-store-review-arbitrage, fix has_install_section check'], capture_output=True, text=True)
print(f'Commit: {r.stdout.strip()}')
if r.returncode != 0:
    print(f'Commit stderr: {r.stderr.strip()}')

# Push
r = subprocess.run([GIT, '-C', REPO, 'push', 'origin', branch], capture_output=True, text=True)
print(f'Push: {r.stdout.strip()}')
if r.returncode != 0:
    print(f'Push stderr: {r.stderr.strip()}')
else:
    print(f'Push successful!')
