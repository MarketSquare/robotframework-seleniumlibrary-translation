import json
import subprocess
from collections import Counter
from pathlib import Path

import pytest

import robotframework_seleniumlibrary_translation_fi


@pytest.fixture(scope="module")
def file() -> Path:
    return (
        Path(__file__).parent.parent
        / "robotframework_seleniumlibrary_translation_fi"
        / "translation.json"
    )


@pytest.fixture(scope="module")
def data() -> robotframework_seleniumlibrary_translation_fi.Language:
    lang = robotframework_seleniumlibrary_translation_fi.get_language()
    result_path = Path(lang["path"])
    with result_path.open("r") as file:
        return json.load(file)


def test_translation(file: Path):
    lang = robotframework_seleniumlibrary_translation_fi.get_language()
    assert lang["language"] == "fi"
    result_path = Path(lang["path"])
    assert result_path == file
    assert result_path.is_file()


def test_json_file_format(data: dict):
    for translation in data.values():
        assert translation.get("name"), translation
        assert translation.get("doc"), translation


def test_keywords_are_unique(data: dict):
    kw_names = [translation.get("name") for translation in data.values()]
    duplicates = {}
    for key, value in dict(Counter(kw_names)).items():
        if value != 1:
            duplicates[key] = value
    assert len(kw_names) == len(set(kw_names)), duplicates


def test_keyword_names_are_unique(data: dict):
    failed_kw_names = []
    for index, translation in enumerate(data):  # noqa: B007
        if translation in ["__init__", "__intro__"]:
            continue
        if translation == data[translation]["name"]:
            failed_kw_names.append(f"{translation} == {data[translation]['name']}")
    assert not failed_kw_names, (
        f"{len(failed_kw_names)} out of {index + 1} keyword "
        f"names where same: {', '.join(failed_kw_names)}"
    )


def test_keyword_names_no_space(
    data: robotframework_seleniumlibrary_translation_fi.Language,
):
    for translation, value in data.items():
        assert " " not in translation, translation
        assert " " not in value["name"], value


def test_verify_checksum(file: Path, tmp_path: Path):
    translation_file = tmp_path / "translation.json"
    subprocess.run(
        [
            "selib",
            "translation",
            str(translation_file),
        ],
        check=True,
    )
    with translation_file.open("r") as source_translation:
        source_data = json.load(source_translation)
    with file.open("r") as translation_file:
        translation_data = json.load(translation_file)
    for kw in source_data:
        source_sha256 = source_data[kw]["sha256"]
        translation_sha256 = translation_data[kw]["sha256"]
        assert (
            source_sha256 == translation_sha256
        ), f"{kw} sha256 was {source_sha256} expected {translation_sha256}"
