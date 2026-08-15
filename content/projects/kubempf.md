+++
title = "kubempf"
description = "Tool for more persistant kubernetes port-forwawrding"
weight = 10
template = "page.html"

[taxonomies]
tags = ["kubernetes", "argocd", "lemon"]

#[extra]
#remote_image = "https://raw.githubusercontent.com/argoproj/argo-cd/refs/heads/master/docs/assets/argo.png"
+++

This is a tool I wrote initially because kubectl port-forward terminates when
it receives particular byte sequences that postgresql over tls sends requently.

The command syntax was also written to mirror SSH port-forwarding as this was something I felt more comfertable with when I wrote the tool.

#### [View Source](https://github.com/narthollis/kubempf){.centered-text}
