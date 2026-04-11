xdg_data_dirs(7)

# NAME

xdg_data_dirs - XDG search path for data files

# DESCRIPTION

*$XDG_DATA_DIRS* defines the preference-ordered set of base directories to
search for data files in addition to the *$XDG_DATA_HOME* base directory.
The directories should be separated with a colon (*:*).

# DEFAULT

If *$XDG_DATA_DIRS* is either not set or empty, a value equal to
_/usr/local/share/:/usr/share/_ should be used.

# NOTES

*$XDG_DATA_HOME* is considered more important than any of the directories
defined by *$XDG_DATA_DIRS*. Within *$XDG_DATA_DIRS*, earlier entries take
precedence.

Specifications that reference *$XDG_DATA_DIRS* should define behavior when
a file is located under multiple base directories.

# SEE ALSO

*basedir-spec*(7), *xdg_data_home*(7)
