import re
import logging
from typing import Optional, Dict

from fire import Fire
from github import Github, Repository
from yaml import load, FullLoader

logging.basicConfig(level='INFO')


def apply_labels(repos: str,
                 org: Optional[str] = None,
                 path: Optional[str] = 'sample/default.yaml',
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 access_token: Optional[str] = None) -> None:
    """
    Applies the labels from a file to all matching repositories.

    :param org: Name of the organisation on Github
    :param repos: Name or pattern of the repositories on which the new_labels will be applied
    :param path: Path of the new_labels yml file. See sample directory for examples.
    :param username: Github username. Not required if :param access_token is provided.
    :param password: Github password. Not required if :param access_token is provided.
    :param access_token: Github access token. Not required if :param username and :param password are provided
    :return: None
    """
    github = github_login(username, password, access_token)
    new_labels = read_label_file(path)
    count = 0

    for repository in get_matching_repositories(github, org, repos):
        update_labels(repository, new_labels)
        count += 1

    logging.info(f'Successfully applied labels from {path} on {count} repositories')


def get_matching_repositories(github: Github, org: Optional[str], repos: str) -> Repository:
    repos_pattern = re.compile(repos)

    if org is not None:
        for organisation in github.get_user().get_orgs():
            if org in [organisation.name, organisation.login]:
                for repository in organisation.get_repos():
                    yield repository
    else:
        for repository in github.get_user().get_repos():
            if repos_pattern.match(repository.name):
                yield repository


def update_labels(repository: Repository, new: Dict[str, Dict[str, str]]):
    logging.info(f'Working on {repository.name}')

    # Edit or delete existing labels
    for old in repository.get_labels():

        # Edit labels
        if fmt(old.name) in new:

            # Edit only if there is a difference
            if (old.name, old.color, old.description) != tuple(new[fmt(old.name)].values()):
                logging.info(f'Editing {old.name}')
                old.edit(*new[fmt(old.name)].values())
        else:
            logging.info(f'Deleting {old.name}')
            old.delete()

    # Create new labels
    existing_labels = {fmt(x.name) for x in repository.get_labels()}
    for new_label in new.values():
        if fmt(new_label['name']) not in existing_labels:
            logging.info(f'Creating {new_label["name"]}')
            repository.create_label(*[x for x in new_label.values() if x is not None])


def read_label_file(path: str) -> Dict[str, Dict[str, str]]:
    with open(path) as fp:
        labels = load(fp, Loader=FullLoader)
    return {fmt(x['name']): x for x in labels}


def fmt(x: str) -> str:
    return x.strip().lower()


def github_login(username: Optional[str] = None,
                 password: Optional[str] = None,
                 access_token: Optional[str] = None) -> Github:
    return Github(*[access_token] if access_token is not None else [username, password])


if __name__ == '__main__':
    Fire(apply_labels)
