## v1.1.6 (2025-01-14)

### Fix

- **deps**: bump Python version (#292)

## v1.1.5 (2025-01-09)

### Fix

- **main-app**: update vulnerabilities (#285)

## v1.1.4 (2023-11-10)

### Fix

- **parse-utils**: checking custom rules against file package names instead (#225)

## v1.1.3 (2023-08-25)

### Fix

- **file-utils**: fix could not find prefix for file, adding find pref… (#191)
- **file-utils**: update to return the longest path in get file path f… (#190)

## v1.1.2 (2023-08-24)

### Fix

- **readme**: fix broken links (#186)
- **readme**: using new logo that renders, before had been using javascript which does not render on GitHub (#185)
- **import-rules**: disabling test violation code checks within the tests directory (#181)

## v1.1.1 (2023-08-20)

### Fix

- **flake8-plugin**: switch to using strings for boolean values, for some reason using boolean options are not working as expected (#175)

### Refactor

- **defaults**: update docstrings and tests for the defaults module (#174)

## v1.1.0 (2023-08-20)

### Feat

- **rule-checker**: updated docstrings (#170)

## v1.0.0 (2023-08-19)

### Feat

- **pyproject**: update development status (#167)
- **pyproject**: update development status (#165)

## v0.11.0 (2023-08-19)

### Feat

- **flake8-plugin**: add check for rule conflicts (#160)

## v0.10.1 (2023-08-19)

### Fix

- **import-rules**: update restricted packages to correctly identify the packages and modules and subpackages that need to be restricted (#137)
- **import-rules**: update checks for import restrictions to correctly identify restricted imports (#136)
- **import-rules**: corrected finding packages that match import restrictions (#135)
- **checker**: use import restrictions from plugin and update test files (#134)
- **import-rules**: update functions (#128)
- **import-rules**: update isolated modules to account for imports from package itself (#126)

### Refactor

- **readme-and-import-rules**: update flag descriptions, add documentation, and refactor code to be more pythonic and efficient (#152)
- **custom-restrictions**: renamed import restrictions, custom re… (#151)
- **dynamic-imports**: added additional dynamic import checks, updated documentation to be more thorough, and added test cases to a function that did not have any (#150)
- **local-imports**: Use local scope imports for clarity instead (#148)
- **isolated-packages-flag**: renamed isolated modules flag to standalone modules to better reflect and describe what the flag does (#146)
- **restricted-import-visitor**: remove check module exists option from the restricted import visitor class, not used and unnecessary (#139)
- **restricted-import-visitor**: remove package imports in this class, calculated elsewhere (#138)
- **plugin**: update plugin to use preprocessed checker settings for restricted packages and import restrictions (#133)
- **restricted-import-visitor**: update restricted import visitor class to include whether restriction is from a restricted package or restricted import (#132)
- **error-codes**: update import restriction error codes (#131)
- **restricted-import-visitor**: move utility functions to restricted import utils module (#130)

## v0.10.0 (2023-08-07)

### Feat

- **option-utils**: add check conflict function and add tests (#124)

### Fix

- **file-utils**: add try except section to find prefix function (#123)

### Refactor

- **import-rules**: update typing to use specific parsed node classes (#120)
- **checker**: remove unused functions (#116)
- **docs**: update documentation directory (#114)

## v0.9.2 (2023-08-04)

### Refactor

- **docs**: update documentation directory
- **readme**: update readme section titles (#113)

## v0.9.1 (2023-08-04)

### Refactor

- **file-utils**: remove unused functions (#112)

## v0.9.0 (2023-08-03)

### Fix

- **pyproject**: fix flake8 extension (#108)
- **node-visitor**: stdlib_list should be imported locally where it is used (#106)
- **restricted-visitor**: refactor get strings functions (#84)
- **visitor**: get_module_name_from_filename uses filename not file_path (#83)
- **default**: fix default settings (#77)

### Refactor

- **node-utils**: remove unused function (#111)
- **pyproject**: add project info (#109)
- **dependencies**: remove pandas and numpy dependencies (#96)
- **example_repos**: remove pendulum dependency (#95)
- **readme**: update intro paragraph, remove unnecessary comments (#88)
- **error-codes**: make error code checks using set instead of list (#86)
- **core**: refactor to make code easier to follow (#85)
- **help-strings**: add error codes to flake8 help strings (#82)
- **defaults**: update help strings (#81)
- **main**: update readme, change log to debug (#80)
- **restricted-imports**: add support for import restrictions (#79)
- **defaults**: update converters and add test cases (#78)
- **import-rules**: update import rules to implement restricted i… (#76)

## v0.8.10 (2023-08-02)

### Refactor

- **node-utils**: remove unused function (#111)

## v0.8.9 (2023-08-01)

### Fix

- **pyproject**: fix flake8 extension (#108)
- **node-visitor**: stdlib list should be imported locally where it is used (#106)

### Refactor

- **pyproject**: add project info (#109)

## v0.8.8 (2023-07-31)

### Refactor

- **dependencies**: remove pandas and numpy dependencies (#96)

## v0.8.7 (2023-07-31)

### Refactor

- **example_repos**: remove pendulum dependency (#95)

## v0.8.6 (2023-07-31)

### Refactor

- **readme**: update intro paragraph, remove unnecessary comments (#88)
- **error-codes**: make error code checks using set instead of list (#86)
- **core**: refactor to make code easier to follow (#85)

## v0.8.5 (2023-07-31)

### Fix

- **restricted-visitor**: refactor get strings functions (#84)

### Refactor

- **core**: refactor to make code easier to follow (#85)

## v0.8.4 (2023-07-31)

### Fix

- **visitor**: get_module_name_from_filename uses filename not file_path (#83)

### Refactor

- **help-strings**: add error codes to flake8 help strings (#82)

## v0.8.3 (2023-07-31)

### Refactor

- **defaults**: update help strings (#81)
- **main**: update readme, change log to debug (#80)
- **restricted-imports**: add support for import restrictions (#79)

## v0.8.2 (2023-07-30)

### Fix

- **default**: fix default settings (#77)

### Refactor

- **defaults**: update converters and add test cases (#78)
- **import-rules**: update import rules to implement restricted i… (#76)

## v0.8.1 (2023-07-28)

### Refactor

- **restricted-imports**: passing file packages to restricted imp… (#75)

## v0.8.0 (2023-07-28)

### Feat

- **checker**: added support for restricted imports (#69)
- **restricted-imports**: added restricted import visitor and utility functions (#68)

### Fix

- **rules-checker**: fix typing in restricted identifiers (#72)
- **file-utils**: return none if file does not exist (#71)
- add parsing for import restrictions (#67)

### Refactor

- **rules-checker**: remove extraneous code to make more efficient (#74)
- **rules-checker**: refactoring to minimize the number of calls (#73)
- **file-utils**: move file util functions to own module (#70)
- update parsing tests and plugin (#66)
- **import-rules**: update custom import rules to use closure (#65)
- cleaned up functions and improved method names (#64)

## v0.7.1 (2023-07-25)

### Refactor

- cleaned up functions and improved method names

## v0.7.0 (2023-07-25)

### Feat

- **standalone-modules**: add test cases (#62)
- **parse-utils**: add module to filename helpers (#61)
- **project-imports**: added support for non-base and non-first party (#60)
- **first-party**: updated first party to include base package (#59)
- **future**: add support for restricting __future__ imports (#58)
- **error-codes**: updated error code messages (#57)
- **third-party**: added support for third party only imports (#56)
- **imports**: update imports to straight imports (#55)
- **import-rules**: implement std lib import restrictions (#54)
- **parse-utils**: add file conversion utils (#53)
- **checker**: update checkers and parsers (#52)
- **registry**: remove old registry options (#50)
- **flake8-linter**: add register options (#49)
- **dynamic**: add custom import rules to default settings (#48)
- **import-rules**: add handling for dynamic string syntax errors (#47)
- added support for standard lib packages (#45)
- **dynamic**: added dynamic string visitor to capture dynamic string… (#44)

### Refactor

- update support for #noqa (#51)
- **error-codes**: update error code messages (#46)

## v0.6.0 (2023-07-22)

### Feat

- **dynamic**: added support for dynamic imports and fixed numerous tests (#42)

### Refactor

- **nodes**: moved parsed nodes to their own file (#43)

## v0.5.0 (2023-07-21)

### Refactor

- **import-rules**: add restrictions for main imports (#39)
- **import-rules**: add private import restrictions (#38)

## v0.4.5 (2023-07-20)

### Refactor

- **import-rules**: implement local import restrictions (#37)
- **import-rules**: add aliased import restrictions (#36)
- **import-rules**: add conditional import restrictions (#35)

## v0.4.4 (2023-07-20)

### Refactor

- **import-rules**: add relative import restrictions (#34)
- **test-cases**: updated wildcard import checks (#33)

## v0.4.3 (2023-07-20)

### Refactor

- **tests**: update tests to use linter fixture (#32)
- implement and connect import rules (#31)
- **import-rules**: remove option arguments, use option dict directly (#30)
- update setting option keys (#29)
- update linters and vistor and error codes (#28)
- **error-codes**: add properties for code and message (#27)

## v0.4.2 (2023-07-19)

### Refactor

- updated linter, checker, and visitor classes and tests (#26)

## v0.4.1 (2023-07-19)

### Refactor

- **error-codes**: update error code stem (#25)

## v0.4.0 (2023-07-19)

### Feat

- **main-package**: updated node visitor and added tests (#22)

### Refactor

- **checker**: use attrs define and field with slots (#24)

## v0.3.0 (2023-07-17)

### Feat

- **makefile**: Added linter files (#15)
- **error-codes**: defined error codes for what linter will cover (#10)

### Fix

- **error-codes**: added methods to error codes enum (#12)

### Refactor

- **import-rules**: move files into directories (#21)
- **main-package**: continuing to implement checker (#20)
- **example-package**: updating imports and docstrings (#19)
- **example-package**: rename package and updating imports (#18)
- **custom-import-rules**: update parameters (#17)
- **visitor**: Consolidate visitor classes (#16)

## v0.2.0 (2023-04-27)

### Feat

- added import rules module and parse utils and error codes (#9)
- added rules checker class to process the results of parsing through file (#8)
- add custom import rules visitor class for traversing imports (#6)

## v0.1.0 (2023-04-26)

### Feat

- added parsed import namedtuple for holding parsed imports from ast

## v0.0.1 (2023-04-24)

### Feat

- add Visitor and Plugin classes
