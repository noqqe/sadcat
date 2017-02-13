sadcat
======

My ssh config is hell. Even if its not much, its hell. I have ~190 host
entries which results in 1094(!) lines of sshconfig. Which I maintain
manually. Man-u-a-ll-y!

Why is that?

I use a lot of aliases to remember all my hosts. Which is probably my
fault but im used to it. A typical entry looked like

::

    Host nyc-cexapsdrap21.company.com drap21 pdrap21
      Hostname nyc-cexapsdrap21.company.com
      User myuser
      Port 22
      IdentiyFile ~/.ssh/project_id_rsa

You can do a lot of stuff with wildcards in sshconfig. What you cant do
is having dynamic aliases (at least what I know). This would require a
templating like option.

And thats why i wrote this tiny script.

install & usage
~~~~~~~~~~~~~~~

as usual.

::

    pip install sadcat
    sadcat ~/.ssh/sadcat.toml

Personally i use two aliases

::

    # set refresh alias
    alias sshre="$SADCAT $HOME/.ssh/sadcat.toml > $HOME/.ssh/config"

    # set edit alias
    alias sshedit="$EDITOR $HOME/.ssh/sadcat.toml"

config
~~~~~~

ranges
^^^^^^

A minimal config would look like this.

.. code:: toml

    [hosts]

    [hosts.nyc-dpzzt]
    hostname = "nyc-dpzzt[01-03]"

and ``sadcat`` generates 3 ssh entries for you called ``nyc-dpzzt01``,
``nyc-dpzzt02`` and ``nyc-dpzzt03``. Simple.

templates
^^^^^^^^^

To save more lines you can apply a template to a hosts group

.. code:: toml

    [hosts]

    [hosts.twoleadingzeros]
    hostname = "fra1024mfoo[001-005]"
    template = "fra1024"

    [templates]

    [templates.fra1024]
    user = "otheruser"
    port = "2202"

Of course, setting a variable in ``hosts`` will always overwrite those
being set in ``templates``.

There is a special template that is applied to every host if its
configured called "default". (``[templates.default]``)

aliases
~~~~~~~

those can be specified in ``hosts`` using a ``toml`` array if multiple
or a string. Range numbers (if available) will be applied at the end.
Thats just how i like it. Theres no deeper meaning.

::

    [hosts.hostsaliases]
    hostname = "nyc-dpzzt[5-9]"
    template = "company"
    alias = [ "dypppt", "dzzzpt" ]

would result in

::

    Host nyc-dpzzt5 dypppt5 dzzzpt5
      hostname ...

    Host nyc-dpzzt6 dypppt6 dzzzpt6
      hostname ...

but as said, ``alias`` can also be just a string

::

    [hosts.hostsaliases]
    hostname = "nyc-dpzzt[5-9]"
    alias = "dypppt"

single hosts
^^^^^^^^^^^^

As you might expected, if you dont have a ``Range`` defined in a
hostname this entry will result in one single host.

.. code:: toml

    [hosts.singlehost]
    hostname = "fra1024mfoo23"
    user = "foo"

custom
~~~~~~

If all that is still not enough flexibility, you can add custom snippets
to your ssh config by defining multiline strings in the ``[custom]``
section with full hosts.

.. code:: toml

    [custom]

    hostsb = '''

    Host bar.foo
      hostname bla
      user foo

    Host foo.bar
      hostname foo
      user bar
      port par
    '''

    strangehost = '''

    Host baz
      hostname baz
      port 666
      user evil
    '''

For more detailed examples see ``conf.toml`` in this repo.

sadcat?
~~~~~~~

I used a project name generator and liked it.
