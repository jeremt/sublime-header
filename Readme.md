#Sublime Header

It's a simple plugin which generates an epitech norme compatible header.

##Install

###Manual installation

[Download](https://github.com/jeremt/header/archive/master.zip) the plugin or clone the repository.

Then copy the containing folder into your SublimeText __Packages__ folder: _Preferences_ -> _Browse Packages_...

###With Package Control

Add https://github.com/jeremt/sublime-header as a new repository :
    __ctrl+shift+p__ -> _Package Control: Add repository_

Install it :
    __ctrl+shift+p__ -> _Package Control: Install package_
    "Sublime Header"

You can configure the package by editing Sublime header settings :

_Preferences_ -> _Package Settings_ -> _Sublime Header_ -> _Settings - User_

````json
{
    "name" : "Your Name",
    "mail" : "your.mail@mailbox.com",
    "allowed_languages" :
    [
        "Python",
        "C"
    ],
    "disallowed_languages" :
    [
        "JSON",
        "Markdown"
    ],
}
````

(Sublime Header will check if current file syntax is in the disallowed list first, then check if it is in the allowed list. You can use one or both lists)


##Usage

Just press __ctrl+shift+h__ to generate a header at the top of the file.


## TODO
- Add all languages
- Configuration file to create custom headers

##License

(The MIT License)

Copyright (c) 2012 Jeremie T. taboada.jeremie@gmail.com

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
