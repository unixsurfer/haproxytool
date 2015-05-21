.. haproxytool
.. README.rst

haproxytool
===========

    *A tool to manage HAProxy via stats socket.*

It uses `haproxyadmin <https://github.com/unixsurfer/haproxyadmin>`_
Python library to interact with HAProxy and run all commands.
One of the main feature is that can work with HAProxy in multi-process mode (nbproc > 1)

.. contents::

Examples
--------

Usage
~~~~~

The command line interface tries to be friendly and compatible with the rest of
the tools available in the Linux land. The `docopt Python module
<https://pypi.python.org/pypi/docopt>`_ is used to build the CLI interface.

Here is the basic syntax to start with::

    % haproxytool
    Usage: haproxytool [-v | -h | --socket-dir DIR] <command> [<args>...]

    % haproxytool -h
    A tool to manage HAProxy via the stats socket.

    Usage: haproxytool [-v | -h | --socket-dir DIR] <command> [<args>...]

    Options:
    -h, --help                show this screen.
    -v, --version             show version.
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files [default: /var/lib/haproxy]

    Arguments:
        DIR  a directory path

    Avalable haproxytool commands are:
        frontend  Frontend operations
        pool      Pool operations
        server    Server operations
        dump      Dumps all informations

    See 'haproxytool help <command>' for more information on a specific command.

Keep reading for more details about each command.

Commands for frontends
~~~~~~~~~~~~~~~~~~~~~~

* Usage

::

    % haproxytool frontend --help
    Manage frontends

    Usage:
        haproxytool frontend [-D DIR | -h] (-r | -s | -o | -e | -d | -t | -p) [NAME...]
        haproxytool frontend [-D DIR | -h] -w OPTION VALUE [NAME...]
        haproxytool frontend [-D DIR | -h] (-l | -M)
        haproxytool frontend [-D DIR | -h] -m METRIC [NAME...]

    Arguments:
        DIR     Directory path
        VALUE   Value to set
        OPTION  Setting name
        METRIC  Name of a metric, use '-M' to get metric names

    Options:
        -h, --help                show this screen
        -e, --enable              enable frontend
        -d, --disable             disable frontend
        -t, --shutdown            shutdown frontend
        -r, --requests            show requests
        -p, --process             show process number
        -s, --status              show status
        -o, --options             show value of options that can be changed with '-w'
        -m, --metric              show value of a metric
        -M, --list-metrics        show all metrics
        -l, --list                show all frontends
        -w, --write               change a frontend option
        -D DIR, --socket-dir=DIR  directory with HAProxy socket files
        [default: /var/lib/haproxy]

* Show status of frontend(s)

::

    % haproxytool -D /run/haproxy frontend -s
    frontend_proc1 OPEN
    frontend2_proc34 OPEN
    haproxy OPEN
    frontend1_proc34 OPEN
    frontend_proc2 OPEN

    % haproxytool -D /run/haproxy frontend -s frontend2_proc34
    frontend2_proc34 OPEN

* Show requests

::

    % haproxytool -D /run/haproxy frontend -r frontend2_proc34
    frontend2_proc34 10

* Show in which HAProxy process a frontend is used

::

    % haproxytool -D /run/haproxy frontend -p frontend2_proc34
    frontend2_proc34 [4, 3]

* Show option(s) that can be changed

:NOTE: Currently, HAProxy allows only to change the maximum connections option for the frontends.

::

    % haproxytool -D /run/haproxy frontend -o frontend_proc1
    frontend_proc1 maxconn=1000000

* Change an option

::

    % haproxytool -D /run/haproxy frontend -w maxconn 100000 frontend_proc1
    frontend_proc1 set maxconn to 100000

    % haproxytool -D /run/haproxy frontend -o frontend_proc1
    frontend_proc1 maxconn=100000

* Changing an option for a frontend assigned to multiple HAProxy process

::

    % haproxytool -D /run/haproxy frontend -o frontend1_proc34
    frontend1_proc34 maxconn=2000000

    % haproxytool -D /run/haproxy frontend -w maxconn 40000 frontend1_proc34
    frontend1_proc34 set maxconn to 40000

    % haproxytool -D /run/haproxy frontend -o frontend1_proc34
    frontend1_proc34 maxconn=80000

    % haproxytool -D /run/haproxy frontend -p frontend1_proc34
    frontend1_proc34 [4, 3]

:NOTE: It is not supported to change a option only to one of the HAProxy
    process

:NOTE: The return value of the option is the sum of the values across all
    HAProxy processes

Commands for pools
~~~~~~~~~~~~~~~~~~

* Usage

::

    % haproxytool pool --help
    Manage pools

    Usage:
        haproxytool pool [-D DIR | -h] (-S | -r | -p | -s) [NAME...]
        haproxytool pool [-D DIR | -h] (-l | -M)
        haproxytool pool [-D DIR | -h] -m METRIC [NAME...]

    Arguments:
        DIR     Directory path
        METRIC   Name of a metric, use '-M' to get metric names

    Options:
        -h, --help                show this screen
        -S, --servers             show members
        -r, --requests            show requests
        -p, --process             show process number
        -s, --status              show status
        -m, --metric              show value of a metric
        -M, --list-metrics        show all metrics
        -l, --list                show all pools
        -D DIR, --socket-dir=DIR  directory with HAProxy socket files
        [default: /var/lib/haproxy]

Commands for servers
~~~~~~~~~~~~~~~~~~~~

* Usage

::

    % haproxytool server --help
    Manage servers

    Usage:
        haproxytool server [-D DIR | -h] (-r | -s | -e | -d | -R | -n | -t | -p | -W) [--pool=<name>...] [NAME...]
        haproxytool server [-D DIR | -h] -w VALUE [--pool=<name>...] [NAME...]
        haproxytool server [-D DIR | -h] (-l | -M)
        haproxytool server [-D DIR | -h] -m METRIC [--pool=<name>...] [NAME...]


    Arguments:
        DIR     Directory path
        VALUE   Value to set
        METRIC  Name of a metric, use '-M' to get metric names

    Options:
        -h, --help                show this screen
        -e, --enable              enable server
        -d, --disable             disable server
        -R, --ready               set server in normal mode
        -n, --drain               drain server
        -t, --maintenance         set server in maintenance mode
        -r, --requests            show requests
        -p, --process             show process number
        -s, --status              show status
        -m, --metric              show value of a metric
        -M, --list-metrics        show all metrics
        -l, --list                show all servers
        -w, --weight              change weight for server
        -W, --get-weight          show weight of server
        -D DIR, --socket-dir=DIR  directory with HAProxy socket files
        [default: /var/lib/haproxy]

* List all servers

::

    % haproxytool -D /run/haproxy server -l
    # poolname servername
    backend1_proc34                bck1_proc34_srv1
    backend1_proc34                bck1_proc34_srv2
    backend1_proc34                bck_all_srv1
    backend_proc2                  bck_proc2_srv4_proc2
    backend_proc2                  bck_proc2_srv3_proc2
    backend_proc2                  bck_proc2_srv2_proc2
    backend_proc2                  bck_proc2_srv1_proc2
    backend_proc1                  member1_proc1
    backend_proc1                  member2_proc1
    backend_proc1                  bck_all_srv1
    backend2_proc34                bck2_proc34_srv1
    backend2_proc34                bck_all_srv1
    backend2_proc34                bck2_proc34_srv2

* Show status of servers per pool

::

    % haproxytool -D /run/haproxy server -s --pool=backend_proc1
    # poolname servername
    backend_proc1                  bck_all_srv1                               DOWN
    backend_proc1                  member1_proc1                              no check
    backend_proc1                  member2_proc1                              no check


    % haproxytool -D /run/haproxy server -s --pool=backend_proc1 --pool=backend2_proc34
    # poolname servername
    backend_proc1                  member1_proc1                              no check
    backend_proc1                  bck_all_srv1                               DOWN
    backend_proc1                  member2_proc1                              no check
    backend2_proc34                bck2_proc34_srv2                           UP
    backend2_proc34                bck2_proc34_srv1                           no check
    backend2_proc34                bck_all_srv1                               no check

* Show weight of servers across all pools and per pool

::

    % haproxytool -D /run/haproxy server -W bck_all_srv1
    # poolname servername
    backend1_proc34                bck_all_srv1                               1.0
    backend2_proc34                bck_all_srv1                               1.0
    backend_proc1                  bck_all_srv1                               100.0
    pparissis at axilleas in ~/bin

    % haproxytool -D /run/haproxy server -W bck_all_srv1 --pool=backend_proc1 --pool=backend2_proc34
    # poolname servername
    backend_proc1                  bck_all_srv1                               100.0
    backend2_proc34                bck_all_srv1                               1.0
    pparissis at axilleas in ~/bin

* Set weight on servers across all pools and per pool

::

    % haproxytool -D /run/haproxy server -w 10 bck_all_srv1
    bck_all_srv1 pool set weight to 10 in backend2_proc34 pool
    bck_all_srv1 pool set weight to 10 in backend1_proc34 pool
    bck_all_srv1 pool set weight to 10 in backend_proc1 pool

    % haproxytool -D /run/haproxy server -w 50 bck_all_srv1 --pool=backend_proc1 --pool=backend2_proc34
    bck_all_srv1 pool set weight to 50 in backend_proc1 pool
    bck_all_srv1 pool set weight to 50 in backend2_proc34 pool
    pparissis at axilleas in ~/bin

* Show requests

::

    % haproxytool -D /run/haproxy server -r bck_all_srv1
    # poolname servername
    backend_proc1                  bck_all_srv1                               0
    backend2_proc34                bck_all_srv1                               2
    backend1_proc34                bck_all_srv1                               10

* List metric names available from the statistics

::

    % haproxytool -D /run/haproxy server -M
    qcur
    qmax
    scur
    smax
    stot
    bin
    bout
    dresp
    econ
    eresp
    wretr
    wredis
    weight
    act
    bck
    chkfail
    chkdown
    lastchg
    downtime
    qlimit
    throttle
    lbtot
    rate
    rate_max
    check_duration
    hrsp_1xx
    hrsp_2xx
    hrsp_3xx
    hrsp_4xx
    hrsp_5xx
    hrsp_other
    cli_abrt
    srv_abrt
    lastsess
    qtime
    ctime
    rtime
    ttime

Please consult `CSV format of HAProxy <http://cbonte.github.io/haproxy-dconv/configuration-1.5.html#9.1>`_ for their
description.

* Show the value of a specific metric

::


    % haproxytool -D /run/haproxy server -m bin bck_all_srv1
    # poolname servername
    backend1_proc34                bck_all_srv1                               760
    backend2_proc34                bck_all_srv1                               152
    backend_proc1                  bck_all_srv1                               0

* Show in which HAProxy process a server is used

::

    % haproxytool -D /run/haproxy server -p bck_all_srv1
    # poolname servername
    backend2_proc34                bck_all_srv1                               [4, 3]
    backend_proc1                  bck_all_srv1                               [1]
    backend1_proc34                bck_all_srv1                               [4, 3]

* Enable/disable a server

::

    % haproxytool -D /run/haproxy server -d bck_all_srv1
    bck_all_srv1 disabled in backend1_proc34 pool
    bck_all_srv1 disabled in backend_proc1 pool
    bck_all_srv1 disabled in backend2_proc34 pool

    % haproxytool -D /run/haproxy server -s bck_all_srv1
    # poolname servername
    backend_proc1                  bck_all_srv1                               MAINT
    backend2_proc34                bck_all_srv1                               MAINT
    backend1_proc34                bck_all_srv1                               MAINT

    % haproxytool -D /run/haproxy server -e bck_all_srv1
    bck_all_srv1 enabled in backend2_proc34 pool
    bck_all_srv1 enabled in backend1_proc34 pool
    bck_all_srv1 enabled in backend_proc1 pool

    % haproxytool -D /run/haproxy server -s bck_all_srv1
    # poolname servername
    backend1_proc34                bck_all_srv1                               UP
    backend2_proc34                bck_all_srv1                               no check
    backend_proc1                  bck_all_srv1                               DOWN

Dump command
~~~~~~~~~~~~~~~~~~

* Usage

::

    % haproxytool dump --help
    Dump a collection of information about frontends, pools and servers

    Usage:
        haproxytool dump [-fpsh -D DIR ]

    Options:
        -h, --help                show this screen
        -f, --frontends           show frontends
        -p, --pools               show pool
        -s, --servers             show server
        -D DIR, --socket-dir=DIR  directory with HAProxy socket files
        [default: /var/lib/haproxy]

Release
-------

To make a release you should first create a signed tag, pbr will use this for the version number::

   git tag -s 0.0.9 -m 'bump release'
   git push --tags

Create the source distribution archive (the archive will be placed in the **dist** directory)::

   python setup.py sdist

Installation
------------

From Source::

   sudo python setup.py install

Build (source) RPMs::

   python setup.py clean --all; python setup.py bdist_rpm

Booking.com instructions::

   python setup.py clean --all
   python setup.py sdist

Build a source archive for manual installation::

   python setup.py sdist

Licensing
---------

Apache 2.0

Acknowledgement
---------------
This program was originally developed for Booking.com.  With approval
from Booking.com, the code was generalised and published as Open Source
on github, for which the author would like to express his gratitude.

Contacts
--------

**Project website**: https://github.com/unixsurfer/haproxytool

**Author**: Palvos Parissis <pavlos.parissis@gmail.com>
