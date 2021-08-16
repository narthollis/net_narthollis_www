+++
title = "Internet Explorer <8 and <select>"
template = "page.html"
date = 2010-08-23T03:34:00Z
[taxonomies]
tags = ["internet explorer","html"]
[extra]
mathjax = "tex-mml"
+++

I have recently encountered a number of issues relating to populating &lt;select&gt; elements using JavaScript. The largest issue I was having was with &lt;select&gt; elements that were themselves created using JavaScript. In this case the elements would be un-selectable.

<!-- more -->

If you clicked on them, or tabbed to them; then they would highlight, but nothing else.

The issue it turns out is caused by the way that Internet Explorer &lt;8 handles &lt;select&gt; lists. More to the point the way that it treats them as special elements, not standard HTML elements. I was simply appending the &lt;option&gt; elements to the &lt;select&gt; as DOM child nodes. While this works correctly in every other web browser I tested (Chrome 4>, FF 3.5>, IE8) it doesn't work in IE7, which was a requirement for the project. It turns out that in Internet Explorer if you want to add more options to a &lt;select&gt; element you need to create new Option objects and append them to the &lt;select&gt;.objects 'array' (I say 'array' as its not really an array... but it behalves enough like one).

(Note, I am using [Prototype][2] language extensions in the below example)
```js
var select = document.getElementById('mySelect');
var options = new Hash({'0': 'ACT', '1': 'SA', '2': 'NT', '3': 'NSW', '4': 'Vic', '5': 'Tas', '6': 'WA', '7': 'Qld'});
var i = 0;
options.each(function(opt) {
  select.options[i] = new Option(opt.value, opt.key, null, false);
  i = i++;
});
```

I hope this helps you if you are also having random issues with &lt;select&gt; elements and Internet Explorer.

[2]: http://prototypejs.org/ "Prototype JavaScript framework"
