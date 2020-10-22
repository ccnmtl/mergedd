import argparse

from tasks import MergeMatchingPullRequestTask


def main(args):
    repos = args.repos
    branch = args.branch

    repo_list = open(repos)

    print('Merge the most recent pull request for branch {}'.format(branch))
    for line in repo_list:
        repo = line.strip()
        MergeMatchingPullRequestTask(
            repo, args.owner, args.branch, args.api_token).run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge pull request')
    parser.add_argument(
        '--repos', help='path to repos.txt file', default='./repos.txt')

    parser.add_argument(
        '--branch', help='name of branch')

    parser.add_argument(
        '--owner', help='repo owner')

    parser.add_argument(
        '--api_token', help='Github oauth token')

    args = parser.parse_args()
    main(args)
