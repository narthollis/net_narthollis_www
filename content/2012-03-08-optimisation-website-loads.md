+++
title = "Optimisation of Website Loads"
template = "page.html"
date = 2012-03-08T04:34:00Z
[taxonomies]
tags = ["html","httpd","rant"]
[extra]
mathjax = "tex-mml"
+++

So Today I was linked to an article about optimising your you web server by updating your Linux kernel to make use of a larger [initial congestion window][1].

So this lead me to wander about some simpler optimisations, something any web developer can realistically do when they deploy an application, and just how much of an effect these opermisations have on a website.

## Method ##
So the first thing I looked at was the load times for a JavaScript heavy project I am currently working on, TimTam.

I used the excellent free service [Web Page Test][2] to test the load times of the website with various configurations of its JavaScript files.

## Tests ##
### Test 1 ###
[The first test][3] was done with out doing any alterations to the development code base.
It shows that the webpage took about 1.1 seconds to load. Which I think it quite good for something I am yet to optimise, which to me would make the results of the test that much more interesting.
### Test 2 ###
[The seconds test][4] was done on a page that loaded of the JavaScript for the project from a single file. I was expecting some increase in speed here, maybe 0.2s at most. What I actually got really surprised me though, this page loaded in 0.81s - this is about a 40% improvement.
### Test 3 ###
[The third test][5] was mostly an after though, and was to use a minified (or in this case [closure compiled][6]) copy of the combined script. After the previous test got such a large improvement I was expecting a rather small jump here. That said, before I ran the script through closure, it was about 95KB and afterwards it was only 45KB - this made me somewhat optimistic for a reasonable improvement. It turns out I should have stuck with my original expectations, as there was only a 5% improvement in load times. Though given that the file is now less than half its original size, anyone who is trying to reduce their bandwidth will love this one.

## Conclusion ##
In conclusion I would say that all web developers should be looking to at the very least consolidate all of their resource files (JavaScript, CSS, and small icons) into larger singular files as much as possible when preparing their projects for deployment.

I would also say that were they can, minifiing these files is also useful - but less so for load times and more so for general site performance.

[1]: http://samsaffron.com/archive/2012/03/01/why-upgrading-your-linux-kernel-will-make-your-customers-much-happier "Why upgrading your Linux Kernel will make your customers much happier"
[2]: http://www.webpagetest.org/ "Web Page Test"
[3]: http://www.webpagetest.org/result/120308_WY_3GJ20/1/details/ "First Test Results"
[4]: http://www.webpagetest.org/result/120308_PT_3GJ1W/1/details/ "Second Test Results"
[5]: http://www.webpagetest.org/result/120308_QB_3GJ3F/1/details/ "Third Test Results"
[6]: https://developers.google.com/closure/compiler/ "Google Closure Compiler"