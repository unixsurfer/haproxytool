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
    Usage: haproxytool [-v | -h] <command> [<args>...]

    % haproxytool -h
    A tool to manage HAProxy via the stats socket.

    Usage: haproxytool [-v | -h] <command> [<args>...]

    Options:
    -h, --help                show this screen.
    -v, --version             show version.

    Available haproxytool commands are:
        haproxy   HAProxy operations
        frontend  Frontend operations
        backend   Backend operations
        server    Server operations
        dump      Dumps all informations
        map       Manage MAPs
        acl       Manage ACLs

    See 'haproxytool help <command>' for more information on a specific command.

Keep reading for more details about each command.

Commands for HAProxy
~~~~~~~~~~~~~~~~~~~~~~

* Usage

::

    % haproxytool haproxy --help
    Manage haproxy

    Usage:
        haproxytool haproxy [-D DIR | -F SOCKET] (-a | -A | -C | -e | -i | -M |
                                                -o | -r | -u | -U | -V | -R | -p)
        haproxytool haproxy [-D DIR | -F SOCKET] -m METRIC
        haproxytool haproxy [-D DIR | -F SOCKET] -w OPTION VALUE
        haproxytool haproxy [-D DIR | -F SOCKET] -c COMMAND

    Arguments:
        DIR     Directory path with socket files
        OPTION  Option name to set a VALUE
        VALUE   Value to set
        METRIC  Name of a metric, use '-M' to get metric names

    Options:
        -a, --all                   clear all statistics counters
        -A, --clear                 clear max values of statistics counters
        -c, --command               send a command to HAProxy
        -C, --maxconn               show configured maximum connection limit
        -e, --errors                show last know request and response errors
        -F SOCKET, --file SOCKET    socket file
        -i, --info                  show haproxy stats
        -m, --metric                show value of a METRIC
        -M, --show-metrics          show all metrics
        -o, --options               show value of options that can be changed with
                                    '-w' option
        -p, --pids                  show PIDs of HAProxy processes
        -r, --requests              show total cumulative number of requests
                                    processed by all processes
        -u, --uptime-secs           show uptime of HAProxy process in seconds
        -U, --uptime                show uptime of HAProxy process
        -V, --hap-version           show version of HAProxy
        -R, --release-date          show release date
        -w, --write                 set VALUE for an OPTION
        -D DIR, --socket-dir=DIR    directory with HAProxy socket files
                                    [default: /var/lib/haproxy]

Commands for frontends
~~~~~~~~~~~~~~~~~~~~~~

* Usage

::

    % haproxytool frontend --help
    Manage frontends

    Usage:
        haproxytool frontend [-D DIR -F SOCKET] (-c | -r | -s | -o | -e | -p | -i)
                             [NAME...]
        haproxytool frontend [-D DIR -F SOCKET] -w OPTION VALUE [NAME...]
        haproxytool frontend [-D DIR -F SOCKET] [-f ] (-d | -t) [NAME...]
        haproxytool frontend [-D DIR -F SOCKET] (-l | -M)
        haproxytool frontend [-D DIR -F SOCKET] -m METRIC [NAME...]

    Arguments:
        DIR     Directory path with socket files
        SOCKET  Socket file
        VALUE   Value to set
        OPTION  Setting name
        METRIC  Name of a metric, use '-M' to get metric names

    Options:
        -c, --showmaxconn         show max sessions
        -d, --disable             disable frontend
        -e, --enable              enable frontend
        -f, --force               force an operation
        -F SOCKET, --file SOCKET  socket file
        -h, --help                show this screen
        -i, --iid                 show proxy ID number
        -l, --show                show all frontends
        -m, --metric              show value of a metric
        -M, --show-metrics        show all metrics
        -o, --options             show value of options that can be changed with
                                '-w' option
        -p, --process             show process number
        -r, --requests            show requests
        -s, --status              show status
        -t, --shutdown            shutdown frontend
        -w, --write               change a frontend option
        -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                                [default: /var/lib/haproxy]

* Show status of frontend(s)

::

    % haproxytool frontend -s
    frontend_proc1 OPEN
    frontend2_proc34 OPEN
    haproxy OPEN
    frontend1_proc34 OPEN
    frontend_proc2 OPEN

    % haproxytool frontend -s frontend2_proc34
    frontend2_proc34 OPEN

* Show requests

::

    % haproxytool frontend -r frontend2_proc34
    frontend2_proc34 10

* Show in which HAProxy process a frontend is used

::

    % haproxytool frontend -p frontend2_proc34
    frontend2_proc34 [4, 3]

* Show option(s) that can be changed

:NOTE: Currently, HAProxy allows only to change the maximum connections option for the frontends.

::

    % haproxytool frontend -o frontend_proc1
    frontend_proc1 maxconn=1000000

* Change an option

::

    % haproxytool frontend -w maxconn 100000 frontend_proc1
    frontend_proc1 set maxconn to 100000

    % haproxytool frontend -o frontend_proc1
    frontend_proc1 maxconn=100000

* Changing an option for a frontend assigned to multiple HAProxy process

::

    % haproxytool frontend -o frontend1_proc34
    frontend1_proc34 maxconn=2000000

    % haproxytool frontend -w maxconn 40000 frontend1_proc34
    frontend1_proc34 set maxconn to 40000

    % haproxytool frontend -o frontend1_proc34
    frontend1_proc34 maxconn=80000

    % haproxytool frontend -p frontend1_proc34
    frontend1_proc34 [4, 3]

:NOTE: It is not supported to change a option only to one of the HAProxy
    process

:NOTE: The return value of the option is the sum of the values across all
    HAProxy processes

Commands for backends
~~~~~~~~~~~~~~~~~~~~~

* Usage

::

    % haproxytool backend --help
    Manage backends

    Usage:
        haproxytool backend [-D DIR | -F SOCKET] (-S | -r | -p | -s | -i) [NAME...]
        haproxytool backend [-D DIR | -F SOCKET] (-l | -M)
        haproxytool backend [-D DIR | -F SOCKET] -m METRIC [NAME...]

    Arguments:
        DIR     Directory path with socket files
        SOCKET  Socket file
        METRIC  Name of a metric, use '-M' to get metric names

    Options:
        -F SOCKET, --file SOCKET  socket file
        -h, --help                show this screen
        -i, --iid                 show proxy ID number
        -l, --show                show all backends
        -m, --metric              show value of a metric
        -M, --show-metrics        show all metrics
        -p, --process             show process number
        -r, --requests            show requests
        -s, --status              show status
        -S, --servers             show servers
        -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                                  [default: /var/lib/haproxy]

Commands for servers
~~~~~~~~~~~~~~~~~~~~

* Usage

::

    % haproxytool server --help
    Manage servers

    Usage:
        haproxytool server [-D DIR | -F SOCKET] (-r | -s | -e | -R | -p | -W | -i |
                        -c | -C | -S) [--backend=<name>...] [NAME...]
        haproxytool server [-D DIR | -F SOCKET] -w VALUE [--backend=<name>...]
                        [NAME...]
        haproxytool server [-D DIR | -F SOCKET] [-f ] (-d | -t | -n)
                        [--backend=<name>...] [NAME...]
        haproxytool server [-D DIR | -F SOCKET] (-l | -M)
        haproxytool server [-D DIR | -F SOCKET] -m METRIC [--backend=<name>...]
                        [NAME...]


    Arguments:
        DIR     Directory path with socket files
        SOCKET  Socket file
        VALUE   Value to set
        METRIC  Name of a metric, use '-M' to get metric names

    Options:
        -c, --show-check-code     show check code
        -C, --show-check-status   show check status
        -d, --disable             disable server
        -e, --enable              enable server
        -f, --force               force an operation
        -F SOCKET, --file SOCKET  socket file
        -h, --help                show this screen
        -i, --sid                 show server ID
        -l, --show                show all servers
        -m, --metric              show value of a metric
        -M, --show-metrics        show all metrics
        -n, --drain               drain server
        -p, --process             show process number
        -r, --requests            show requests
        -R, --ready               set server in normal mode
        -s, --status              show status
        -S, --show-last-status    show last check status
        -t, --maintenance         set server in maintenance mode
        -w, --weight              change weight for server
        -W, --get-weight          show weight of server
        -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                                  [default: /var/lib/haproxy]

* List all servers

::

    % haproxytool server -l
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

    % haproxytool server -s --backend=backend_proc1
    # backendname servername
    backend_proc1                  bck_all_srv1                               DOWN
    backend_proc1                  member1_proc1                              no check
    backend_proc1                  member2_proc1                              no check


    % haproxytool server -s --backend=backend_proc1 --backend=backend2_proc34
    # backendname servername
    backend_proc1                  member1_proc1                              no check
    backend_proc1                  bck_all_srv1                               DOWN
    backend_proc1                  member2_proc1                              no check
    backend2_proc34                bck2_proc34_srv2                           UP
    backend2_proc34                bck2_proc34_srv1                           no check
    backend2_proc34                bck_all_srv1                               no check

* Show weight of servers across all backends and per backend

::

    % haproxytool server -W bck_all_srv1
    # backendname servername
    backend1_proc34                bck_all_srv1                               1
    backend2_proc34                bck_all_srv1                               1
    backend_proc1                  bck_all_srv1                               100
    pparissis at axilleas in ~/bin

    % haproxytool server -W bck_all_srv1 --backend=backend_proc1 --backend=backend2_proc34
    # backendname servername
    backend_proc1                  bck_all_srv1                               100
    backend2_proc34                bck_all_srv1                               1
    pparissis at axilleas in ~/bin

* Set weight on servers across all backends and per backend

::

    % haproxytool server -w 10 bck_all_srv1
    bck_all_srv1 backend set weight to 10 in backend2_proc34 backend
    bck_all_srv1 backend set weight to 10 in backend1_proc34 backend
    bck_all_srv1 backend set weight to 10 in backend_proc1 backend

    % haproxytool server -w 50 bck_all_srv1 --backend=backend_proc1 --backend=backend2_proc34
    bck_all_srv1 backend set weight to 50 in backend_proc1 backend
    bck_all_srv1 backend set weight to 50 in backend2_proc34 backend
    pparissis at axilleas in ~/bin

* Show requests

::

    % haproxytool server -r bck_all_srv1
    # backendname servername
    backend_proc1                  bck_all_srv1                               0
    backend2_proc34                bck_all_srv1                               2
    backend1_proc34                bck_all_srv1                               10

* List metric names available from the statistics

::

    % haproxytool server -M
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


    % haproxytool server -m bin bck_all_srv1
    # backendname servername
    backend1_proc34                bck_all_srv1                               760
    backend2_proc34                bck_all_srv1                               152
    backend_proc1                  bck_all_srv1                               0

* Show in which HAProxy process a server is used

::

    % haproxytool server -p bck_all_srv1
    # backendname servername
    backend2_proc34                bck_all_srv1                               [4, 3]
    backend_proc1                  bck_all_srv1                               [1]
    backend1_proc34                bck_all_srv1                               [4, 3]

* Enable/disable a server

::

    % haproxytool server -d bck_all_srv1
    Are you sure we want to disable 3 servers y/n?: y
    bck_all_srv1 disabled in backend1_proc34 backend
    bck_all_srv1 disabled in backend_proc1 backend
    bck_all_srv1 disabled in backend2_proc34 backend

:NOTE: When more than 1 server is about to be disabled, user is prompt to
       confirm the action. Use -f to force disabling servers.

::

    % haproxytool server -s bck_all_srv1
    # backendname servername
    backend_proc1                  bck_all_srv1                               MAINT
    backend2_proc34                bck_all_srv1                               MAINT
    backend1_proc34                bck_all_srv1                               MAINT

    % haproxytool server -e bck_all_srv1
    bck_all_srv1 enabled in backend2_proc34 backend
    bck_all_srv1 enabled in backend1_proc34 backend
    bck_all_srv1 enabled in backend_proc1 backend

    % haproxytool server -s bck_all_srv1
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
        haproxytool dump [-D DIR | -F SOCKET] [-fbsh]

    Arguments:
        SOCKET  Socket file

    Options:
        -f, --frontends           show frontends
        -F SOCKET, --file SOCKET  socket file
        -b, --backends            show backends
        -s, --servers             show servers
        -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                                  [default: /var/lib/haproxy]

Map command
~~~~~~~~~~~~

* Usage

::

    % haproxytool map --help
    Manage MAPs

    Usage:
        haproxytool map [-D DIR | -F SOCKET] -l
        haproxytool map [-D DIR | -F SOCKET] (-s | -c ) MAPID
        haproxytool map [-D DIR | -F SOCKET] -g MAPID KEY
        haproxytool map [-D DIR | -F SOCKET] (-S | -A) MAPID KEY VALUE
        haproxytool map [-D DIR | -F SOCKET] -d MAPID KEY


    Arguments:
        DIR     Directory path with socket files
        MAPID   ID of the map or file returned by show map
        KEY     ID of key
        SOCKET  Socket file
        VALUE   Value to set

    Options:
        -A, --add                 add a <KEY> entry into the map <MAPID>
        -F SOCKET, --file SOCKET  socket file
        -h, --help                show this screen
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

    % haproxytool map -l
    # id (file) description
    4 (/etc/haproxy/v-m1-bk) pattern loaded from file '/etc/haproxy/v-m1-bk'
    used by map at file '/etc/haproxy/haproxy.cfg' line 87

* Show the content of a map

::

    % haproxytool map -s 4
    0xb743f0 0 www.foo.com-0
    0xb74460 1 www.foo.com-1

* Add a key to a map

::

    % haproxytool map -A 4 3 www.goo.com
    key was added successfully

    % haproxytool map -s 4
    0xb743f0 0 www.foo.com-0
    0xb74460 1 www.foo.com-1
    0x28f0f50 3 www.goo.com

* Delete an entry from a map

::

    % haproxytool map -d 4 3
    key was deleted successfully

    % haproxytool map -s 4
    0xb743f0 0 www.foo.com-0
    0xb74460 1 www.foo.com-1

* Set a value for a key in a map

::

    % haproxytool map -S 4 1 bar.com
    value was set successfully

    % haproxytool map -s 4
    0xb743f0 0 www.foo.com-0
    0xb74460 1 bar.com

* Clear all entries of a map

::

    % haproxytool map -c 4
    all entries of map were cleared successfully

    % haproxytool map -s 4

    %

:NOTE: Currently, HAProxy doesn't allow to create new MAPs via the stats socket.

ACL command
~~~~~~~~~~~

* Usage

::

    % haproxytool acl --help
    Manage ACLs

    Usage:
        haproxytool acl [-D DIR | -F SOCKET] -l
        haproxytool acl [-D DIR | -F SOCKET] (-c | -s) ACLID
        haproxytool acl [-D DIR | -F SOCKET] (-A | -g ) ACLID VALUE
        haproxytool acl [-D DIR | -F SOCKET] -d ACLID KEY


    Arguments:
        DIR     Directory path with socket files
        ACLID   ID of the acl or file returned by show acl
        SOCKET  Socket file
        VALUE   Value to set
        KEY     Key ID of ACL value/pattern

    Options:
        -h, --help                show this screen
        -A, --add                 add a <KEY> entry into the acl <ACLID>
        -F SOCKET, --file SOCKET  socket file
        -s, --show                show acl
        -g, --get                 lookup the value of a key in the acl
        -c, --clear               clear all entries for a acl
        -l, --list                list all acl ids
        -d, --delete              delete all the acl entries from the acl <ACLID>
                                  corresponding to the key <KEY>
        -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                                  [default: /var/lib/haproxy]

* List all ACLIDs

::


    % haproxytool acl -D /run/haproxy -l
    # id (file) description
    0 (/etc/haproxy/wl_stats) pattern loaded from file '/etc/haproxy/wl_stats' used by acl at file '/etc/haproxy/haproxy.cfg' line 55
    1 () acl 'src' file '/etc/haproxy/haproxy.cfg' line 55
    2 (/etc/haproxy/bl_frontend) pattern loaded from file '/etc/haproxy/bl_frontend' used by acl at file '/etc/haproxy/haproxy.cfg' line 85
    3 () acl 'src' file '/etc/haproxy/haproxy.cfg' line 85
    5 () acl 'ssl_fc' file '/etc/haproxy/haproxy.cfg' line 88
    6 () acl 'req.cook' file '/etc/haproxy/haproxy.cfg' line 101
    7 () acl 'req.cook' file '/etc/haproxy/haproxy.cfg' line 102
    8 () acl 'req.cook' file '/etc/haproxy/haproxy.cfg' line 103

* Show the content of a acl

::

    % haproxytool acl -D /run/haproxy -s 2
    0x2115c90 11.155.183.41
    0x3e92f80 10.10.10.10

* Add an entry in a acl

::

    % haproxytool acl -D /run/haproxy --add 2 12.12.12.0
    value was added successfully

    % haproxytool acl -D /run/haproxy -s 2
    0x2115c90 11.155.183.41
    0x3e92f80 10.10.10.10
    0x21341e0 12.12.12.0

* Delete an entry from acl

::

    % haproxytool acl -D /run/haproxy --delete 2 12.12.12.0
    key was deleted successfully

    % haproxytool acl -D /run/haproxy -s 2
    0x2115c90 11.155.183.41
    0x3e92f80 10.10.10.10

* Lookup entries in acl for debugging purposes

::

    % haproxytool acl -D /run/haproxy -g 2 11.155.183.41
    type=ip, case=sensitive, match=yes, idx=tree, pattern="11.155.183.41"

    %haproxytool acl -D /run/haproxy -g 2 11.155.183.0
    type=ip, case=sensitive, match=no

* Clear all entries from a acl

::

    % haproxytool acl -D /run/haproxy -s 2
    0x2115c90 11.155.183.41
    0x3e92f80 10.10.10.10

    % haproxytool acl -D /run/haproxy -c 2
    all entries of acl were cleared successfully

    % haproxytool acl -D /run/haproxy -s 2

    %

Release
-------

#. Bump version in haproxytool/__init__.py

#. Commit above change with::

      git commit -av -m'RELEASE 0.1.3 version'

#. Create a signed tag, pbr will use this for the version number::

      git tag -s 0.1.3 -m 'bump release'

#. Create the source distribution archive (the archive will be placed in the
   **dist** directory)::

      python setup.py sdist

#. pbr updates ChangeLog file and we want to squeeze this change to the
   previous commit, thus run::

      git commit -av --amend

#. Move current tag to the last commit::

      git tag -fs 0.1.3 -m 'bump release'

#. Push changes::

      git push;git push --tags

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

**Author**: Pavlos Parissis <pavlos.parissis@gmail.com>
