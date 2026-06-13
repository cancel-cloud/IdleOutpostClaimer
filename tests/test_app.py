import unittest
import sys
import types
from unittest.mock import patch

sys.modules.setdefault("requests", types.SimpleNamespace())

import app


class ClaimConfigurationTests(unittest.TestCase):
    def test_weekly_gems_endpoint_is_configured(self):
        self.assertIn("weekly_gems", app.ENDPOINTS)
        self.assertEqual(
            app.ENDPOINTS["weekly_gems"],
            "/api/v2/project/256000/free/item/com.rockbite.zombieoutpost.webshop.weeklygems",
        )

    def test_scheduled_claims_include_weekly_gems(self):
        claim_all_rewards = getattr(app, "claim_all_rewards", None)
        self.assertTrue(callable(claim_all_rewards))

        claimed = []

        with patch.object(app, "log"), patch.object(
            app, "claim", side_effect=lambda session, key: claimed.append(key)
        ):
            claim_all_rewards(object())

        self.assertEqual(
            claimed,
            ["shovels", "tickets", "legendary", "weekly", "weekly_gems"],
        )


if __name__ == "__main__":
    unittest.main()
