# DjangoMetrics

This project is an open source demo of a middleware service in the Django web framework. It utilizes the open source Django project [bootcamp][0] as its base.

The [middleware][1] has three basic features:

* Detect how many string objects are created per page request \*
* Time each page request from start to finish
* Provide a brief overview of memory utilization per page request

\* string count is currently disabled for signup and login tasks

Page request logs can be found in the root directory's requests.log file and metrics can be found in the root directory's metrics.log file. In order to turn on DjangoMetrics simply run "python manage.py metrics" instead of the usual "python manage.py runserver".


## Installation Guide

[Detailed installation guide][2].


[0]: https://www.github.com/vitorfs/bootcamp.git
[1]: https://github.com/JWeesner/DjangoMetrics/blob/master/bootcamp/middleware.py
[2]: https://github.com/JWeesner/DjangoMetrics/wiki/Bootcamp-install
