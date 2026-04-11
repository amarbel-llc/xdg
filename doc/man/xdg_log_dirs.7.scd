xdg_log_dirs(7)

# NAME

xdg_log_dirs - XDG search path for log files

# DESCRIPTION

*$XDG_LOG_DIRS* defines the preference-ordered set of base directories to
search for log files in addition to the *$XDG_LOG_HOME* base directory.
The directories should be separated with a colon (*:*).

# DEFAULT

If *$XDG_LOG_DIRS* is either not set or empty, a value equal to
_/var/log_ should be used.

# NOTES

*$XDG_LOG_HOME* is considered more important than any of the directories
defined by *$XDG_LOG_DIRS*. Within *$XDG_LOG_DIRS*, earlier entries take
precedence.

Specifications that reference *$XDG_LOG_DIRS* should define behavior when
a file is located under multiple base directories.

# SEE ALSO

*basedir-spec*(7), *xdg_log_home*(7)
