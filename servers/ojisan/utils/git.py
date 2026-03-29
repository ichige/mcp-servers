import git
from pathlib import Path

class GitHelper:
    """
    Git コマンドヘルパー
    """
    @staticmethod
    def get_last_commit_time(repository: Path, path: Path) -> int | None:
        """
        ファイルの最終コミット日時を返す
        """
        repo = git.Repo(repository)
        commits = list(repo.iter_commits(paths=path, max_count=1))

        if not commits:
            return None

        return commits[0].committed_date