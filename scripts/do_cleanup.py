import subprocess, os

GIT = r'C:\Program Files\Git\cmd\git.exe'
REPO = r'C:\Users\Fariz\OneDrive\Desktop\experiments\opendirectory'

for f in ['scripts/final_push.py', 'scripts/cleanup.py', 'changed.txt', 'files.txt', 'find_git.py', 'run_git.bat']:
    fp = os.path.join(REPO, f)
    if os.path.exists(fp):
        os.remove(fp)

subprocess.run([GIT, '-C', REPO, 'add', '-A'], capture_output=True, text=True)
r = subprocess.run([GIT, '-C', REPO, 'commit', '-m', 'cleanup: remove temp helper scripts'], capture_output=True, text=True)
print(r.stdout.strip()[:300])
if r.returncode != 0:
    print(r.stderr.strip()[:300])

r = subprocess.run([GIT, '-C', REPO, 'push', 'origin', 'fix/video-tags-and-readme-cleanup', '--force'], capture_output=True, text=True)
print('Push:', r.stdout.strip()[:200] if r.stdout else 'OK')
if r.returncode != 0:
    print(r.stderr.strip()[:200])
else:
    print('Done!')
