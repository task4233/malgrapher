from generate_dot_by_radare2 import generate_dot_by_radare2
import pytest
import os

test_file_path = 'sample/hello'


def test_generate_dot_by_radare2():
    saved_path = ''

    try:
        saved_path = generate_dot_by_radare2(test_file_path, 'hello')
    except Exception as e:
        print(e)

    assert(type(saved_path) is str)
    assert(len(saved_path) != 0)

    assert(os.path.exists(saved_path))
    assert(os.path.getsize(saved_path) > 0)


def test_generate_dot_by_radare2_failed_with_empty_bin_file_path():
    with pytest.raises(ValueError):
        generate_dot_by_radare2('', 'hello')


def test_generate_dot_by_radare2_failed_with_empty_sample_name():
    with pytest.raises(ValueError):
        generate_dot_by_radare2(test_file_path, '')
