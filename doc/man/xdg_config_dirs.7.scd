xdg_config_dirs(7)

# NAME

xdg_config_dirs - XDG search path for configuration files

# DESCRIPTION

*$XDG_CONFIG_DIRS* defines the preference-ordered set of base directories to
search for configuration files in addition to the *$XDG_CONFIG_HOME* base
directory. The directories should be separated with a colon (*:*).

# DEFAULT

If *$XDG_CONFIG_DIRS* is either not set or empty, a value equal to
_/etc/xdg_ should be used.

# NOTES

*$XDG_CONFIG_HOME* is considered more important than any of the directories
defined by *$XDG_CONFIG_DIRS*. Within *$XDG_CONFIG_DIRS*, earlier entries
take precedence.

Specifications that reference *$XDG_CONFIG_DIRS* should define behavior when
a file is located under multiple base directories.

# SEE ALSO

*basedir-spec*(7), *xdg_config_home*(7)
