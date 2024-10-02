---
title: Concerning testing
---

# Concerning testing

- What is it?
- Why do we need it?
- When should we use it?
- How do we use it?




# What is it?
- Unit testing
- System testing
- Integration testing
- Regression testing

# Unit testing
> Unit is defined as a single behaviour exhibited by the system under test (SUT), usually corresponding to a requirement.
> From the system-requirements perspective only the perimeter of the system is relevant, thus only entry points to externally-visible system behaviours define units.

> Testing is often performed by the programmer who writes and modifies the code under test. Unit testing may be viewed as part of the process of writing code. 

- Discuss unit in the context of PLUPP and NBIS.se

# System testing
> System testing, a.k.a. end-to-end (E2E) testing, is testing conducted on a complete software system. 

- Discuss system definition in the context of PLUPP and NBIS.se

# Integration testing
> Integration testing, also called integration and testing, abbreviated I&T, is a form of software testing in which multiple parts of a software system are tested as a group.

- Discuss integration layer definition in the context of PLUPP and NBIS.se

# Regression testing
> Regression testing is re-running functional and non-functional tests to ensure that previously developed and tested software still performs as expected after a change. If not, that would be called a regression.

- Discuss the definition of regression testing
- Can we perform regression testing without first having functional tests?
- Discuss regression testing in the context of PLUPP and NBIS.se




# Why do we need it?

- Quality assurance in general
- Make sure units fullfils the expectations
- Make sure system parts work well together
- Make sure the code keeps working when introducing changes




# When should we use it?

- Always
- When appropriate
- It depends


# When refactoring
- Writing regression tests for the external interface of what you want to change the implementation of will reduce the risk of introducing new bugs
- Writing unit tests for the core concepts of the new implementation can help verify where errors happen while figuring out the implementation


# When fixing bugs
- When fixing a bug we want to make sure it is not reintroduced later. Adding a test that verifies the fix does this.
- When code has existing tests we can be sure that a bug fix does not introduce new bugs


# When building new features
- Writing tests for new code it is a good way of making sure your assertions about the code are true
- When the code has existing tests it is easier to know when your added functionality breaks existing functionality

# Before deploying
- Running integrations tests verifies that the systems to be deployed all work together




# How do we use it?
- Look at django in PLUPP
- Look at javascript in PLUPP/Sitevision




# Attribution

All quotes are taken from Wikipedia articles for the respective subject and use the license [Creative Commons ShareAlike](https://en.wikipedia.org/wiki/Wikipedia:Text_of_the_Creative_Commons_Attribution-ShareAlike_4.0_International_License)
