# strpy
String Python (or stringify-python) is an object-to-string converter that respects python types. If JSON got XML pregnant and genetic engineers altered the baby's DNA to include python, this would be the result.
## Installation
I dunno. Copy the code for all I care.
## Usage
Say you have a big dict (or list or set or whatever) that you want to be TOTALLY flat ascii -- no single- or double-quotes, no backslashes, no unicode, nothing...
```
complexdd = {u'imgs': {u'ff': 45,
                       u'fl': 55,
                       u'descriptors': ('forward', 'backward', 'up', 'down'),
                       u'filepath': u'/path/to/a/file.txt'},
 u'maps': {u'america': [[u'san francisco', u'colorado', 120000000L, 1j, 'strings'], ['bond', '007']],
           u'ussr': False,
           u'this_guy': u'a string \\ with a lot \\ of "double quotes" and \\backslashes\\',
           u"this_guys_bro": u"a string with 'single' quotes."},
 u'a set': {1, 3L, True}, u'a-tupleset': {(2, 3), (4, 5)}, u'atuple': (u'\u263a', True, False,),
 u'paragraphs': '''Whose woods these are I think I know.
                   His house is in the village though;
                   He will not see me stopping here
                   To watch his woods fill up with snow.

                   My little horse must think it queer
                   To stop without a farmhouse near
                   Between the woods and frozen lake
                   The darkest evening of the year.

                   He gives his harness bells a shake
                   To ask if there is some mistake.
                   The only other sound's the sweep
                   Of easy wind and downy flake.

                   The woods are lovely, dark and deep,
                   But I have promises to keep,
                   And miles to go before I sleep,
                   And miles to go before I sleep.''',
 u'meta': u'holy cow! {{this}}has tags!{{/this}} but {li0}it{/li0} is a string.',
 u'haiku': u"Wake, butterfly\n\rit's late\u2011\n\rwe've miles to go together.\xa0",
 u'frozen_set': frozenset(['a', 'b', '\\backslash\\'])}
```
Well, you do this...
`flatstring = strpy.dumps(complexdd)`
And you get this...
```
print flatstring
{di0}{li1}{tu2}{un}a set{/un}{se4}{bo}True{/bo}{lo}3{/lo}{/se4}{/tu2}{tu3}{un}maps{/un}{di5}{li6}{tu7}{un}ussr{/un}{bo}False{/bo}{/tu7}{tu8}{un}this_guys_bro{/un}{un}a string with {/sq/}single{/sq/} quotes.{/un}{/tu8}{tu9}{un}america{/un}{li11}{li12}{un}san francisco{/un}{un}colorado{/un}{lo}120000000{/lo}{co}1j{/co}{st}strings{/st}{/li12}{li13}{st}bond{/st}{st}007{/st}{/li13}{/li11}{/tu9}{tu10}{un}this_guy{/un}{un}a string {/bs/} with a lot {/bs/} of {/dq/}double quotes{/dq/} and {/bs/}backslashes{/bs/}{/un}{/tu10}{/li6}{/di5}{/tu3}{tu4}{un}meta{/un}{un}holy cow! {{this}}has tags!{{/this}} but {li0}it{/li0} is a string.{/un}{/tu4}{tu5}{un}a-tupleset{/un}{se7}{tu8}{in}4{/in}{in}5{/in}{/tu8}{tu9}{in}2{/in}{in}3{/in}{/tu9}{/se7}{/tu5}{tu6}{un}atuple{/un}{tu8}{un}{/9786/}{/un}{bo}True{/bo}{bo}False{/bo}{/tu8}{/tu6}{tu7}{un}imgs{/un}{di9}{li10}{tu11}{un}descriptors{/un}{tu13}{st}forward{/st}{st}backward{/st}{st}up{/st}{st}down{/st}{/tu13}{/tu11}{tu12}{un}fl{/un}{in}55{/in}{/tu12}{tu13}{un}ff{/un}{in}45{/in}{/tu13}{tu14}{un}filepath{/un}{un}/path/to/a/file.txt{/un}{/tu14}{/li10}{/di9}{/tu7}{tu8}{un}paragraphs{/un}{st}Whose woods these are I think I know.\n                   His house is in the village though;\n                   He will not see me stopping here\n                   To watch his woods fill up with snow.\n\n                   My little horse must think it queer\n                   To stop without a farmhouse near\n                   Between the woods and frozen lake\n                   The darkest evening of the year.\n\n                   He gives his harness bells a shake\n                   To ask if there is some mistake.\n                   The only other sound{/sq/}s the sweep\n                   Of easy wind and downy flake.\n\n                   The woods are lovely, dark and deep,\n                   But I have promises to keep,\n                   And miles to go before I sleep,\n                   And miles to go before I sleep.{/st}{/tu8}{tu9}{un}haiku{/un}{un}Wake, butterfly\n\rit{/sq/}s late{/8209/}\n\rwe{/sq/}ve miles to go together.{/160/}{/un}{/tu9}{tu10}{un}frozen_set{/un}{fr12}{st}a{/st}{st}b{/st}{st}{/bs/}backslash{/bs/}{/st}{/fr12}{/tu10}{/li1}{/di0}
```
And you can go back using this...
`origdict = strpy.loads(flatstring)`
If you don't believe me, you can do this...
`origdict == complexdd`
...which will return `True`. I promise.
## Contributing
1. Fork!
2. Update with a feature branch: `git checkout -b some-tests-finally-you-jerk`
3. Commit to the cause: `git commit -am 'Now there are tests, you lazy programmer. AND proper python etiquette for distributing code. Get a job!'`
4. K... Push to the branch: `git push origin some-tests-finally-you-jerk`
5. Submit a "PR", which I'm told is short for "pull request".
## History
One day, I might write a test, but I'm pretty sure it's bullet-proof.
## Credits
I am Chris.
## License
Just don't say you wrote it yourself, you hack. Link to here or something.
