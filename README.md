# font_integrity_tool
This tool checks the integrity of the font files.

It checks the glyphs from unicode U+0020, and identifies if there are any unnecessary spaces.

Allowed spaces are:
 - U+0020 : Space
 - U+0085 : Next Line
 - U+00A0 : No-break Space(NBSP)
 - U+1680 : Ogham Space Mark
 - U+180E : Mongolian Vowel Separator
 - U+2000 : En Quad
 - U+2001 : Em Quad
 - U+2002 : En Space
 - U+2003 : Em Space
 - U+2004 : Three-Per-Em Space
 - U+2005 : Four-Per-Em Space
 - U+2006 : Six-Per-Em Space
 - U+2007 : Figure Space
 - U+2008 : Punctuation Space
 - U+2009 : Thin Space
 - U+200A : Hair Space
 - U+200B : Zero Width Space
 - U+200C : Zero Width Non-joiner
 - U+200D : Zero Width Joiner
 - U+2028 : Line Separator
 - U+2029 : Paragraph Separator
 - U+202F : Narrow NBSP
 - U+205F : Medium Mathematical Space
 - U+2060 : Word Joiner
 - U+3000 : Ideographic Space
 - U+FEFF : Zero Width NBSP
