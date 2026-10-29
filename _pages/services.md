---
layout: page
title: Services
permalink: /services/
description: Professional service to the research community.
nav: true
nav_order: 4
---

{% for category in site.data.services %}
{% if category.entries.size > 0 %}

<h2 class="category">{{ category.title }}</h2>
<div class="table-responsive">
  <table class="table table-sm table-borderless">
    {% assign entries = category.entries | sort: 'year' | reverse %}
    {% for item in entries %}
      <tr>
        <th scope="row" style="width: 20%">
          {% if item.url %}<a href="{{ item.url }}">{{ item.venue }}</a>{% else %}{{ item.venue }}{% endif %}
        </th>
        <td>
          {{ item.role }}<br>
          <span class="text-muted">{{ item.name }}</span>
        </td>
      </tr>
    {% endfor %}
  </table>
</div>
{% endif %}
{% endfor %}
