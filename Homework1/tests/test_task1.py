import subprocess
import os


def test_hello_world_output():

    # Get the absolute path to the directory
    test_dir = os.path.dirname(__file__)

    # Construct the path to the directory
    src_dir = os.path.abspath(os.path.join(test_dir, '..', 'src'))

    result = subprocess.run(
        ['python', 'task1.py'],
        capture_output=True,
        text=True,
        check=True,
        cwd=src_dir
    )

    assert result.stdout.strip() == "Hello World!"