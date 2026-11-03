---
layout: page
title: Awards
permalink: /awards/
description: Awards, Honors and Grants.
nav: true
nav_order: 4.5
---

{% if site.data.awards %}

<div class="table-responsive">
  <table class="table table-sm table-borderless">
    {% assign awards = site.data.awards | sort: 'date' | reverse %}
    {% for item in awards %}
      <tr>
        <th scope="row" style="width: 15%">{{ item.date | date: '%Y' }}</th>
        <td>
          {% if item.url %}
            <a href="{{ item.url }}" target="_blank" rel="noopener noreferrer"><strong>{{ item.title }}</strong></a>
          {% else %}
            <strong>{{ item.title }}</strong>
          {% endif %}
          {% if item.organization or item.note %}
            <br>
            <small class="text-muted">
              {%- if item.organization -%}{{ item.organization }}{%- endif -%}
              {%- if item.organization and item.note %} &middot; {% endif -%}
              {%- if item.note -%}{{ item.note | markdownify | remove: '<p>' | remove: '</p>' | strip }}{%- endif -%}
            </small>
          {% endif %}
        </td>
      </tr>
    {% endfor %}
  </table>
</div>
{% endif %}
