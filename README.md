[![Build Status](https://travis-ci.org/CFMTech/jupytext_papermill_post.svg?branch=master)](https://travis-ci.org/CFMTech/jupytext_papermill_post)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CFMTech/jupytext_papermill_post/master?filepath=world_facts.md)

This repository contains Material for CFM's Jupytext+Papermill blog post (Sep. 2019).

Before the publication of the blog post, this is a work in progress.

# Bash commands

```bash
jupytext world_facts.md --to ipynb
```

```bash
jupytext world_facts.ipynb --set-kernel -
```


```bash
papermill world_facts.ipynb world_facts_2017.ipynb -p year 2017
```

```bash
jupyter nbconvert world_facts_2017.ipynb --to html
```

```bash
jupyter nbconvert --to html --no-input world_facts_2017.ipynb --output world_facts_2017_report.html
```

```bash
cat world_facts.md | jupytext --from md --to ipynb --set-kernel - | papermill -p year 2017 | jupyter nbconvert --stdin --output world_facts_2017_report.html
```
