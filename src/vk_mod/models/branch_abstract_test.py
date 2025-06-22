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


def test_serealize_and_deserealize_success_success():
    branch = BranchAbstract(config=test_config)
    config = branch.get_config()
    assert config["config"] == test_config

    loaded_branch = BranchAbstract.from_config(config)
    assert loaded_branch.config == test_config
