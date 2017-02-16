#!/usr/bin/env python

import os
import sys
import textwrap
import re
import toml

def parse_config(conffile):
    """"
    open and read config file
    :conffile: file path as str
    :returns: dict
    """

    if not os.path.isfile(conffile):
        print("Error: config not found")
        sys.exit(1)

    try:
        with open(conffile) as conffile:
            config = toml.loads(conffile.read())
    except toml.TomlDecodeError as e:
        print("Error: Invalid config.")
        print("Error was: %s" % e)
        sys.exit(1)

    return config

def generate_range(start, end):
    """
    Convert [01-09] or [5-9] to a list() of values like
    [ '01', '02', '03' ] or so. This list is used for the Host
    section loop afterwards
    :start: str
    :end: str
    """

    # if it seems to be a single host entry,
    # skip all this
    if start is None and end is None:
        return [""]

    # convert str to int
    s = int(start)
    e = int(end)

    # counting var
    c = s

    # get a list
    nlist = []

    # loop in range
    while c <= e:

        # 01
        if start.startswith("0"):
            nlist.append("%02d" % c)
        # 001
        elif start.startswith("00"):
            nlist.append("%03d" % c)
        # 1
        else:
            nlist.append("%01d" % c)

        c = c + 1

    return nlist

def delkey_if_exists(sec, key):
    """
    Just a simple wrapper to delete stuff from
    a dictionary
    :sec: dict
    :key: str
    :returns: dict
    """
    try:
        del sec[key]
    except (KeyError, TypeError):
        pass
    return sec


def ssh_block(nlist, start, end, section, template, defaults):
    for i in nlist:

        # working copy of the template object
        # to be able to remove keys that are in host section
        templ = dict(template)
        defs = dict(defaults)

        # build hostname and delete
        hostname = "%s%s%s" % (start, i, end)

        # build aliases and delete
        alias = ""
        try:
            if isinstance(section["alias"], list):
                for x in section["alias"]:
                    alias = alias + x + str(i) + " "
            else:
                alias = section["alias"] + str(i)
        except KeyError:
            pass


        # create hostname and host section
        print("Host %s %s" % (hostname,alias))
        print(" hostname %s" % hostname)

        # delete all keys from templ and defaults that are set in host
        # this effect is used to overwrite variables from templ
        # in host
        for key in section:
            templ = delkey_if_exists(templ, key)
            defs = delkey_if_exists(defs, key)

        # delete meta keys only used by sadcat itself
        section = delkey_if_exists(section, "template")
        section = delkey_if_exists(section, "hostname")

        # apply default vars
        for k, v in defs.iteritems():
            print(" %s %s" % (k,v))

        # apply all templ vars
        for k, v in templ.iteritems():
            print(" %s %s" % (k,v))

        # apply all left host section wars
        for k, v in section.iteritems():
            if not k == "alias":
                print(" %s %s" % (k,v))

        print("")

def get_template_for_host(section, config):
    """
    get template dict object from host section
    """
    try:
        template = section["template"]
        try:
            template = config["templates"][template]
        except KeyError:
            print("ERROR: Template %s does not exist!" % template)
            sys.exit(1)
    except KeyError:
        template = {}
        pass

    return template

def parse_hostname_exp(hostgroup):
    """
    Split hostname from foo[01-03]bar into
    01, 02, foo, bar.
    Bascially a very naive parser of regex ranges.
    """

    f = re.findall(r'(.*)\[(\d+)-(\d+)\](.*)', hostgroup["hostname"])

    try:
        rstart = f[0][1]
        rend = f[0][2]
        hstart = f[0][0]
        hend = f[0][3]
    except:
        # Seems to be a single host
        rstart = None
        rend = None
        hstart = hostgroup["hostname"]
        hend = ""

    return rstart, rend, hstart, hend

def generate_hosts(config):

    hosts = config["hosts"]

    try:
        defaults = config["templates"]["default"]
    except KeyError:
        defaults = {}

    for hostgroup in hosts:

        # new dict for this host section
        section = config["hosts"][hostgroup]

        # Comment for ssh config
        print("# %s\n" % hostgroup)

        # parse hostname expression
        rstart, rend, hstart, hend = parse_hostname_exp(section)

        # generate range
        nlist = generate_range(rstart, rend)

        # get template referenced in this host entry
        template = get_template_for_host(section, config)


        # fill all gathered informations into block generator
        ssh_block(nlist, hstart, hend, section, template, defaults)

def paste_appended_options(config):
    """
    Pasts appended ssh config parts from
    ssh config if any configured
    :returns: bool
    """
    try:
        print("# Custom appended section\n")
        for c in config["custom"].keys():
            print("# " + c)

            # this is a dirty hack for https://github.com/uiri/toml/issues/71
            for line in config["custom"][c].split('\n'):
                if "Host " in line:
                    print(textwrap.dedent(line))
                else:
                    print("  " + textwrap.dedent(line))

    except KeyError:
        pass

    return True

def main():

    # help
    if len(sys.argv) <= 1:
        print("Usage: %s conf.toml" % sys.argv[0])
        sys.exit(1)

    config = parse_config(sys.argv[1])
    generate_hosts(config)
    paste_appended_options(config)

if __name__ == '__main__':
    main()
