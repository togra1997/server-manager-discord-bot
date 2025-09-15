from src.utils.run_command import CommandRunner
import pytest


def test_add_command():
    runner = CommandRunner()
    runner.add_command("echo_hello", "echo Hello")

    command_dict = runner.commands
    assert "echo_hello" in command_dict.keys()
    assert command_dict["echo_hello"] == "echo Hello"


def test_run_command_success():
    runner = CommandRunner()
    runner.add_command("echo_hello", "echo Hello")

    result = runner.run_command("echo_hello")
    assert result == "Hello"


def test_run_command_ValueError():
    runner = CommandRunner()
    runner.add_command("echo_hello", "echo Hello")

    with pytest.raises(ValueError) as e:
        runner.run_command("unknown_command")
    assert str(e.value) == "unknown command: unknown_command"
