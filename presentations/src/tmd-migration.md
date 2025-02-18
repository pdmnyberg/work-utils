---
title: Rubberducking the TMD
---


# The current structure
- The current `Model` is very rigid
    - Fixed sets: (`Quality`, `Impact`, `Demographic`)
    - Fixed fields
    - Fixed field domains
- The current `Model` has a sketchy structure
    - Everything is stored as string
    - The string are not exakt matches to the old field domains


# The new model

- `Question`: Represents questions
- `QuestionSet`: Represents a set of questions
- `QuestionSuperSet`: Represents a collection of QuestionSets


# Question

- `Question`
    - Represents questions
    - Label for reading allowing editing that does not change the meaning of the question
    - Immutable id for referencing
    - Single choice or multi choice

# QuestionSet

- `QuestionSet`
    - Represents a set of questions
    - Name and description mostly used for identification
    - Immutable id for referencing

# QuestionSuperSet

- `QuestionSuperSet`
    - Represents a collection of QuestionSets
    - Name for identification
    - Immutable id for referencing
    - Carries properties describing how to use the collection of questions


# Migrating to the new model

- Test the migration functions
- Test as little as possible while achieving a satisfying coverage


# The approach

- Aim for a generalized implementation
- Write a function that can verify compatibility between of either `Quality`, `Impact` or `Demographic` and any `QuestionSet`
- Write a function that can transfer data from a either `Quality`, `Impact` or `Demographic` to any compatible `QuestionSet`
- Test the generic functionality


# Caveats

- There are some values that we want to convert while transfering
- We will need to test the conversion completely
    - In the data transfer
    - In the compatibility check
