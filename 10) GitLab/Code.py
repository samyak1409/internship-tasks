"""
Hi Samyak,

We will need data (commits, developers' details, etc.) for every repo in the following GitLab orgs:
https://gitlab.com/tezos
https://gitlab.com/bitcoin-cash-node
https://gitlab.com/NebulousLabs

I have attached the GitHub code I used to get the data from GitHub repositories.

Please keep in mind that an org has multiple repos, you will need to fetch the orgs for the repos before going to the
final step of getting commits data.

I have also attached sample dataset of how the final data should look like.

Regards,
Vasundhara
"""


# IMPORTS:

from requests import Session, RequestException
from time import perf_counter, sleep
from itertools import count
from json import dumps
from os.path import exists
from os import mkdir, startfile
from csv import writer


start_time = perf_counter()


# ATTRIBUTES:

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
GROUP_PATHS = ('tezos', 'bitcoin-cash-node', 'NebulousLabs')  # The ID or URL-encoded path of the group owned by the authenticated user
BASE_URL = 'https://gitlab.com/api/v4'
WITH_SHARED = False  # Include projects shared to this group. Default is true
INCLUDE_SUBGROUPS = True  # Include projects in subgroups of this group. Default is false
MAX_ITEMS_PER_PAGE = 100  # Number of items to list per page (default: 20, max: 100).
DEBUG = False  # default: False
DATA_DIR = 'Scraped Data'


# MAIN:

if not exists(DATA_DIR):
    mkdir(DATA_DIR)

# Session Init:
with Session() as session:

    session.headers = HEADERS
    session.stream = False  # stream off for all the requests of this session

    for group_num, group_path in enumerate(GROUP_PATHS, start=1):

        print('\n' + f'Group {group_num}) {group_path}')

        # Step 1) List a group’s projects: https://docs.gitlab.com/ee/api/groups.html#list-a-groups-projects

        # Pagination: https://docs.gitlab.com/ee/api/index.html#pagination
        project_count = None
        projects = []
        for page in count(start=1):

            # Getting Request's Response:
            while True:
                try:
                    response = session.get(url=f'{BASE_URL}/groups/{group_path}/projects?simple=true&with_shared={WITH_SHARED}&include_subgroups={INCLUDE_SUBGROUPS}&pagination=keyset&page={page}&per_page={MAX_ITEMS_PER_PAGE}')
                except RequestException as e:
                    print(f'{type(e).__name__}:', e.__doc__.split('\n')[0], 'TRYING AGAIN...')
                    sleep(1)  # take a breath
                else:
                    if response.status_code == 200:
                        break
                    else:  # bad response
                        print(f'{response.status_code}: {response.reason} TRYING AGAIN...')
                        sleep(1)  # take a breath

            projects.extend(response.json())  # save this page's data

            # https://docs.gitlab.com/ee/api/index.html#other-pagination-headers:
            # print(response.headers)  # debugging
            if project_count is None:
                project_count = response.headers['X-Total']
                print('\n' + 'Project Count:', project_count)
            if response.headers['X-Next-Page'] == '':
                break  # stop when no more pages left

        # print(dumps(projects, indent=4))  # debugging

        for project_num, project_path in enumerate(map(lambda project: project['path_with_namespace'], projects), start=1):

            print('\n' + f'Project {project_num}) {project_path}')

            project_path = project_path.replace('/', '%2F')  # https://docs.gitlab.com/ee/api/index.html#namespaced-path-encoding

            # Step 2) List repository commits: https://docs.gitlab.com/ee/api/commits.html#list-repository-commits

            # Pagination: https://docs.gitlab.com/ee/api/index.html#pagination
            print('Loading Commits', end='')
            commits = []
            for page in count(start=1):

                print('.', end='')

                # Getting Request's Response:
                while True:
                    try:
                        response = session.get(url=f'{BASE_URL}/projects/{project_path}/repository/commits?pagination=keyset&page={page}&per_page={MAX_ITEMS_PER_PAGE}')  # parameter "all=true" is not working; should return all the commits acc. to https://docs.gitlab.com/ee/api/commits.html; so using pagination
                    except RequestException as e:
                        print(f'{type(e).__name__}:', e.__doc__.split('\n')[0], 'TRYING AGAIN...')
                        sleep(1)  # take a breath
                    else:
                        if response.status_code == 200:
                            break
                        else:  # bad response
                            print(f'{response.status_code}: {response.reason} TRYING AGAIN...')
                            sleep(1)  # take a breath

                commits.extend(response.json())  # save this page's data

                # https://docs.gitlab.com/ee/api/index.html#other-pagination-headers:
                # print(response.headers)  # debugging
                if response.headers['X-Next-Page'] == '':
                    break  # stop when no more pages left

            print('\n' + 'Commit Count:', len(commits))

            if DEBUG:
                print(dumps(commits, indent=4))

            # Writing to CSV:
            csv_file = f'{DATA_DIR}\\{project_path}.csv'
            with open(file=csv_file, mode='w', encoding='utf-8', newline='') as f:  # https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
                w = writer(f)
                w.writerow(commits[0].keys())  # column names
                w.writerow([])  # line gap
                w.writerows(map(lambda commit: commit.values(), commits))  # commits' data
            print('Saved to:', csv_file)

            if DEBUG:
                startfile(csv_file)
                break  # project traversal

        if DEBUG:
            break  # group traversal

        print('\n' + '-' * 120)  # sep line


print('\n' + f'Successfully finished in {int(perf_counter()-start_time)}s.')
