xdg_runtime_dir(7)

# NAME

xdg_runtime_dir - XDG base directory for user-specific runtime files

# DESCRIPTION

*$XDG_RUNTIME_DIR* defines the base directory relative to which user-specific
non-essential runtime files and other file objects (such as sockets, named
pipes, etc.) should be stored.

# REQUIREMENTS

The directory MUST be owned by the user, and they MUST be the only one having
read and write access to it. Its Unix access mode MUST be 0700.

The lifetime of the directory MUST be bound to the user being logged in. It
MUST be created when the user first logs in and if the user fully logs out
the directory MUST be removed. If the user logs in more than once they should
get pointed to the same directory.

The directory MUST be on a local file system and not shared with any other
system. It must support AF_UNIX sockets, symbolic links, hard links, proper
permissions, file locking, sparse files, memory mapping, file change
notifications, and a reliable hard link count. No restrictions on the file
name character set should be imposed.

Files in the directory MUST NOT survive reboot or a full logout/login cycle.
Files MAY be subjected to periodic clean-up. To prevent removal, files should
have their access time timestamp modified at least once every 6 hours of
monotonic time or have the sticky bit set.

# DEFAULT

*$XDG_RUNTIME_DIR* is set by the login manager. There is no default value.
If not set, applications should fall back to a replacement directory with
similar capabilities and print a warning message.

# NOTES

Applications should use this directory for communication and synchronization
purposes and should not place larger files in it, since it might reside in
runtime memory and cannot necessarily be swapped out to disk.

# SEE ALSO

*basedir-spec*(7)
