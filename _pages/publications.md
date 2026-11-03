---
layout: page
permalink: /publications/
title: Publications
description: publications by categories in reversed chronological order.
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

<div class="alert alert-secondary mt-3" role="alert">
  PDFs linked below are the author's version of each work, provided for personal, non-commercial use only and not for redistribution. Please refer to the DOI link for the version of record.
</div>

{% include bib_search.liquid %}

<div class="publications">

{% assign sections = 'conference:Conferences,workshop:Workshops,journal:Journal Articles,abstract:Talk Abstracts' | split: ',' %}
{% for section in sections %}
  {% assign pubtype = section | split: ':' | first %}
  {% assign heading = section | split: ':' | last %}
  {% capture count %}{% bibliography_count --query @*[pubtype={{ pubtype }}] %}{% endcapture %}
  {% assign count = count | strip | plus: 0 %}
  {% if count > 0 %}

<h1>{{ heading }}</h1>

{% bibliography --query @*[pubtype={{ pubtype }}] %}

{% endif %}
{% endfor %}

</div>
