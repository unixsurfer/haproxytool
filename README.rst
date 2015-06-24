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

    Available haproxytool commands are:
        frontend  Frontend operations
        backend   Backend operations
        server    Server operations
        dump      Dumps all informations
        map       Manage MAPs

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

Commands for backends
~~~~~~~~~~~~~~~~~~

* Usage

::

    % haproxytool backend --help
    Manage backends

    Usage:
        haproxytool backend [-D DIR | -h] (-S | -r | -p | -s) [NAME...]
        haproxytool backend [-D DIR | -h] (-l | -M)
        haproxytool backend [-D DIR | -h] -m METRIC [NAME...]

    Arguments:
        DIR     Directory path
        METRIC   Name of a metric, use '-M' to get metric names

    Options:
        -h, --help                show this screen
        -S, --servers             show servers
        -r, --requests            show requests
        -p, --process             show process number
        -s, --status              show status
        -m, --metric              show value of a metric
        -M, --list-metrics        show all metrics
        -l, --list                show all backends
        -D DIR, --socket-dir=DIR  directory with HAProxy socket files
        [default: /var/lib/haproxy]

Commands for servers
~~~~~~~~~~~~~~~~~~~~

* Usage

::

    % haproxytool server --help
    Manage servers

    Usage:
        haproxytool server [-D DIR | -h] (-r | -s | -e | -d | -R | -n | -t | -p | -W) [--backend=<name>...] [NAME...]
        haproxytool server [-D DIR | -h] -w VALUE [--backend=<name>...] [NAME...]
        haproxytool server [-D DIR | -h] (-l | -M)
        haproxytool server [-D DIR | -h] -m METRIC [--backend=<name>...] [NAME...]


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
    # backendname servername
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

* Show status of servers per backend

::

    % haproxytool -D /run/haproxy server -s --backend=backend_proc1
    # backendname servername
    backend_proc1                  bck_all_srv1                               DOWN
    backend_proc1                  member1_proc1                              no check
    backend_proc1                  member2_proc1                              no check


    % haproxytool -D /run/haproxy server -s --backend=backend_proc1 --backend=backend2_proc34
    # backendname servername
    backend_proc1                  member1_proc1                              no check
    backend_proc1                  bck_all_srv1                               DOWN
    backend_proc1                  member2_proc1                              no check
    backend2_proc34                bck2_proc34_srv2                           UP
    backend2_proc34                bck2_proc34_srv1                           no check
    backend2_proc34                bck_all_srv1                               no check

* Show weight of servers across all backends and per backend

::

    % haproxytool -D /run/haproxy server -W bck_all_srv1
    # backendname servername
    backend1_proc34                bck_all_srv1                               1
    backend2_proc34                bck_all_srv1                               1
    backend_proc1                  bck_all_srv1                               100
    pparissis at axilleas in ~/bin

    % haproxytool -D /run/haproxy server -W bck_all_srv1 --backend=backend_proc1 --backend=backend2_proc34
    # backendname servername
    backend_proc1                  bck_all_srv1                               100
    backend2_proc34                bck_all_srv1                               1
    pparissis at axilleas in ~/bin

* Set weight on servers across all backends and per backend

::

    % haproxytool -D /run/haproxy server -w 10 bck_all_srv1
    bck_all_srv1 backend set weight to 10 in backend2_proc34 backend
    bck_all_srv1 backend set weight to 10 in backend1_proc34 backend
    bck_all_srv1 backend set weight to 10 in backend_proc1 backend

    % haproxytool -D /run/haproxy server -w 50 bck_all_srv1 --backend=backend_proc1 --backend=backend2_proc34
    bck_all_srv1 backend set weight to 50 in backend_proc1 backend
    bck_all_srv1 backend set weight to 50 in backend2_proc34 backend
    pparissis at axilleas in ~/bin

* Show requests

::

    % haproxytool -D /run/haproxy server -r bck_all_srv1
    # backendname servername
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
    # backendname servername
    backend1_proc34                bck_all_srv1                               760
    backend2_proc34                bck_all_srv1                               152
    backend_proc1                  bck_all_srv1                               0

* Show in which HAProxy process a server is used

::

    % haproxytool -D /run/haproxy server -p bck_all_srv1
    # backendname servername
    backend2_proc34                bck_all_srv1                               [4, 3]
    backend_proc1                  bck_all_srv1                               [1]
    backend1_proc34                bck_all_srv1                               [4, 3]

* Enable/disable a server

::

    % haproxytool -D /run/haproxy server -d bck_all_srv1
    bck_all_srv1 disabled in backend1_proc34 backend
    bck_all_srv1 disabled in backend_proc1 backend
    bck_all_srv1 disabled in backend2_proc34 backend

    % haproxytool -D /run/haproxy server -s bck_all_srv1
    # backendname servername
    backend_proc1                  bck_all_srv1                               MAINT
    backend2_proc34                bck_all_srv1                               MAINT
    backend1_proc34                bck_all_srv1                               MAINT

    % haproxytool -D /run/haproxy server -e bck_all_srv1
    bck_all_srv1 enabled in backend2_proc34 backend
    bck_all_srv1 enabled in backend1_proc34 backend
    bck_all_srv1 enabled in backend_proc1 backend

    % haproxytool -D /run/haproxy server -s bck_all_srv1
    # backendname servername
    backend1_proc34                bck_all_srv1                               UP
    backend2_proc34                bck_all_srv1                               no check
    backend_proc1                  bck_all_srv1                               DOWN

Dump command
~~~~~~~~~~~~

* Usage

::

    % haproxytool dump --help
    Dump a collection of information about frontends, backends and servers

    Usage:
        haproxytool dump [-fpsh -D DIR ]

    Options:
        -h, --help                show this screen
        -f, --frontends           show frontends
        -b, --backends            show backend
        -s, --servers             show server
        -D DIR, --socket-dir=DIR  directory with HAProxy socket files
        [default: /var/lib/haproxy]

Map command
~~~~~~~~~~~~

* Usage

::

    % haproxytool dump --help
    Manage MAPs

    Usage:
        haproxytool map [-D DIR | -h] -l
        haproxytool map [-D DIR | -h] (-s | -c ) MAPID
        haproxytool map [-D DIR | -h] -g MAPID KEY
        haproxytool map [-D DIR | -h] (-S | -A) MAPID KEY VALUE
        haproxytool map [-D DIR | -h] -d MAPID KEY


    Arguments:
        DIR     Directory path
        MAPID   ID of the map or file returned by show map
        KEY     ID of key
        VALUE   Value to set

    Options:
        -h, --help                show this screen
        -A, --add                 add a <KEY> entry into the map <MAPID>
        -s, --show                show map
        -g, --get                 lookup the value of a key in the map
        -c, --clear               clear all entries for a map
        -l, --list                list all map ids
        -S, --set                 set a new value for a key in a map
        -d, --delete              delete all the map entries from the map <MAPID>
                                  corresponding to the key <KEY>
        -D DIR, --socket-dir=DIR  directory with HAProxy socket files
        [default: /var/lib/haproxy]

* List all MAPIDs

::

    % haproxytool -D /run/haproxy map -l
    # id (file) description
    4 (/etc/haproxy/v-m1-bk) pattern loaded from file '/etc/haproxy/v-m1-bk'
    used by map at file '/etc/haproxy/haproxy.cfg' line 87

* Show the content of a map

::

    % haproxytool -D /run/haproxy map -s 4
    0xb743f0 0 www.foo.com-0
    0xb74460 1 www.foo.com-1

* Add a key to a map

::

    % haproxytool -D /run/haproxy map -A 4 3 www.goo.com
    key was added successfully

    % haproxytool -D /run/haproxy map -s 4
    0xb743f0 0 www.foo.com-0
    0xb74460 1 www.foo.com-1
    0x28f0f50 3 www.goo.com

* Delete an entry from a map

::

    % haproxytool -D /run/haproxy map -d 4 3
    key was deleted successfully

    % haproxytool -D /run/haproxy map -s 4
    0xb743f0 0 www.foo.com-0
    0xb74460 1 www.foo.com-1

* Set a value for a key in a map

::

    % haproxytool -D /run/haproxy map -S 4 1 bar.com
    value was set successfully

    % haproxytool -D /run/haproxy map -s 4
    0xb743f0 0 www.foo.com-0
    0xb74460 1 bar.com

* Clear all entries of a map

::

    % haproxytool -D /run/haproxy map -c 4
    all entries of map were cleared successfully

    % haproxytool -D /run/haproxy map -s 4

    %

:NOTE: Currently, HAProxy doesn't allow to create new MAPs via the stats socket.

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
