import unittest
from pathlib import Path


WORKFLOW = Path(".github/workflows/version-and-release.yml")


class ReleaseWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text()

    def test_generated_changelog_is_staged_before_rebase(self):
        self.assertIn("git add version.py CHANGELOG.md", self.workflow)
        self.assertIn("git diff --cached --quiet", self.workflow)

    def test_tag_creation_is_idempotent(self):
        self.assertIn('TAG="v${{ steps.new_version.outputs.new_version }}"', self.workflow)
        self.assertIn('git rev-parse "$TAG"', self.workflow)
        self.assertIn('git rev-list -n 1 "$TAG"', self.workflow)
        self.assertIn('git rev-parse HEAD', self.workflow)
        self.assertIn('Tag $TAG already exists on HEAD; skipping tag creation.', self.workflow)

    def test_release_creation_allows_existing_release_updates(self):
        self.assertIn("allowUpdates: true", self.workflow)


if __name__ == "__main__":
    unittest.main()
