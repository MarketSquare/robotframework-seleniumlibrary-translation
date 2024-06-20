*** Settings ***
Library     SeleniumLibrary    language=FI
Library     Process
Library     OperatingSystem
Library     json_lib.py

*** Test Cases ***
Translation Works With Translation
    Sulje Kaikki Selaimet

LibDoc Works With Translation
    [Setup]    Remove File    ${CURDIR}/SL.json
    ${json_kw_speck} =    Join Path    ${CURDIR}    SL.json
    ${cmd} =    Join Command Line
    ...    python
    ...    -m
    ...    robot.libdoc
    ...    --format=json
    ...    SeleniumLibrary::language=FI
    ...    ${json_kw_speck}
    Run Process    ${cmd}    shell=True
    Compare Translations    ${json_kw_speck}
