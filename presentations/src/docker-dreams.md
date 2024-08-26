---
title: Meerkats Docker
subtitle: The dreams of the future
---

# Wanted properties of a docker container

- The layers are set up to use the caching ordering layers in the expected order of number of changes
- Dependecies should be built into the container unless they are prohivitively large (avoid dependencies in volumes in prod)
- In development it is sometimes preferrable to mount some dependecies to allow for them to be shared with the IDE
- A deployed image should never leave artifacts other than user content
- A deployed container should never be dependent on host resources other than configuration parameters
- Configuration data should generally supplied using the ENV properties


# Docker compose layers

- It is nice to use stacked docker compose files for different environments
- Should we use a production first style or a dev first style?
- In dev the containers should be configured to never restart (when shutting down the computer we want the container space to be cleared)