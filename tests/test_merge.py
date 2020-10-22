import unittest

from tasks import MergeMatchingPullRequestTask
import requests_mock


class TestMerge(unittest.TestCase):

    @requests_mock.mock()
    def test_get_pull_request(self, m):
        m.register_uri(
            'GET',
            'https://api.github.com/repos/ccnmtl/dummy/pulls?state=open',
            json=[{'head': {'ref': 'the_branch'}, 'number': 444}])

        task = MergeMatchingPullRequestTask(
            'dummy', 'ccnmtl', 'the_branch', '12345')
        self.assertEqual(task.get_pull_request(), 444)

    @requests_mock.mock()
    def test_check_status_not_mergeable(self, m):
        m.register_uri(
            'GET',
            'https://api.github.com/repos/ccnmtl/dummy/pulls/444',
            json={'mergeable': False, 'mergeable_state': 'unstable'})

        task = MergeMatchingPullRequestTask(
            'dummy', 'ccnmtl', 'the_branch', '12345')
        self.assertFalse(task.check_status(444))

    @requests_mock.mock()
    def test_check_status_unstable(self, m):
        m.register_uri(
            'GET',
            'https://api.github.com/repos/ccnmtl/dummy/pulls/444',
            json={'mergeable': True, 'mergeable_state': 'unstable'})

        task = MergeMatchingPullRequestTask(
            'dummy', 'ccnmtl', 'the_branch', '12345')
        self.assertFalse(task.check_status(444))

    @requests_mock.mock()
    def test_check_status_mergeable(self, m):
        m.register_uri(
            'GET',
            'https://api.github.com/repos/ccnmtl/dummy/pulls/444',
            json={'mergeable': True, 'mergeable_state': 'clean'})

        task = MergeMatchingPullRequestTask(
            'dummy', 'ccnmtl', 'the_branch', '12345')
        self.assertTrue(task.check_status(444))
