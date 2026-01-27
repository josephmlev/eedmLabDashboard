import shutil
import subprocess
from datetime import datetime

date_str = datetime.now().strftime('%Y-%m-%d')
shutil.copy('data.json', f'backups/data_{date_str}.json')

subprocess.run(['git', 'add', f'data_{date_str}.json'])
subprocess.run(['git', 'commit', '-m', f'Archive {date_str}'])
subprocess.run(['git', 'pull', '--rebase'])
subprocess.run(['git', 'push'])
