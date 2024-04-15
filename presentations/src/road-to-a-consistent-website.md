---
title: Vägen till en konsekvent hemsida
---

# Introduktion: Användarupplevelsen
- Hur står det till egentligen?
- Hur ser första intrycket ut?
- Hur relaterar helhetsupplevelsen till första intrycket?
- Hur ser läget ut för en innehållsansvarig?

# Hur står det till egentligen?
- Idag har vi vissa problem med att sidan inte alltid har en konsekvent stil
  - Storlekar på text:  [about](https://nbis.se/about), [get-support](https://nbis.se/get-support)
  - Mellanrum mellan element: h[about](https://nbis.se/about), [bioinformatics](https://nbis.se/services/bioinformatics)
  - Kantutrymmen: [about](https://nbis.se/about), [training](https://nbis.se/training)
  - Interaktionsmönster: [about](https://nbis.se/about), [training](https://nbis.se/training), [facts-and-figures](https://nbis.se/about/facts-and-figures)
- Är det ett problem?

# Hur ser första intrycket ut?
- Startsidan kan vara lite som en tutorial för vad man kan förvänta sig av en hemsida
- Startsidan kan vara en lite mer utsvävande presentation
- Det borde kännas naturligt att kliva från startsidan vidare till innehållet
- Exempel: [nf-core](https://nf-co.re/) och [Data Centre](https://data.scilifelab.se/)

# Hur relaterar helhetsupplevelsen till första intrycket?
- Känns det intuitivt att interagera med resten av siten efter att man besökt startsidan?
- Kan vi bli bättre på att återanvända interaktionsmönster?

# Hur ser läget ut för en innehållsansvarig?
- Idag finns det många unika sidor med egna typer
- Är många unika sidor med så variationer det bästa sättet att beskriva det vi behöver?
- Hur ser det ut med flexibiliteten i nuvarande lösning?
- Service-sidorna är ett intressant exempel: [Service pages på github](https://github.com/NBISweden/nbis.se/blob/develop/frontend/pages/services/%5B%5B...slug%5D%5D.tsx)


# Introduktion: Utvecklarupplevelsen
- Hur hittar man i kodbasen?
- Hur minskar vi behovet av underhåll?
- Hur minskar vi kodduplicering?
- Hur tänker vi kring komponenter?
- Hur förstärker vi innehållsansvarig på bästa sätt?

# Hur hittar man i kodbasen?
- Enligt standard för Next -> hierarkin styr url
- Utifrån vad jag sett leder det lätt till att man sprider ut koncept och koddelning blir i viss mån lidande
- Är det ett riktigt behov att ha så många unika sidtyper?

# Hur minskar vi behovet av underhåll?
- Mindre kod -> mindre underhåll
- Ökad mängd datadrivet innehåll -> mindre underhåll
- Pragmatiska designbeslut -> mindre underhåll

# Hur minskar vi kodduplicering?
- Ökat användande av existerande komponenter
- Undvik att använda standard-html utanför komponenter
- Gå igenom existerande komponenter innan nya implementeras
- Bryt ner komplicerade komponenter till enklare återanvändbara koncept
- Bygg koncept som är mer generiska
- Fler möjligheter?

# Hur tänker vi kring komponenter?
- Komponenter är som byggklossar eller Lego
- Hur lätt är det att återanvända specialbitarna i Lego?
- Vilken nivå är rimlig att lägga sig på?

# Hur förstärker vi innehållsansvarig på bästa sätt?
- Reducera mängden koncept att arbeta med för att göra det enklare att förstå
- Gör sidor mer flexibla i stil med Service-sidorna
- Minska behovet för utvecklare vid framtagande av nytt material