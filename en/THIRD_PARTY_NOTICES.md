# Third-party notices

This course (“CLPN From Scratch”) is © 2026 ZHANG; its course content is licensed under CC BY 4.0 and its code under the MIT License (see `LICENSE` for which paths are which).
The following bundled third-party components and data are **not** covered by those licences; they remain under their own licences, reproduced below.

| Component | Version | Location in this repository / website | Licence |
|---|---|---|---|
| KaTeX (incl. `contrib/auto-render`, CSS and fonts) | 0.16.11 | `lessons/assets/vendor/katex/` | MIT — full text in `lessons/assets/vendor/katex/LICENSE` |
| JetBrains Mono (latin subset, weights 400 / 600, woff2) | — | `lessons/assets/vendor/fonts/` | SIL Open Font License 1.1 — full text in `lessons/assets/vendor/fonts/OFL-JetBrainsMono.txt` |
| Dataset “Positive mental health among sports coaches: A six-month longitudinal study” (file `PMH_Coaches_data.csv`, unmodified) | Dryad version 3 (2023) | `data/coaches_mhc_raw.csv` | CC0 1.0 Universal (public domain dedication) — see the section below |

The course download `downloads/clpn-course.zip` contains the offline website and therefore both components above (under `clpn-course/lessons/assets/vendor/`, each with its own licence file); this notice and `LICENSE` are included at the top level of the zip. The zip also contains `data/coaches_mhc_raw.csv`.

`data/elsoc_phq8_wide.csv` is a subset of the ELSOC panel: original sample, PHQ items 1–8 for waves 2016–2018, sex and age, with new row ids. It was derived by `R/data_elsoc.R` from the file `ELSOC_Wide_2016_2021_v1.00_R.RData` of Reproducible Research, Centre for Social Conflict and Cohesion Studies COES, 2022, "Estudio Longitudinal Social de Chile 2016-2021", https://doi.org/10.7910/DVN/LQMURF, Harvard Dataverse, V1, UNF:6:z/vWFguq9fg03YaOLWFddA== [fileUNF]. Dataverse marks that version CC0 1.0 (public domain dedication); it is redistributed under CC0. The original file is bundled unmodified as `data/elsoc/ELSOC_Wide_2016_2021_v1.00_R.RData` (MD5 a5a45571d39cf9db12e1949fdcb6fff2), also under CC0. The zip contains both files.

---

## KaTeX — MIT License

```
The MIT License (MIT)

Copyright (c) 2013-2020 Khan Academy and other contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## JetBrains Mono — SIL Open Font License, Version 1.1

```
Copyright 2020 The JetBrains Mono Project Authors (https://github.com/JetBrains/JetBrainsMono) JetBrainsMono-Italic[wght].ttf: Copyright 2020 The JetBrains Mono Project Authors (https://github.com/JetBrains/JetBrainsMono)

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at:
http://scripts.sil.org/OFL


-----------------------------------------------------------
SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007
-----------------------------------------------------------

PREAMBLE
The goals of the Open Font License (OFL) are to stimulate worldwide
development of collaborative font projects, to support the font creation
efforts of academic and linguistic communities, and to provide a free and
open framework in which fonts may be shared and improved in partnership
with others.

The OFL allows the licensed fonts to be used, studied, modified and
redistributed freely as long as they are not sold by themselves. The
fonts, including any derivative works, can be bundled, embedded,
redistributed and/or sold with any software provided that any reserved
names are not used by derivative works. The fonts and derivatives,
however, cannot be released under any other type of license. The
requirement for fonts to remain under this license does not apply
to any document created using the fonts or their derivatives.

DEFINITIONS
"Font Software" refers to the set of files released by the Copyright
Holder(s) under this license and clearly marked as such. This may
include source files, build scripts and documentation.

"Reserved Font Name" refers to any names specified as such after the
copyright statement(s).

"Original Version" refers to the collection of Font Software components as
distributed by the Copyright Holder(s).

"Modified Version" refers to any derivative made by adding to, deleting,
or substituting -- in part or in whole -- any of the components of the
Original Version, by changing formats or by porting the Font Software to a
new environment.

"Author" refers to any designer, engineer, programmer, technical
writer or other person who contributed to the Font Software.

PERMISSION & CONDITIONS
Permission is hereby granted, free of charge, to any person obtaining
a copy of the Font Software, to use, study, copy, merge, embed, modify,
redistribute, and sell modified and unmodified copies of the Font
Software, subject to the following conditions:

1) Neither the Font Software nor any of its individual components,
in Original or Modified Versions, may be sold by itself.

2) Original or Modified Versions of the Font Software may be bundled,
redistributed and/or sold with any software, provided that each copy
contains the above copyright notice and this license. These can be
included either as stand-alone text files, human-readable headers or
in the appropriate machine-readable metadata fields within text or
binary files as long as those fields can be easily viewed by the user.

3) No Modified Version of the Font Software may use the Reserved Font
Name(s) unless explicit written permission is granted by the corresponding
Copyright Holder. This restriction only applies to the primary font name as
presented to the users.

4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
Software shall not be used to promote, endorse or advertise any
Modified Version, except to acknowledge the contribution(s) of the
Copyright Holder(s) and the Author(s) or with their explicit written
permission.

5) The Font Software, modified or unmodified, in part or in whole,
must be distributed entirely under this license, and must not be
distributed under any other license. The requirement for fonts to
remain under this license does not apply to any document created
using the Font Software.

TERMINATION
This license becomes null and void if any of the above conditions are
not met.

DISCLAIMER
THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
OTHER DEALINGS IN THE FONT SOFTWARE.
```

---

## Sports-coach mental health data — CC0 1.0

`data/coaches_mhc_raw.csv` is the unmodified file `PMH_Coaches_data.csv` (63,813 bytes, MD5 `c89921f505a473ab4084b761fb5567e6`) from:

> Ackeret, N., Röthlin, P., Horvath, S., & Allemand, M. (2023). *Positive mental health among sports coaches: A six-month longitudinal study* [Dataset, version 3]. Dryad. https://doi.org/10.5061/dryad.8931zcrws

Related article: Ackeret, N., Röthlin, P., Horvath, S., & Allemand, M. (2024). Positive mental health among sports coaches: A 6-month longitudinal study. *Sport, Exercise, and Performance Psychology, 13*(1), 76–88. https://doi.org/10.1037/spy0000335

The dataset is dedicated to the public domain under the Creative Commons CC0 1.0 Universal Public Domain Dedication (https://creativecommons.org/publicdomain/zero/1.0/legalcode), as stated on its Dryad page and in its DataCite metadata. No permission is needed to redistribute it; we cite it as good scholarly practice. The course uses it only for the measurement-invariance exercise of lesson 7.6. Known problems with the file (summary columns that do not match the item columns; conflicting descriptions of the wave spacing) are documented in `data/data_dictionary.md`.
