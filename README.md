# Mergedd

A little utility to merge an outstanding pull request on a named branch across multiple repositories. The code uses the Github API to find the outstanding pull request on a branch, check on the status of a pull request and issue a merge command if all checks are green.

To use this utility, you'll need to generate a [personal access token](https://github.com/settings/tokens).

Then make the project:

```make```

Construct a file with a list of repositories. By default, the runner looks for `repos.txt`.
```
$ cat repos.txt
repo_one
repo_two
repo_three
```

Merge the prs:

```ve/bin/python ./runner.py --owner <repo owner> --branch <pr branch> --api_token <github oauth token>```

This is a sister utility to [Upgrayedd](https://github.com/ccnmtl/upgrayedd) authored by `@thraxil`.
