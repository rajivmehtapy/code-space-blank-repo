import github
import duckdb
import requests
import json
from github import Github
from github import Auth
duckdb.default_connection.execute("SET GLOBAL pandas_analyze_sample=100000")

# !pip install PyGithub
# !pip install -U github-dependents-info

def get_star_count(repo_name,auth):
    # Gets the star count for a GitHub repo.

    # Args:
    #     repo_name: The name of the GitHub repo.

    # Returns:
    #     The star count for the repo.

    g = github.Github(auth=auth)
    repo = g.get_repo(repo_name)
    return repo.stargazers_count

def get_forks_count(repo_name,auth):
    """Get the forks count for a GitHub repo.

    Args:
        repo_name (str): The name of the GitHub repo.

    Returns:
        int: The number of forks for the repo.
    """

    github_user = github.Github(auth=auth)
    repo = github_user.get_repo(repo_name)
    print(f'--->{repo.get_license().name}')
    return repo.forks_count

def get_activity(repo_name,auth):
    """
    Get the activity for a GitHub repo.

    Args:
        repo_name (str): The name of the GitHub repo.

    Returns:
        dict: The activity for the repo.
    """

    g = github.Github(auth=auth)
    repo = g.get_repo(repo_name)
    activity = repo.get_stats_contributors()

    return activity

def get_watch_count(repo_name,auth):
  """Gets the watch count for a GitHub repo.

  Args:
    repo_name: The name of the GitHub repo.

  Returns:
    The watch count for the repo.
  """

  client = github.Github(auth=auth)
  repo = client.get_repo(repo_name)
  watch_count = repo.get_subscribers()
  return watch_count.totalCount

def get_release_count(repo_name,auth):
    """Gets the release count for a GitHub repo.

    Args:
        repo_name (str): The name of the GitHub repo.

    Returns:
        int: The number of releases for the repo.
    """

    g = github.Github(auth=auth)
    repo = g.get_repo(repo_name)
    releases = repo.get_releases()
    return releases.totalCount

def get_last_release_date(repo_name,auth,version_id):
    """Gets the last release date from a GitHub repo.

    Args:
        repo_name (str): The name of the GitHub repo.

    Returns:
        str: The last release date.
    """
    g = github.Github(auth=auth)
    repo = g.get_repo(repo_name)
    release = repo.get_release(id=version_id)
    return release.published_at

def get_contributor_count(repo_name,auth):
    """Gets the contributor count for a GitHub repo.

    Args:
        repo_name (str): The name of the GitHub repo.

    Returns:
        int: The number of contributors to the repo.
    """

    g = github.Github(auth=auth)
    repo = g.get_repo(repo_name)
    contributors = repo.get_contributors()
    return contributors.totalCount

def get_license(repo_name,git_access_token):

  url = "https://api.github.com/repos/PyGithub/PyGithub/license"
  payload = {}
  headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': 'Bearer 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',
    'X-GitHub-Api-Version': '2022-11-28'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  license=json.loads(response.text)
  return license['license']['key']

def get_total_repo(id):
    try:
        sql=f"""
        Select sum(no_of_stacks) as total_repo
        from final
        where tool_id={id}
        """
        return sql_helper(sql).to_dict()['total_repo'][0]
    except Exception as ex:
        return 0

def get_Repo_Count_For_A_Tools_Version_wise(tool_id):
    try:
        sql=f"""
        select 
            number,"detected in # of stacks" as no_of_stacks
        from versions_data_df
        where 
            tool_id = {tool_id}
        """ 
        return [{'version':item.number , 'no':item.no_of_stacks}for inx,item in sql_helper(sql).iterrows()]
    except Exception as ex:
        print(f'Data --> {ex}')

def sql_helper(sql):
    return duckdb.query(sql).to_df()

def sql_helper_one(sql):
    return duckdb.query(sql).fetchone()