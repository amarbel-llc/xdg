basedir-spec(7)

# NAME

basedir-spec - XDG Base Directory Specification

# DESCRIPTION

The XDG Base Directory Specification defines a set of environment variables
for locating user-specific and system-wide files. Applications use these
variables to determine where to read and write data, configuration, state,
log, cache, and runtime files.

All paths set in these variables must be absolute. Relative paths should be
considered invalid and ignored.

# ENVIRONMENT

The following environment variables are defined by version 0.9 of the
specification.

*$XDG_DATA_HOME*
	Base directory for user-specific data files.
	Default: _$HOME/.local/share_

*$XDG_CONFIG_HOME*
	Base directory for user-specific configuration files.
	Default: _$HOME/.config_

*$XDG_STATE_HOME*
	Base directory for user-specific state data.
	Default: _$HOME/.local/state_

*$XDG_LOG_HOME*
	Base directory for user-specific log files.
	Default: _$HOME/.local/log_

*$XDG_CACHE_HOME*
	Base directory for user-specific non-essential cached data.
	Default: _$HOME/.cache_

*$XDG_RUNTIME_DIR*
	Base directory for user-specific runtime files and sockets.
	Set by the login manager; no default.

*$XDG_DATA_DIRS*
	Preference-ordered search path for data files.
	Default: _/usr/local/share/:/usr/share/_

*$XDG_CONFIG_DIRS*
	Preference-ordered search path for configuration files.
	Default: _/etc/xdg_

*$XDG_LOG_DIRS*
	Preference-ordered search path for log files.
	Default: _/var/log_

# DIRECTORY CREATION

When writing a file, if the destination directory does not exist, an attempt
should be made to create it with permission 0700. Existing directory
permissions should not be changed.

# PRECEDENCE

For variables with both a HOME and DIRS variant, the HOME directory is
always considered more important than any directory in the DIRS search path.
Within a DIRS search path, earlier entries take precedence.

# SEE ALSO

*xdg_data_home*(7), *xdg_config_home*(7), *xdg_state_home*(7),
*xdg_log_home*(7), *xdg_cache_home*(7), *xdg_runtime_dir*(7),
*xdg_data_dirs*(7), *xdg_config_dirs*(7), *xdg_log_dirs*(7),
*environ*(7)
