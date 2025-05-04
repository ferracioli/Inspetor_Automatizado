from git import Repo
import os

class GitHandler:
    def __init__(self, repo_path):
        self.repo = Repo(repo_path)
        
    def get_latest_python_files(self, limit=10):
        """Retorna os arquivos Python modificados recentemente."""
        python_files = []
        
        for commit in list(self.repo.iter_commits('HEAD', max_count=5)):
            for file in commit.stats.files.keys():
                if file.endswith('.py') and os.path.exists(os.path.join(self.repo.working_dir, file)):
                    if file not in python_files:
                        python_files.append(file)
            
            if len(python_files) >= limit:
                break
                
        return python_files
    
    def get_file_content(self, file_path):
        """Retorna o conteúdo de um arquivo."""
        full_path = os.path.join(self.repo.working_dir, file_path)
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                return f.read()
        return None
