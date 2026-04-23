---
title: Using django translations
geometry: "left=3cm,right=3cm,top=2cm,bottom=2cm"
---

# Using translations
This document tries to give a short introduction on how to add translations to an existing django project. It will take you through the necessary steps:
- [Dependencies](#dependencies)
- [Basic configuration](#basic-configuration)
- [Using translations in code](#using-translations-in-code)
- [Working with translation files](#working-with-translation-files)
- [Preparing translations for runtime](#preparing-translations-for-runtime)
- [Getting localized responses](#getting-localized-responses)

At the end of the documents there are som additional [notes](#notes) related to how to use translations in pactice.

## Dependencies
In order to work with translations in django it is necessary to have `GNU gettext` installed on your system.

## Basic configuration
In order to use translations, a number of configuration options need to be in place.

- `LANGUAGE_CODE`: The fallback language to use when other detection options fail see section about user language detection.
- `LANGUAGES`: A list of available languages. Using standardized language codes.
- `USE_I18N`: Should be `True` when using translations,
- `LOCALE_PATHS`: Defines where locales can be generated and located,
- `MIDDLEWARE`: In order to have django detect user language you need to add `django.middleware.locale.LocaleMiddleware` to the list of middleware.

An example config can look like this.

```python
MIDDLEWARE = [
    #...,
    "django.middleware.locale.LocaleMiddleware",
    #...
]

LANGUAGE_CODE = "sv"

LANGUAGES = [
    ("sv", _("Swedish")),
    ("en", _("English")),
]

USE_I18N = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

```

## Using translations in code

When adding translations it is sometimes important to think about when a string is being processed by python. In some cases the string/value will be read while the script is loading and sometimes they will be read during runtime. These two cases are important to distinguish in order to add translations properly.

Cases when where the string/value is being read while the script is loading are:
- Values declaratively assigned to an object or class 
- Most things outside the scope of a function
- Probalby a number of other things

In this case it is appropriate to use `gettext_lazy`. Example cases are model and other type definitions.

```python
from django.utils.translation import gettext_lazy as _
from django.db import models

class Choices(models.IntegerChoices):
    A = (1, _("Value of A"))
    B = (2, _("Value of B"))
```

For the other cases where the code is enclosed within a function it is appropriate to use `gettext`.

```python
from django.utils.translation import gettext as _

def my_translated_value():
    return _("Translate this")
```

The distinction between `gettext_lazy` and `gettext` is that `gettext` will return a translated string immediately while `gettext_lazy` will return a proxy value that can be evaluated to a transalted string by casting it to a string `str(proxy_value)`.


## Working with translation files
After successfully configuring `LOCALE_PATHS` and adding your first translatable strings using `gettext`, you can generate message files which will contain your future translations. This can be done by using djangos `manage.py` script as follows.

```sh
# The following examples uses the english and swedish language code respectively
./manage.py makemessages -l en
./manage.py makemessages -l sv
```

These commands will generate message files in your `LOCALE_PATHS` directory (`{LOCALE_PATHS}/{language_code}/LC_MESSAGES/django.po`) and the content will look something like this:

```po
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2026-04-22 09:00+0000\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"Language: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"

#: bird_ringing/settings.py:146
msgid "Swedish"
msgstr ""

#: bird_ringing/settings.py:147
msgid "English"
msgstr ""
```

Translation work will invlove adding the respective translation in every `msgstr` associated with a `msgid`. Adding more `gettext` translations in your code and running `./manage.py makemessages -l <lang_code>` again will include the additions in your `django.po` while keeping the existing translations.

## Preparing translations for runtime
When you have created you translation messages files you will need to compile them in order to make the translations usable in runtime. This can be done by using djangos `manage.py` script as follows:

```sh
python manage.py compilemessages
```

This will generate corresponding `django.mo` for every `django.po` in your `LOCALE_PATHS` directory. The `django.mo` file can generally be excluded from version control since they are a result generated from the content of your `django.po` files.

## Getting localized responses
The user language is determined using the following priority order:
1. User session
2. Language in cookies
3. `Accept-Language` header in the request
4. Using the setting `LANGUAGE_CODE`


### Extras
Have a look at `i18n_patterns` if you want to be able to select language using the url rather than other variants.

## Notes

When using translations while providing a REST API it might be useful to keep `ENUM` like properties uniquely identifiabe yet human readable. This can be done providing a returned type that includes both an `id` and a `label`. Where both `id` and `label` are strings but `label` is translated to the identified langauge. If that makes the result structure to intricate I would recommend avoid translating the results from the REST API.

When using translations for an `models.IntegerChoices` the above reasoning can be applied as follows. Note that this is only an example of how to transform the data and not how to implement an actual serializer. The point here is to use a stable human readable `id` which `models.IntegerChoices.name` provides while the `models.IntegerChoices.label` provides the translated label for the value.

```python
# ...

class Choices(models.IntegerChoices):
    A = (1, _("Value of A"))
    B = (2, _("Value of B"))

def enum_like_api_response_for_Choices(value):
    return {
        "id": str(Choices(value).name).lower(),
        "label": Choices(value).label,
    }
```