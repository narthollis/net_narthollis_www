+++
title = "Resurected, Again!"
template = "page.html"
date = 2026-08-15T17:18:00+09:30
[taxonomies]
tags = ["blog","tech"]
+++

Once again, I have spent the effort to resurect this website and blog.

<!-- more -->

And to mirror the last time I [revived](./2021-08-17-revived.md) this site, it again has some changes in tech.

Less drastic this time, the site is still built using [Zola](https://getzola.org/),
but rather than the previous in-cluster build process, I am now building the site
using [Github Actions](https://github.com/narthollis/net_narthollis_www/blob/main/.github/workflows/docker-publish.yml).
I then use renovate to open a pull-request on the repository holding my [ArgoCD Manifests](../projects/lemon-argo.md) -
 which will then replicate the changes into my live kubernetes cluster.

 Also rather than using Nginx I am now using (Static Web Server)[https://static-web-server.net/]
 as this offered and easier cleaner containerisation process.

And, yea as per normal I expect this to be the last post again for a while. Although I do hope to
populate the new [Projects](../projects/) section of the site and keep this at least somewhat
current.
