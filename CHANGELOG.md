## v0.8.3 (2023-07-31)

### Refactor

- **help-strings**: add error codes to flake8 help strings
- **defaults**: update help strings (#81)
- **main**: update readme, change log to debug (#80)
- **restricted-imports**: add support for import restrictions (#79)

## v0.8.2 (2023-07-30)

### Fix

- **default**: fix default settings (#77)

### Refactor

- **restricted-imports**: add support for import restrictions
- **defaults**: update converters and add test cases (#78)
- **import-rules**: update import rules to implement restricted i… (#76)

## v0.8.1 (2023-07-28)

### Refactor

- **import-rules**: update import rules to implement restricted identifiers
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

- **restricted-imports**: passing file packages to restricted import visitor
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

- **isolated-modules**: add test cases (#62)
- **parse-utils**: add module to filename helpers (#61)
- **project-imports**: added support for non-base and non-first party (#60)
- **first-party**: updated first party to include base package (#59)
- **future**: add support for restricting __future__ imports (#58)
- **error-codes**: updated error code messages (#57)
- **third-party**: added support for third party only imports (#56)
- update imports to straight imports (#55)
- **import-rules**: implement std lib import restrictions (#54)
- **parse-utils**: add file conversion utils (#53)
- update checkers and parsers (#52)
- remove old registry options (#50)
- **flake8-linter**: add register options (#49)
- **import-rules**: add custom import rules to default settings (#48)
- add handling for dynamic string syntax errors (#47)
- added support for standard lib packages (#45)
- **dynamic**: added dynamic string visitor to capture dynamic string… (#44)

### Refactor

- update support for #noqa (#51)
- **error-codes**: update error code messages (#46)

## v0.6.0 (2023-07-22)

### Feat

- **dynamic**: added dynamic string visitor to capture dynamic string imports
- added support for dynamic imports and fixed numerous tests (#42)

### Refactor

- **nodes**: moved parsed nodes to their own file (#43)

## v0.5.0 (2023-07-21)

### Feat

- added support for dynamic imports and fixed numerous tests

### Refactor

- **import-rules**: add restrictions for main imports (#39)
- **import-rules**: add private import restrictions (#38)

## v0.4.5 (2023-07-20)

### Refactor

- **import-rules**: add private import restrictions
- **import-rules**: implement local import restrictions (#37)
- **import-rules**: add aliased import restrictions (#36)
- **import-rules**: add conditional import restrictions (#35)

## v0.4.4 (2023-07-20)

### Refactor

- **import-rules**: add conditional import restrictions
- **import-rules**: add relative import restrictions (#34)
- **test-cases**: updated wildcard import checks (#33)

## v0.4.3 (2023-07-20)

### Refactor

- **test-cases**: updated wildcard import checks
- **tests**: update tests to use linter fixture (#32)
- implement and connect import rules (#31)
- **import-rules**: remove option arguments, use option dict directly (#30)
- update setting option keys (#29)
- update linters and vistor and error codes (#28)
- **error-codes**: add properties for code and message (#27)

## v0.4.2 (2023-07-19)

### Refactor

- **error-codes**: add properties for code and message
- updated linter, checker, and visitor classes and tests (#26)

## v0.4.1 (2023-07-19)

### Refactor

- updated linter, checker, and visitor classes and tests
- **error-codes**: update error code stem (#25)

## v0.4.0 (2023-07-19)

### Feat

- **main-package**: updated node visitor and added tests (#22)

### Refactor

- **error-codes**: update error code stem
- **checker**: use attrs define and fied with slots (#24)

## v0.3.0 (2023-07-17)

### Feat

- **main-package**: updated node visitor and added tests
- **makin**: Added linter files (#15)
- defined error codes for what linter will cover (#10)

### Fix

- added methods to error codes enum (#12)

### Refactor

- **import-rules**: move files into directories (#21)
- **main-package**: continuuing to implement checker (#20)
- **example-package**: updating imports and docstrings (#19)
- **example-package**: rename package and updating imports (#18)
- **custom-import-rules**: update parameters (#17)
- **visitor**: Consolidate visitor classes (#16)

## v0.2.0 (2023-04-27)

### Feat

- defined error codes for what linter will cover
- added import rules module and parse utils and error codes (#9)
- added rules checker class to process the results of parsing through file (#8)
- add custom import rules visitor class for traversing imports (#6)

## v0.1.0 (2023-04-26)

### Feat

- added parsed import namedtuple for holding parsed imports from ast

## v0.0.1 (2023-04-24)

### Feat

- add Visitor and Plugin classes
