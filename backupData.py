import shutil
import subprocess
from datetime import datetime

date_str = datetime.now().strftime('%Y-%m-%d')
filename = f'backups/data_{date_str}.json'
shutil.copy('data.json', filename)

subprocess.run(['git', 'add', filename])
subprocess.run(['git', 'commit', '-m', f'Archive {date_str}'])
subprocess.run(['git', 'pull', '--rebase'])
subprocess.run(['git', 'push'])
