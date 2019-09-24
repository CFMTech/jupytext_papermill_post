# Automated Reports with Jupyter Notebooks (using Jupytext and Papermill)

[![Build Status](https://travis-ci.org/CFMTech/jupytext_papermill_post.svg?branch=master)](https://travis-ci.org/CFMTech/jupytext_papermill_post)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CFMTech/jupytext_papermill_post/master)
[![Jupytext](https://img.shields.io/badge/jupytext-1.2.4-blue.svg)](https://github.com/mwouts/jupytext)
[![Papermill](https://img.shields.io/badge/papermill-1.2.0-blue.svg)](https://github.com/nteract/papermill)
[![CFM insights](https://img.shields.io/badge/medium-CFM%20insights-00ab6c.svg)](https://medium.com/capital-fund-management)

Jupyter notebooks are one of the best available tools for running code interactively and writing a narrative with data and plots. What is less known is that they can be conveniently versioned and run automatically.

Do you have a Jupyter notebook with plots and figures that you regularly run manually? Wouldn't it be nice to use the same notebook and instead have an automated reporting system, launched from a script? What if this script could even pass some parameters to the notebook it runs?

This post explains in a few steps how this can be done concretely, including within a production environment.

![](https://github.com/CFMTech/jupytext_papermill_post/raw/master/screenshots/Hoe%27s_six-cylinder_press.png)

## Example notebook

We will show you how to version control, automatically run and publish a notebook that depends on a parameter. As an example, we will use a [notebook](https://nbviewer.jupyter.org/github/CFMTech/jupytext_papermill_post/blob/master/outputs/world_facts_2017.ipynb) that describes the world population and the gross domestic product for a given year. It is simple to use: just change the `year` variable in the first cell, re-run, and you get the plots for the chosen year. But this requires a manual intervention. It would be much more convenient if the update could be automated and produce a report for each possible value of the `year` parameter (more generally, a notebook can update its results based not only on some user-provided parameters, but also through a connection to a database, etc.).

![](https://github.com/CFMTech/jupytext_papermill_post/raw/master/screenshots/notebook_overview.png)


---


## Version control

In a professional environment, notebooks are designed by, say, a data scientist, but the task of running them in production may be handled by a different team. So in general people have to share notebooks. This is best done through a version control system.

Jupyter notebooks are famous for the difficulty of their version control. Let's consider our notebook above, with a file size of 3 MB, much of it being contributed by the embedded [Plotly](https://plot.ly/python) library. The notebook is less than 80 KB if we remove the output of the second code cell. And as small as 1.75 KB when all outputs are removed. This shows how much of its contents is unrelated to pure code! If we don't pay attention, code changes in the notebook will be lost in an ocean of binary contents.


To get meaningful diffs, we use [Jupytext](https://github.com/mwouts/jupytext/) (disclaimer: I am the author of Jupytext). Jupytext [can be installed](https://github.com/mwouts/jupytext/blob/master/README.md#installation) with `pip` or `conda`. Once the notebook server is restarted, a Jupytext menu appears in Jupyter:

![](https://github.com/CFMTech/jupytext_papermill_post/raw/master/screenshots/jupytext_menu.png)

We click on _Pair Notebook with Markdown_, save the notebook... and we obtain two representations of the notebook: `world_fact.ipynb` (with both input and output cells) and `world_fact.md` (with only the input cells).


Jupytext's representation of notebooks as Markdown files is compatible with all major Markdown editors and viewers, including GitHub and VS Code. The Markdown version is for example rendered by GitHub as:

![](https://github.com/CFMTech/jupytext_papermill_post/raw/master/screenshots/markdown_nb_on_github.png)

As you can see, the Markdown file does not include any output. Indeed, we don't want it at this stage since we only need to share the notebook code. The Markdown file also has a very clear diff history, which makes versioning notebooks simple.


The `world_facts.md` file is automatically updated by Jupyter when you save the notebook. And the other way round also works! If you modify `world_facts.md` with either a text editor, or by pulling the latest contributions from the version control system, then the changes appear in Jupyter when you refresh the notebook in the browser.

In our version control system, we only need to track the Markdown file (and we even explicitly ignore all `.ipynb` files). Obviously, the team that will execute the notebook needs to regenerate the `world_fact.ipynb` document. For this they use Jupytext in the command line:

```bash
jupytext world_facts.md --to ipynb
```

    [jupytext] Reading world_facts.md
    [jupytext] Writing world_facts.ipynb


We are now properly versioning the notebook. The diff history is much clearer. See for instance how the [addition](https://github.com/CFMTech/jupytext_papermill_post/commit/ed138e1eddf951229d349e9cc1a435b40ac3d3d6) of the gross domestic products to our report looks like:

![](https://github.com/CFMTech/jupytext_papermill_post/raw/master/screenshots/notebook_diff.png)



### Jupyter notebooks as Scripts?

As an alternative to the Markdown representation, we could have paired the notebook to a `world_facts.py` script using Jupytext. You should give it a try if your notebook contains more code than text. That's often a first good step towards a complete and efficient refactoring of long notebooks: once the notebook is represented as a script, you can extract any complex code and move it to a (unit-tested) library using the refactoring tools in your IDE.


### JupyterLab, JupyterHub, Binder, Nteract, Colab & Cloud notebooks?

Do you use JupyterLab and not Jupyter Notebook? No worries: the method above also applies in this case. You will just have to use the [Jupytext extension for JupyterLab](https://github.com/mwouts/jupytext/blob/master/README.md#jupytext-commands-in-jupyterlab) instead of the Jupytext menu. And in case you were wondering, Jupytext also work in [JupyterHub](https://jupyter.org/hub) and [Binder](http://mybinder.org/).

If you use other notebook editors like [Nteract desktop](https://nteract.io/desktop), [CoCalc](https://cocalc.com/), [Google Colab](https://colab.research.google.com/notebooks/welcome.ipynb), or another cloud notebook editor, you may not be able to use Jupytext as a plugin in the editor. In this case you can simply use Jupytext in the command line. Close your notebook and inject the pairing information into `world_facts.ipynb` with

    jupytext --set-formats ipynb,md world_facts.ipynb

and then keep the two representations synchronized with

    jupytext --sync world_facts.ipynb


---


## Notebook parameters

[Papermill](https://github.com/nteract/papermill/) is the reference library for executing notebooks with parameters. 

Papermill needs to know which cell contains the notebook parameters. This is simply done by adding a `parameter` tag in that cell with the cell toolbar in Jupyter Notebook:

![](https://github.com/CFMTech/jupytext_papermill_post/raw/master/screenshots/cell_tag_notebook.png)

In JupyterLab you can use the [celltags](https://github.com/jupyterlab/jupyterlab-celltags) extension.

And if you prefer you can also directly edit `world_facts.md` and add the tag there:

    ```python tags=["parameters"]
    year = 2000
    ```


---

## Automated execution

We now have all the information required to execute the notebook on a production server. 

### Production environment

In order to execute the notebook, we need to know in which environment it should run. As we are working with a Python notebook in this example, we list its dependencies in a [`requirements.txt`](https://github.com/CFMTech/jupytext_papermill_post/blob/master/requirements.txt) file, as is standard for Python projects.

For simplicity, we also include the notebook tools in the same environment, i.e. add `jupytext` and `papermill` to the same `requirements.txt` file. Strictly speaking, these tools could be installed and executed in another Python environment.

The corresponding Python environment is created with either 

    conda create -n run_notebook --file requirements.txt -y

or 

    pip install -r requirements.txt

(if in a virtual environment). 

Please note that the `requirements.txt` file is just one way of specifying an execution environment. The [Reproducible Execution Environment Specification](https://repo2docker.readthedocs.io/en/latest/specification.html#the-reproducible-execution-environment-specification) by the Binder team is one of the most complete references on the subject.

### Continuous Integration

It is a good practice to test each new contribution to either the notebook or its requirements. For this you can use for example [Travis CI](http://travis-ci.com/), a continuous integration solution. You will need only these two commands:
- `pip install -r requirements.txt` to install the dependencies
- `jupytext world_facts.md --set-kernel - --execute` to test the execution of the notebook in the current Python environment.

You can find a concrete example in our [`.travis.yml`](https://github.com/CFMTech/jupytext_papermill_post/blob/master/.travis.yml) file.

We are already executing the notebook automatically, aren't we? Travis will tell us if a regression is introduced in the project... What progress! But we're not 100% done yet, as we promised to execute the notebook with parameters.

### Using the right kernel

Jupyter notebooks are associated with a _kernel_ (i.e. a pointer to a local Python environment), but that kernel might not be available on your production machine. In this case, we simply update the notebook kernel so as to point to the environment that we have just created:

```bash
jupytext world_facts.ipynb --set-kernel -
```

Note that the minus sign in `--set-kernel -` above represents the _current_ Python environment. In our example this yields:


    [jupytext] Reading world_facts.ipynb
    [jupytext] Updating notebook metadata with '{"kernelspec": {"name": "python3", "language": "python", "display_name": "Python 3"}}'
    [jupytext] Writing world_facts.ipynb (destination file replaced)


In case you want to use another kernel just pass the kernel name to the `--set-kernel` option (you can get the list of all available kernels with `jupyter kernelspec list` and/or declare a new kernel with `python -m ipykernel install --name kernel_name --user`).


### Executing the notebook with parameters

We are now ready to use [Papermill](https://github.com/nteract/papermill) for executing the notebook. 

```bash
papermill world_facts.ipynb world_facts_2017.ipynb -p year 2017
```

    Input Notebook:  world_facts.ipynb
    Output Notebook: world_facts_2017.ipynb
    100%|██████████████████████████████████████████████████████| 8/8 [00:04<00:00,  1.41it/s]

We're done! The notebook has been executed and the file `world_facts_2017.ipynb` contains the outputs. 


---


## Publishing the Notebook

It's time to deliver the notebook that was just executed. Maybe you want it in your mailbox? Or maybe you prefer to get a URL where you can see the result? We cover a few ways of doing that.

GitHub can display Jupyter notebooks. This is a convenient solution, as you can easily choose who can access repositories. This works well as long as you don't include any interactive JavaScript plots or widgets in the notebook (the JavaScript parts are ignored by GitHub). In the case of our notebook, the interactive plots [do not appear](https://github.com/CFMTech/jupytext_papermill_post/blob/master/outputs/world_facts_2017.ipynb) on GitHub, so we need another approach.

Another option is to use the Jupyter Notebook Viewer. The [nbviewer service](https://nbviewer.jupyter.org/) can render any notebook which is publicly available on GitHub. Our notebook is thus [rendered correctly](https://nbviewer.jupyter.org/github/CFMTech/jupytext_papermill_post/blob/master/outputs/world_facts_2017.ipynb) there. If your notebook is not public, you can choose to install [nbviewer](https://github.com/jupyter/nbviewer) locally. 

Alternatively, you can convert the executed notebook to HTML, and publish it on [GitHub pages](https://pages.github.com/), or on your own HTML server, or send it over email. Converting the notebook to HTML is easily done with

```bash
jupyter nbconvert world_facts_2017.ipynb --to html
```

    [NbConvertApp] Converting notebook world_facts_2017.ipynb to html
    [NbConvertApp] Writing 3361863 bytes to world_facts_2017.html

The resulting HTML file includes the code cells as below:

![](https://github.com/CFMTech/jupytext_papermill_post/raw/master/screenshots/html_with_input.png)

But maybe you don't want to see the input cells in the HTML? You just need to add `--no-input`:

```bash
jupyter nbconvert --to html --no-input world_facts_2017.ipynb --output world_facts_2017_report.html
```

And you'll get a cleaner report:

![](https://github.com/CFMTech/jupytext_papermill_post/raw/master/screenshots/html_no_input.png)

Sending the standalone HTML file as an attachment in an email is an easy exercise. Embedding the report in the body of the email is also possible (but interactive plots won't work).

Finally, if you are looking for a polished report and have some knowledge of LaTeX, you can give the PDF export option of Jupyter's nbconvert command a try.

---

## Using pipes

An alternative to using named files would be to use pipes. `jupytext`, `nbconvert` and `papermill` all support them. A one-liner substitute for the previous commands is:

```bash
cat world_facts.md \
| jupytext --from md --to ipynb --set-kernel - \
| papermill -p year 2017 \
| jupyter nbconvert --stdin --output world_facts_2017_report.html
```

---
## Conclusion

You should now be able to set up a full pipeline for generating reports in production, based on Jupyter notebooks. We have seen how to:
- version control a notebook with [Jupytext](https://github.com/mwouts/jupytext)
- share a notebook and its dependencies between various users
- test a notebook with continuous integration
- execute a notebook with parameters using [Papermill](https://github.com/nteract/papermill/)
- and finally, how to publish the notebook (on GitHub or nbviewer), or render it as a static HTML page.

The technology used in this example is fully based on the [Jupyter Project](https://jupyter.org/), which is the de facto standard for Data Science. The tools used here are all open source and work well with any continuous integration framework. 

You have everything you need to schedule and deliver fine-tuned, code-free reports! 


## Epilogue

The tools used here are written in Python. But they are _language agnostic_. Thanks to the Jupyter framework, they actually apply to any of the [40+ programming language for which a Jupyter kernel exists](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels).

Now, imagine that you have authored a document containing a few Bash command lines, just like this blog post. Install Jupytext and the [bash kernel](https://github.com/takluyver/bash_kernel), and the blog post becomes this [interactive Jupyter notebook](https://mybinder.org/v2/gh/CFMTech/jupytext_papermill_post/master?filepath=README.md)!

Going further, shouldn't we make sure that every instruction in our post actually works? We do that via our [continuous integration](https://github.com/CFMTech/jupytext_papermill_post/blob/master/.travis.yml)… spoiler alert: that's as simple as `jupytext --execute README.md`!

---


## Acknowledgments

Marc would like to thank [Eric Lebigot](https://github.com/lebigot) and [Florent Zara](https://github.com/flzara) for their contributions to this article, and to [CFM](https://www.cfm.fr) for supporting this work through their Open-Source Program.

## About the author

This article was written by [Marc Wouts](https://github.com/mwouts).

_Marc joined the research team of CFM in 2012 and has worked on a range of research projects, from optimal trading to portfolio construction._

_Marc has always been interested in finding efficient workflows for doing collaborative research involving data and code. In 2015 he authored an internal tool for publishing Jupyter and R Markdown notebooks on Atlassian's Confluence wiki, providing a first solution for collaborating on notebooks. In 2018, he authored [Jupytext](https://jupytext.readthedocs.io/en/latest/introduction.html), an open-source program that facilitates the version control of Jupyter notebooks. Marc is also interested in data visualization, and coordinates a working group on this subject at CFM._

_Marc obtained a PhD in Probability Theory from the Paris Diderot University in 2007._
