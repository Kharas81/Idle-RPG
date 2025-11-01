import unittest
from rpg_project.src.services.config_loader import ConfigLoaderService
from rpg_project.src.models.config_models import ItemConfig, OpponentConfig

class TestConfigLoaderService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loader = ConfigLoaderService()
        cls.loader.load_configs("config")

    def test_get_item_config(self):
        item = self.loader.get_item_config("potion")
        self.assertIsInstance(item, ItemConfig)
        self.assertEqual(item.name, "Heiltrank")

    def test_get_opponent_config(self):
        opponent = self.loader.get_opponent_config("goblin")
        self.assertIsInstance(opponent, OpponentConfig)
        self.assertEqual(opponent.name, "Goblin")

if __name__ == "__main__":
    unittest.main()