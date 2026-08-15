+++
title = "narth-network"
description = "A toy networking stack in rust"
weight = 100
template = "page.html"

[taxonomies]
tags = ["rust", "toy"]

+++

A toy networking stack built in rust mostly for fun and to get a better
understanding of writing larger projects in rust. I made efforts to build a
lock-free networking stack with seperation between the Network, Interface, and
Protocol layers. The objective is to have a public API that mirrors the rust
native socket APIs.

#### [View Source](https://github.com/narthollis/narth-network){.centered-text}
