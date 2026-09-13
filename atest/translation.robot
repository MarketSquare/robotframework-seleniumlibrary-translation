*** Settings ***
Library     SeleniumLibrary    language=FI
Library     SeleniumLibrary    language=FR    WITH NAME    French
Library     Process
Library     OperatingSystem
Library     json_lib.py

*** Test Cases ***
Translation Works With Translation
    Sulje Kaikki Selaimet

French Translation Works
    Fermer Tous Les Navigateurs

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

LibDoc Works With French Translation
    ${json_kw_speck} =    Join Path    ${OUTPUT DIR}    SL_fr.json
    ${result} =    Run Process
    ...    python
    ...    -m
    ...    robot.libdoc
    ...    --format\=json
    ...    SeleniumLibrary::language\=FR
    ...    ${json_kw_speck}
    Should Be Equal As Integers    ${result.rc}    0    ${result.stderr}
    Compare Translations    ${json_kw_speck}    fr
