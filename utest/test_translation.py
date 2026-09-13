import hashlib
import json
import subprocess
import textwrap
from collections import Counter
from pathlib import Path

import pytest

import robotframework_seleniumlibrary_translation


@pytest.fixture(scope="module", params=["fi", "fr"])
def language(request):
    return request.param


@pytest.fixture(scope="module")
def file(language) -> Path:
    return (
        Path(__file__).parent.parent
        / "robotframework_seleniumlibrary_translation"
        / f"translation_{language}.json"
    )


@pytest.fixture(scope="module")
def data(file: Path) -> dict:
    with file.open(encoding="utf-8") as stream:
        return json.load(stream)


def test_translation(file: Path, language):
    lang = robotframework_seleniumlibrary_translation.get_language()
    assert [item["language"] for item in lang] == ["fi", "fr"]
    translation = next(item for item in lang if item["language"] == language)
    result_path = Path(translation["path"])
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
    data: robotframework_seleniumlibrary_translation.Language,
):
    for translation, value in data.items():
        assert " " not in translation, translation
        assert " " not in value["name"], value


def source_checksums(translation: dict) -> set[str]:
    # The CI Python versions expose different common docstring indentation.
    # SeleniumLibrary hashes raw docstrings as UTF-16, so accept both forms.
    first, separator, rest = translation["doc"].partition("\n")
    dedented = first + separator + textwrap.dedent(rest)
    return {
        translation["sha256"],
        hashlib.sha256(dedented.encode("utf-16")).hexdigest(),
    }


def test_source_checksums_handle_indentation():
    old_doc = "Summary.\n\n        Details.\n        "
    new_doc = "Summary.\n\nDetails.\n"
    old_hash = hashlib.sha256(old_doc.encode("utf-16")).hexdigest()
    new_hash = hashlib.sha256(new_doc.encode("utf-16")).hexdigest()
    hashes = source_checksums({"doc": old_doc, "sha256": old_hash})
    assert hashes == {old_hash, new_hash}
    changed_hash = hashlib.sha256(
        new_doc.replace("Details", "Changed").encode("utf-16")
    )
    assert changed_hash.hexdigest() not in hashes


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
    with translation_file.open(encoding="utf-8") as source_translation:
        source_data = json.load(source_translation)
    with file.open(encoding="utf-8") as translation_file:
        translation_data = json.load(translation_file)
    for kw in source_data:
        source_sha256 = source_data[kw]["sha256"]
        translation_sha256 = translation_data[kw]["sha256"]
        assert translation_sha256 in source_checksums(source_data[kw]), (
            f"{kw} sha256 was {source_sha256} expected {translation_sha256}"
        )
