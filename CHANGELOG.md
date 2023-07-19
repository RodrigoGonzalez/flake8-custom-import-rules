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
