---
title: Conventional Commits
---


# Introduktion: Frågeställning

Vanliga frågor kring releasearbetet av mjukvara:

- Hur vet vi om en ny version av ett beroende fungerar med systemet?
- Hur gör vi releaser?
- Hur reducerar vi det manuella arbetet?


# Introduktion: Lösningen
- Hur vet vi om en ny version av ett beroende fungerar med systemet?
    - *Semantic versioning*
- Hur gör vi releaser?
    - *Besluta om versionsförändring, taggning, changelog*
- Hur reducerar vi det manuella arbetet?
    - *Conventional commits*
    - *Automatiska verktyg*


# Semantic versioning

- Ett tydligt sätt att beskriva hur ett API förändrats
- En grund för enklare systemuppdateringar
- Spec: [https://semver.org/](https://semver.org/)


# SemVer: Hur gör vi? För ett API

- Finns även väl dokumenterat på semver
- *PATCH*: En rättning av felaktigt beteende i ett API
- *MINOR*: En förändring av ett API som lägger till funktionalitet men bibehåller tidigare funktionalitet
- *MAJOR*: En förändring som ändrar beteendet hos eller eller flera av de publika funktionerna i ett API


# SemVer: Hur gör vi? För ett gränssnitt

- Beror lite på hur man väljer att definiera **gränssnittet**
- Finns det ett värde med detta?
- *PATCH*: En rättning som av gränssnittets beteende eller av interna funktioner
- *MINOR*: En utökning av gränssnittes funktionalitet med bibehållen tidigare funktionalitet
- *MAJOR*: En större förändring av användarupplevelsen som vid förändring av arbetssätt eller större omflyttningar i gränssnittet


# Conventional commits

- En standard för hur man skriver commit-meddelanden
- En grund för automatisering av release-processen
- Spec: [https://www.conventionalcommits.org/en/v1.0.0/](https://www.conventionalcommits.org/en/v1.0.0/)
- Verktyg: [https://www.conventionalcommits.org/en/about/](https://www.conventionalcommits.org/en/about/)


# CC: Varför?

- Changelog
- Beroendehantering
- Tydlig kommunikation


# CC: Verktyg: Commitizen

- URL: [https://github.com/commitizen-tools/commitizen](https://github.com/commitizen-tools/commitizen)
- Kika på exempel:
    - Initialisera
    - Gör några ändringar
    - Bumpa versionen
    - Gör ändringar + breaking
    - Bumpa versionen


# CC: Applicera i PLUPP

- Använda scope? (API, deploy, dev)
- Generera release med changelog från commit-log?
- Behöver vi tänka mer på historiken?
- Är det värt att applicera på *PollenDB*?