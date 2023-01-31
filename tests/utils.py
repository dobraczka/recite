from typing import Optional
import toml
import pathlib

def create_file(
    my_tmp_path: pathlib.Path, file_name: str, content: Optional[str] = None
):
    # create a file "myfile" in "mydir" in temp folder
    filepath = my_tmp_path / file_name
    with filepath.open("w", encoding="utf-8") as f:
        if content is not None:
            f.write(content)


def create_versioned_pyproject_toml(my_tmp_path: pathlib.Path, version: str):
    create_file(
        my_tmp_path,
        "pyproject.toml",
        toml.dumps(
            {
                "tool": {
                    "poetry": {
                        "version": version,
                        "name": "test",
                        "authors": ["test"],
                        "description": "desct",
                    }
                }
            }
        ),
    )
