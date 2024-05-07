---
title: State of NBIS.se
---

# The assumptions
This state evaluation makes the following assumtions:

- We want to reduce the amount of code to maintain
- We want to keep variance from page to page low
- We want a small set of design concepts in order to make the user experience intuitive
- We want to move more content responsibility to the **Editor** role

# The way forward: Code and design
The same ideas can be used to reduce both code and the number of design concepts so I think they can be addressed together.

- Improve usage of components
- Establish conventions for how to use components
- Establish conventions for when to create a new component
  - What requires a new component?

# The general case for website content
This is not necessarily how the current NBIS.se works but the over simplified optimal case.

- Header (Fixed over entire site)
- ContentComponent[] (A collection of content components that can be described in the CMS data structures)
  - Our mission is mostly an exercise in breaking down our work into ContentComponents
- Footer (Fixed over entire site)

# The general case for website content
Taken from the concepts of Wordpress as I interpret them

- Pages: Rarely changed content that composes the structure of the site describing the structure of the organization
- Posts: A stream of content that has frequent additions and describes the current state of events or part of the organization

# Examples
A component that does too much: https://github.com/NBISweden/nbis.se/blob/develop/frontend/components/TrainingPageTemplate/training-page-template.tsx

- Renders an entire page
- Hard to reuse for other purposes
- Risk of style deviations is high
- Should it be broken down?

# Examples
A component that does too much but has a better reason to: https://github.com/NBISweden/nbis.se/blob/develop/frontend/components/Home/home.tsx

- Renders an entire page but is a **Hero** asset
- Impossible to reuse
- Risk of style deviations is high but kind of acceptable
- Should it be broken down?

# Examples
A component using and undefined standard: https://github.com/NBISweden/nbis.se/blob/develop/frontend/components/ExpandableCard/expandablecard.module.scss

- Using a direct value within a component increases the risk of deviation
- Having a consistent way of defining variables for spacing, borders and the like is important
- Only use variables in component styles in order to avoid deviation

# Examples
Hard to reuse component: https://github.com/NBISweden/nbis.se/blob/develop/frontend/components/Courses/courses.tsx

- Coding this component to use courses specifically make the design concept hard to reuse
- Passing the `Course` components as children could have been a better option
- Coding components (design concepts) for specific content types makes them harder to reuse
- Consider transform `course -> generic concept -> GenericComponent` instead

# Examples
Page with completely custom content: https://github.com/NBISweden/nbis.se/blob/develop/frontend/pages/get-support/index.tsx

- Almost impossible to reuse
- Requires a single API endpoint on its own
- Risk of deviation is high

# Moving forward
For custom pages

- Do we really need it?
- Only use existing components within a custom page

# Moving forward
For new components

- Try to find an existing component
- Can it be used?
- Can it be adapted?
- Challenge the requirement
- Write a new component

# Moving forward
For old components

- Do we have unnecessary overlap due to over specific components?
- Can we break down larger components into smaller reusable parts?
- Consider two classes of components:
- ContentComponent: A component that can easily be mapped to the structures of strapi and therefore fits well as a node in the generic site renderer
- InternalComponent: A design concept component that can be used to build a `ContentComponent` in order improve reuse and consistency

# Moving forward
Migrating to a generic site renderer

- Look at `services`
- Can we express all pages using the concepts available?
- Implement missing concepts
- Implement mapping from `specific pages` to `generic pages` in frontend while leaving strapi structure intact
- Migrate strapi content to `generic pages` or move the pages manually as the site evolves

# Going too far
Show example from experiments if we have time.