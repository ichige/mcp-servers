import git
import logging
from git import Remote
from pathlib import Path

logger = logging.getLogger(__name__)

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

    @staticmethod
    def update_repository(repository: Path) -> str | None:
        """
        指定してリポジトリを最新化します。
        あくまで参照元となる .resource 配下のリポジトリの最新化を想定したものです。
        """
        try:
            repo = git.Repo(repository)
            return repo.git.pull("origin", "main")
        except Exception as e:
            logging.error(f"Git repository update failed: {e}")
            return None
