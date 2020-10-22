# Mergedd

A little utility to merge an outstanding pull request on a named branch across multiple repositories. The code uses the Github API to check on the status of a pull request and issue a merge command if all checks are green.

To use this utility, you'll need to generate a [personal access token](https://github.com/settings/tokens).

Then make the project:
   make

Construct your list of repositories:
   repos.txt
       repo_one
       repo_two
       repo_three

Run the merge:
    ve/bin/python ./runner.py --owner <repo owner> --match <pr branch> --api_token <github oauth token>

This is a sister utility to [Upgrayedd].
