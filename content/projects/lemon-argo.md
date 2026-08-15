+++
title = "ArgoCD Manifests"
description = "Manifest deployed to my home lab (lemon) kubernetes cluster"
weight = 1
template = "page.html"

[taxonomies]
tags = ["kubernetes", "rust"]

#[extra]
#remote_image = "https://raw.githubusercontent.com/argoproj/argo-cd/refs/heads/master/docs/assets/argo.png"
+++

This is where I maintain all of the kubernetes manifests thatI deploy into my
local kubernetes cluster. This uses leverages ArgoCD `ApplicationSet`s and a
custom config shape to fully manage the deployed applications via Git, only the
intiial bootstrap `AppProject` and `Application` need to be hand applied.

#### [View Source](https://github.com/narthollis-lemon/argo){.centered-text}
