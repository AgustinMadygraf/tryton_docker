# Tryton\run.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.app import main
from src.models.update_repo import RepoUpdater

if __name__ == '__main__':
    repo_path = 'C:\AppServ\www\AnalizadorDeProyecto'
    updater = RepoUpdater(repo_path)
    updater.run()    
    main()
