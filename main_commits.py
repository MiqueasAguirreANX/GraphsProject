"""
['id', 'node_id', 'name', 'full_name', 'private', 'owner', 'html_url', 'description', 'fork', 'url', 'forks_url',
'keys_url', 'collaborators_url', 'teams_url', 'hooks_url', 'issue_events_url', 'events_url', 'assignees_url',
'branches_url', 'tags_url', 'blobs_url', 'git_tags_url', 'git_refs_url', 'trees_url', 'statuses_url', 'languages_url',
'stargazers_url', 'contributors_url', 'subscribers_url', 'subscription_url', 'commits_url', 'git_commits_url',
'comments_url', 'issue_comment_url', 'contents_url', 'compare_url', 'merges_url', 'archive_url', 'downloads_url',
'issues_url', 'pulls_url', 'milestones_url', 'notifications_url', 'labels_url', 'releases_url', 'deployments_url',
 'created_at', 'updated_at', 'pushed_at', 'git_url', 'ssh_url', 'clone_url', 'svn_url', 'homepage', 'size',
 'stargazers_count', 'watchers_count', 'language', 'has_issues', 'has_projects', 'has_downloads', 'has_wiki',
 'has_pages', 'forks_count', 'mirror_url', 'archived', 'disabled', 'open_issues_count', 'license', 'forks',
 'open_issues', 'watchers', 'default_branch', 'permissions']
"""

import requests as r
import pandas as pd

token = '534466e905f901ad45b642db7ddd4f6080e925d1'

COMMITS_DEVS_PRO = {
    'omgnetwork': [],           # error:
    'maticnetwork': [],         # error:
    'cryptoeconomicslab': [],   # error:
    'perun-network': [],        # error:
    'raiden-network': [],       # error:
    'connext': [],              # error:
    'AztecProtocol': [],        # error:
    'matter-labs': [],          # error:
    'LoopringSecondary': [],    # error:
    'starkware-libs': [],       # error:
    'fuellabs': [],             # error:
    'ethereum-optimism': [],    # error:
    'OffchainLabs': [],         # error:
    'celer-network': [],        # error:
    'skalenetwork': [],         # error:
}


def main():
    cont1 = 0
    for k in COMMITS_DEVS_PRO.keys():
        url = f'https://api.github.com/orgs/{k}/repos'
        lista_proyectos = r.get(url, params={'access_token': token}).json()
        cont2 = 0
        print(k)
        print()
        for item in lista_proyectos:
            print(item['full_name'])
            try:
                url2 = f"https://api.github.com/repos/{item['full_name']}/commits"
                print(url2)
                commits = r.get(url2, params={'type': 'public', 'access_token': token})
                print(commits.status_code)
                print()
                for commit in commits.json():
                    print(commit)
                    print(f"{commit['commit']['author']['name']}:{commit['commit']['author']['date']}")
                    print()
                    COMMITS_DEVS_PRO[k].append({'project': item['name'], 'name': commit['commit']['author']['name'],
                                                'date': commit['commit']['author']['date']})

            except Exception as e:
                print(f'Ocurred an error at index ({cont1},{cont2})')
                print(f'{e}')
            finally:
                cont2 += 1

        cont1 += 1

    print('Trabajo terminado: commits de todos los proyectos de todos los repositorios')
    list_df = []
    for org in COMMITS_DEVS_PRO.keys():
        for item in COMMITS_DEVS_PRO[org]:
            list_df.append([org, item['project'], item['name'], item['date']])

    df = pd.DataFrame(list_df)
    df.to_csv(path_or_buf='commits.csv')


main()
