---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.2.3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

In this notebook we plot the world population and the gross domestic product per country

```python tags=["parameters"]
year = 2000
```

```python
import plotly.offline as offline
from plots import sundial_plot

offline.init_notebook_mode()
```

## World Population

```python
sundial_plot('SP.POP.TOTL', 'World Population', year)
```

## Gross Domestic Product (current USD)

```python
sundial_plot('NY.GDP.MKTP.CD', 'Gross Domestic Product', year)
```
