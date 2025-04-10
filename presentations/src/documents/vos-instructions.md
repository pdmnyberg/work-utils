---
title: Crispr web app instruction
geometry: "left=2cm,right=2cm,top=1cm,bottom=1cm"
---

# Setup volume
The following image describes how to setup the container with a volume. The important properties are `Volume`, `Path` and in this case `Image`.

![Setup container with volume](resources/vos-instructions/01.png){ width=70% }

# Manage files
To mange files you first have to create a `File Manager`. This can be done in the `Manage Files` section. When you have created a file manager for your volume you can find it in the list of file manager. Use it by pressing the link `File Manager`.

![Setup file manager](resources/vos-instructions/02.png){ width=70% }

## Creating a message
To add a message your volume needs to have the following file structure:

```
<root-of-volume>:
    vector_oligo_search:
        search.md
        page:
            <page-id>.md
```

The files `search.md` and `<page-id>.md` need to comply with the markdown standard and may contain a frontmatter segment describing the message. An example can look as follows:

```
---
type: danger
---

This is a real test warning.

Look out!
```

Where the `type` can be `danger`, `warning`, `info`.

Setting this up using serve.scilifelab.se can look as follows:

![Navigate to file manager](resources/vos-instructions/03.png)
![Root of file manager](resources/vos-instructions/04.png)
![Message root of file manager](resources/vos-instructions/05.png)
![An example message](resources/vos-instructions/06.png)


