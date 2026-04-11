xdg_state_home(7)

# NAME

xdg_state_home - XDG base directory for user-specific state data

# DESCRIPTION

*$XDG_STATE_HOME* defines the base directory relative to which user-specific
state files should be stored.

State data should persist between application restarts but is not important or
portable enough to be stored in *$XDG_DATA_HOME*. It may contain:

- Actions history (recently used files, command history)
- Current state of the application that can be reused on a restart (view,
  layout, open files, undo history)

Log files should be stored in *$XDG_LOG_HOME* instead.

# DEFAULT

If *$XDG_STATE_HOME* is either not set or empty, a default equal to
_$HOME/.local/state_ should be used.

# SEE ALSO

*basedir-spec*(7), *xdg_log_home*(7), *xdg_data_home*(7)
