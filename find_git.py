import subprocess, os

os.chdir(r'C:\Users\Fariz\OneDrive\Desktop\experiments\opendirectory')

git_paths = [
    r'C:\Program Files\Git\cmd\git.exe',
    r'C:\Program Files\Git\bin\git.exe',
    r'C:\Program Files\Git\mingw64\bin\git.exe',
]

git_exe = None
for p in git_paths:
    if os.path.isfile(p):
        git_exe = p
        break

if not git_exe:
    for root, dirs, files in os.walk(r'C:\Program Files\Git'):
        for f in files:
            if f == 'git.exe':
                git_exe = os.path.join(root, f)
                break
        if git_exe:
            break

print(f'Using git: {git_exe}')
print(f'Exists: {os.path.isfile(git_exe) if git_exe else False}')

if git_exe:
    r = subprocess.run([git_exe, '--version'], capture_output=True, text=True)
    print(f'rc: {r.returncode}')
    print(f'stdout: {r.stdout}')
    print(f'stderr: {r.stderr}')
