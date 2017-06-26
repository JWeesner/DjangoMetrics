# DjangoMetrics

This project is an open source demo of a middleware service in the Django web framework. It utilizes the open source Django project bootcamp[0] as it's base.

The middleware[1] has three basic features:

* Detect how many string objects are created per page request \*
* Time each page request from start to finish
* Provide a brief overview of memory utilization per page request

\* string count is currently disabled for signup and login tasks


## Installation Guide

[Detailed installation guide][2].


[0]: https://www.github.com/vitorfs/bootcamp.git
[1]: https://github.com/JWeesner/DjangoMetrics/blob/master/bootcamp/middleware.py
[2]: https://github.com/JWeesner/DjangoMetrics/wiki/Bootcamp-install
