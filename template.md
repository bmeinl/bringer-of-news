**Weekly video dump for the week of {{ datestring }}**

Hello, everyone. This is an intro text I should probably change!  


{% for c in channels %}
*****
**[{{ c.title }}](http://youtube.com/user/{{ c.title }})**
{% if c.comment is defined %} - {{ c.comment }} {% endif %}

{% for l in c.links %}
>*****
>{{ loop.index }}. {{ l }}

{% endfor %}

>*****

{% if not loop.last %} ^^. {% endif %}
{% endfor %}

