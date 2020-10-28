import requests


class MergeMatchingPullRequestTask(object):

    def __init__(self, repo, owner, pattern, api_token):
        self.repo = repo
        self.owner = owner
        self.pattern = pattern
        self.headers = {'Authorization': 'token %s' % api_token}
        self.git_base = 'https://api.github.com/repos'

    def get_pull_request(self):
        url = '{}/{}/{}/pulls?state=open'.format(
            self.git_base, self.owner, self.repo)

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            for pr in response.json():
                if self.pattern == pr['head']['ref']:
                    return pr['number']

        return False

    def check_status(self, number):
        url = '{}/{}/{}/pulls/{}'.format(
            self.git_base, self.owner, self.repo, number)

        response = requests.get(url, headers=self.headers)
        if not response.status_code == 200:
            return False

        the_json = response.json()
        return the_json['mergeable'] and the_json['mergeable_state'] == 'clean'

    def delete_branch(self):
        url = '{}/{}/{}/git/refs/heads/{}'.format(
            self.git_base, self.owner, self.repo, self.pattern)

        response = requests.delete(url, headers=self.headers)
        return response.status_code == 200

    def merge_request(self, number):
        url = '{}/{}/{}/pulls/{}/merge'.format(
            self.git_base, self.owner, self.repo, number)

        response = requests.put(url, headers=self.headers)
        return response.status_code == 200

    def run(self):
        print('====== %s =======' % self.repo)

        # Get the most recent pull request based on a branch name
        number = self.get_pull_request()
        if not number:
            print('No pull request for branch {}'.format(self.pattern))
            return
        print('Found pull request #{}'.format(number))

        # Verify the pull request is mergeable
        if not self.check_status(number):
            print('Pull request is not mergeable')
            return
        print('Ready to merge')

        # Merge the pull request
        if not self.merge_request(number):
            print('An error occurred when trying to merge the pull request')
            return False
        print('Merged')

        # Delete the branch
        if not self.delete_branch():
            print('An error occured when trying to delete the branch')
            return False
        print('Pull request branch deleted')
