import subprocess

GIT = r'C:\Program Files\Git\cmd\git.exe'
REPO = r'C:\Users\Fariz\OneDrive\Desktop\experiments\opendirectory'

def git(*args):
    r = subprocess.run([GIT, '-C', REPO] + list(args), capture_output=True, text=True)
    out = r.stdout.strip()
    err = r.stderr.strip()
    if r.returncode != 0:
        print(f'ERROR: {err}')
        return None
    return out

# Delete remaining temp files
import os
for f in ['scripts/cleanup.py']:
    fp = os.path.join(REPO, f)
    if os.path.exists(fp):
        os.remove(fp)

# Add deletions and commit
git('add', '-A')
r = subprocess.run([GIT, '-C', REPO, 'commit', '-m', 'cleanup: remove temporary helper scripts'], capture_output=True, text=True)
print(f'Commit: {r.stdout.strip()}')
if r.returncode != 0:
    print(f'Stderr: {r.stderr.strip()}')

# Force push
r = subprocess.run([GIT, '-C', REPO, 'push', 'origin', 'fix/video-tags-and-readme-cleanup', '--force'], capture_output=True, text=True)
print(f'Push: {r.stdout.strip()}')
if r.returncode != 0:
    print(f'Stderr: {r.stderr.strip()}')
else:
    print('Done! Clean force-push completed.')
