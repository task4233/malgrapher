from convert import convert_dot_to_networkx
import pytest


def test_convert_to_networkx():
    dot_file_path = './out/ls.dot'
    G = convert_dot_to_networkx(dot_file_path)
    assert G is not None


def test_convert_to_networkx_with_empty_dotfile_path():
    with pytest.raises(FileNotFoundError):
        convert_dot_to_networkx('')


def test_convert_to_networkx_with_empty_saved_path():
    dot_file_path = './out/ls.dot'
    saved_file_path = './out/ls_cfg.png'
    G = convert_dot_to_networkx(dot_file_path, saved_file_path)
    assert G is not None
