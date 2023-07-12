import git
import os
import datetime
import uuid
import random


class FakeGit:
    def __init__(self):
        self.project_dir = os.path.realpath(os.path.dirname(__file__))
        self.min_commits = 5
        self.max_commits = 20
        self.repo = None
        self.remote_url = "https://github.com/hungltsme/dummy-project.git"
        self.repo_name = self.remote_url.split("/")[-1].split(".")[0]
        print("[Info]: Starting")

    def load_repo(self):
        try:
            print("[Info]: Loading git repository")
            self.repo = git.Repo(os.path.join(self.project_dir))
            print("[Info]: Repo loaded")
        except git.exc.NoSuchPathError as e:
            print("[Error]: Repo not found. Creating new one from remote-url")
            # os.mkdir(os.path.join(self.project_dir, self.repo_name))
            # self.repo = git.Repo.clone_from(self.remote_url, os.path.join(self.project_dir, self.repo_name))
            raise e

    def execute_commit(self, year: int, month: int, day: int):
        action_date = str(datetime.date(year, month, day).strftime('%Y-%m-%d %H:%M:%S'))
        os.environ["GIT_AUTHOR_DATE"] = action_date
        os.environ["GIT_COMMITTER_DATE"] = action_date
        self.repo.index.commit(message=f"{(uuid.uuid4())}")

    def single_commit(self, year: int, month: int, day: int):
        current_date = datetime.date(year, month, day)
        commits_amount = random.randint(self.min_commits, self.max_commits)
        print(f"Currently commit {current_date} with {commits_amount} commits")
        for x in range(commits_amount):
            self.execute_commit(current_date.year, current_date.month, current_date.day)

    def many_commits(self, start_date, stop_date, mix=False):
        while True:
            self.single_commit(start_date.year, start_date.month, start_date.day)
            random_days = random.randint(3, 9)
            if not mix:
                random_days = 1
            start_date = start_date + datetime.timedelta(days=random_days)
            if start_date >= stop_date:
                break

    def git_push(self):
        try:
            origin = self.repo.remote(name='origin')
            origin.push()
        except Exception as e:
            print(f'Error occurred while pushing the code !:\n{e}')
        else:
            print("Changes have been pushed !")


if __name__ == "__main__":
    fake_git = FakeGit()
    fake_git.load_repo()

    if input("1.Create single commit\n2.Range of commits\n>> ") == '1':
        provided_data = [int(x) for x in input("Date in format YYYY/MM/DD\n>> ").split("/")]
        fake_git.single_commit(provided_data[0], provided_data[1], provided_data[2])
        fake_git.git_push()
    else:
        _start_date = [int(x) for x in input("Start date in format YYYY/MM/DD\n>> ").split("/")]
        _stop_date = [int(x) for x in input("Stop date in format YYYY/MM/DD\n>> ").split("/")]

        _start_date = datetime.date(_start_date[0], _start_date[1], _start_date[2])
        _stop_date = datetime.date(_stop_date[0], _stop_date[1], _stop_date[2])

        fake_git.many_commits(_start_date, _stop_date)
        fake_git.git_push()
