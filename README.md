# github-label-manager
Manage labels across multiple projects

## Purpose
1. Apply labels from a file to one or more repositories
2. Apply labels from a file to multiple repositories in an organization
3. Easily follow best-practices / style-guides for labelling

## Usage

### Clone and open this repository

```bash
git clone https://github.com/varunvora/github-label-manager.git
cd github-label-manager
```

### Install python dependencies
```bash
pip install -U -r requirements.txt
```

### Run the script
```bash
python3 apply_labels.py --repos=$MY_REPO --access_token=$GITHUB_TOKEN
``` 

## Options
- Apply labels from a custom file by passing its path using `--path`
- Apply labels using Github username and password by passing `--username` and `--password`
- Apply labels to multiple repositories by supplying a regex pattern for `--repos`
- Apply labels for an organisation's repositories using `--org=`
- Run `python3 apply_labels.py -- --help` for help

## Contribution
- Feel free to add more [samples](/sample).