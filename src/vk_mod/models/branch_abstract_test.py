from .branch_abstract import BranchAbstract


test_config = {
        "test_config_1": True,
        "test_config_2": 10
    }


def test_initialize_success():
    branch = BranchAbstract(config=test_config)
    assert branch.config == test_config


def test_default_initialize_success():
    branch = BranchAbstract()
    assert branch.config == {}


def test_get_config_success():
    branch = BranchAbstract(test_config)
    config = branch.get_config()
    assert config == test_config
