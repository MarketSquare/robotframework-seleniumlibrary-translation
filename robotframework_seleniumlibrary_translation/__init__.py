# Copyright 2024-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pathlib import Path
from typing import TypedDict

__version__ = "1.0.3"


class Language(TypedDict):
    language: str
    path: str


def get_language() -> list[Language]:
    folder = Path(__file__).parent

    return [{"language": "fi", "path": str(folder / "translation_fi.json")}]
