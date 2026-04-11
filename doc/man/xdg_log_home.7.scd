xdg_log_home(7)

# NAME

xdg_log_home - XDG base directory for user-specific log files

# DESCRIPTION

*$XDG_LOG_HOME* defines the base directory relative to which user-specific
log files should be stored.

Log files are informational records of application activity intended for
debugging, auditing, or monitoring. They are append-oriented and may grow
without bound. Deleting log files MUST NOT affect the correctness or
functionality of applications.

# DEFAULT

If *$XDG_LOG_HOME* is either not set or empty, a default equal to
_$HOME/.local/log_ should be used.

# NOTES

Applications SHOULD organize log files into subdirectories of
*$XDG_LOG_HOME* named after the application. Applications SHOULD document
their log retention expectations.

*$XDG_LOG_HOME* takes precedence over any directory in *$XDG_LOG_DIRS*.

# SEE ALSO

*basedir-spec*(7), *xdg_log_dirs*(7), *xdg_state_home*(7)
