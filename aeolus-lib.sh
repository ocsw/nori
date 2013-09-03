############
# debugging
############

#
# turn on shell command printing for particular commands
#
# commands will be printed preceded by 'cmd: '
#
# note that any variables set on the same line as the command will be
# printed on separate lines, one variable per line, e.g.:
#   cmd: foo=bar
#   cmd: baz=quux
#   cmd: do_something arg1 arg2 arg3
#
[ "${skip_begincmdprint+X}" = "" ] && \
begincmdprint () {



##################################
# SSH remote commands and tunnels
##################################

#
# run a remote SSH command
#
# ssh_options and ssh_rcommand must be indexed, non-sparse arrays
#
# global vars: cmdexitval
# config settings: ssh_port, ssh_keyfile, ssh_options, ssh_user, ssh_host,
#                  ssh_rcommand
# library functions: begincmdprint(), endcmdprint()
# utilities: ssh
# files: $ssh_keyfile
# bashisms: arrays
#
[ "${skip_sshremotecmd+X}" = "" ] && \
sshremotecmd () {
  begincmdprint
  ssh \
    ${ssh_port:+-p "$ssh_port"} \
    ${ssh_keyfile:+-i "$ssh_keyfile"} \
    "${ssh_options[@]}" \
    ${ssh_user:+-l "$ssh_user"} \
    "$ssh_host" \
    "${ssh_rcommand[@]}"
  endcmdprint 2>/dev/null

  return "$cmdexitval"
}

#
# run a remote SSH command in the background
#
# $1 is the name of a global variable to store the ssh PID in, to
# differentiate between multiple commands; if unset or null, it defaults to
# "sshpid"
#
# if $2 is unset or null, a callback function to kill the ssh process when
# the script exits will be registered; to prevent this, make $2 non-null
# (suggested value: "noauto")
#
# (to set $2 while leaving $1 as the default, use "" for $1)
#
# ssh_options and ssh_rcommand must be indexed, non-sparse arrays
#
# "local" vars: sshpid_var, sshpid_l
# global vars: (contents of $1, or sshpid), cmdpid
# config settings: ssh_port, ssh_keyfile, ssh_options, ssh_user, ssh_host,
#                  ssh_rcommand
# library functions: begincmdprint(), endcmdprintbg(), addexitcallback(),
#                    killsshremotebg()
# utilities: ssh, printf, [
# files: $ssh_keyfile
# bashisms: arrays, printf -v [v3.1]
#
[ "${skip_sshremotebgcmd+X}" = "" ] && \
sshremotebgcmd () {
  # apply default
  sshpid_var="sshpid"

  # get value, if set
  [ "$1" != "" ] && sshpid_var="$1"

  # run the command
  begincmdprint
  ssh \
    ${ssh_port:+-p "$ssh_port"} \
    ${ssh_keyfile:+-i "$ssh_keyfile"} \
    "${ssh_options[@]}" \
    ${ssh_user:+-l "$ssh_user"} \
    "$ssh_host" \
    "${ssh_rcommand[@]}" \
    &
  endcmdprintbg 2>/dev/null

  # register the exit callback
  [ "$2" = "" ] && addexitcallback "killsshremotebg" "$sshpid_var"

  # get the PID
  sshpid_l="$cmdpid"
  printf -v "$sshpid_var" "%s" "$sshpid_l"  # set the global
}

#
# kill a backgrounded remote SSH command
#
# $1 is the name of a global variable that contains the ssh PID, to
# differentiate between multiple commands; if unset or null, it defaults to
# "sshpid"
#
# if $2 is unset or null, the callback function to kill the ssh process when
# the script exits will be unregistered (see sshremotebgcmd()); to prevent
# this, make $2 non-null (suggested value: "noauto")
#
# (to set $2 while leaving $1 as the default, use "" for $1)
#
# can be run even if the command was already killed / died
#
# "local" vars: sshpid_var, sshpid_l
# global vars: (contents of $1, or sshpid)
# library functions: removeexitcallback()
# utilities: printf, kill, [
# bashisms: ${!var}, printf -v [v3.1]
#
[ "${skip_killsshremotebg+X}" = "" ] && \
killsshremotebg () {
  # apply default
  sshpid_var="sshpid"

  # get value, if set
  [ "$1" != "" ] && sshpid_var="$1"

  # get the PID
  sshpid_l="${!sshpid_var}"

  if [ "$sshpid_l" != "" ]; then
    kill "$sshpid_l" > /dev/null 2>&1  # don't complain if it's already dead
    wait "$sshpid_l"
    printf -v "$sshpid_var" "%s" ""  # so we know it's been killed
  fi

  # unregister the exit callback
  [ "$2" = "" ] && removeexitcallback "killsshremotebg" "$sshpid_var"
}

#
# run an SSH tunnel command
#
# $1 is the name of a global variable to store the ssh PID in, to
# differentiate between multiple tunnels; if unset or null, it defaults to
# "tunpid"
#
# if $2 is unset or null, a callback function to kill the ssh process when
# the script exits will be registered; to prevent this, make $2 non-null
# (suggested value: "noauto")
#
# (to set $2 while leaving $1 as the default, use "" for $1)
#
# tun_sshoptions must be an indexed, non-sparse array
#
# "local" vars: tunpid_var, tunpid_l
# global vars: (contents of $1, or tunpid), cmdpid
# config settings: tun_localport, tun_remotehost, tun_remoteport,
#                  tun_sshport, tun_sshkeyfile, tun_sshoptions, tun_sshuser,
#                  tun_sshhost
# library functions: begincmdprint(), endcmdprintbg(), addexitcallback(),
#                    killsshtunnel()
# utilities: ssh, printf, [
# files: $tun_sshkeyfile
# bashisms: arrays, printf -v [v3.1]
#
[ "${skip_sshtunnelcmd+X}" = "" ] && \
sshtunnelcmd () {
  # apply default
  tunpid_var="tunpid"

  # get value, if set
  [ "$1" != "" ] && tunpid_var="$1"

  # run the command
  begincmdprint
  ssh \
    -L "${tun_localport}:${tun_remotehost}:${tun_remoteport}" -N \
    ${tun_sshport:+-p "$tun_sshport"} \
    ${tun_sshkeyfile:+-i "$tun_sshkeyfile"} \
    "${tun_sshoptions[@]}" \
    ${tun_sshuser:+-l "$tun_sshuser"} \
    "$tun_sshhost" \
    &
  endcmdprintbg 2>/dev/null

  # register the exit callback
  [ "$2" = "" ] && addexitcallback "killsshtunnel" "$tunpid_var"

  # get the PID
  tunpid_l="$cmdpid"
  printf -v "$tunpid_var" "%s" "$tunpid_l"  # set the global
}

#
# kill an SSH tunnel
#
# $1 is the name of a global variable that contains the ssh PID, to
# differentiate between multiple tunnels; if unset or null, it defaults to
# "tunpid"
#
# if $2 is unset or null, the callback function to kill the ssh process when
# the script exits will be unregistered (see sshtunnelcmd()); to prevent
# this, make $2 non-null (suggested value: "noauto")
#
# (to set $2 while leaving $1 as the default, use "" for $1)
#
# can be run even if the tunnel already died / was closed / was killed
#
# note: this will hang if the remote port isn't open; you should be using
# opensshtunnel(), or duplicating its functionality
#
# "local" vars: tunpid_var, tunpid_l
# global vars: (contents of $1, or tunpid)
# library functions: removeexitcallback()
# utilities: printf, kill, [
# bashisms: ${!var}, printf -v [v3.1]
#
[ "${skip_killsshtunnel+X}" = "" ] && \
killsshtunnel () {
  # apply default
  tunpid_var="tunpid"

  # get value, if set
  [ "$1" != "" ] && tunpid_var="$1"

  # get the PID
  tunpid_l="${!tunpid_var}"

  if [ "$tunpid_l" != "" ]; then
    kill "$tunpid_l" > /dev/null 2>&1  # don't complain if it's already dead
    wait "$tunpid_l"
    printf -v "$tunpid_var" "%s" ""  # so we know it's been killed
  fi

  # unregister the exit callback
  [ "$2" = "" ] && removeexitcallback "killsshtunnel" "$tunpid_var"
}

#
# open an SSH tunnel, including testing and logging
#
# $1 is the name of a global variable to store the ssh PID in, to
# differentiate between multiple tunnels; if unset or null, it defaults to
# "tunpid" (example setting suggestion: "rsynctunpid")
#
# $tun_descr should be a description of the tunnel's purpose (e.g.
# "mysql dumps" or "rsync backups"); this is used in status and error
# messages
# a global variable with name "$1_descr" (defaults to "tunpid_descr"
# if $1 is unset or null) will be used to save the current value of
# $tun_descr
#
# if $2 is unset or null, a callback function to close the tunnel when
# the script exits will be registered; to prevent this, make $2 non-null
# (suggested value: "noauto")
#
# (to set $2 while leaving $1 as the default, use "" for $1)
#
# returns 0 on success
# on error, calls sendalert(), then acts according to the value of
# tun_on_err:
#   "exit": exits the script with exitval $sshtunnel_exitval
#   "phase": returns 1 ("abort this phase of the script")
# if tun_on_err is unset or null, it defaults to "exit"
#
# FD 3 gets a start message and the actual output (stdout and stderr) of
# ssh
#
# "local" vars: tunpid_var, tunpid_l, waited, sshexit
# global vars: (contents of $1, or tunpid, and the corresponding *_descr),
#              tun_descr, phaseerr
# config settings: tun_localhost, tun_localport, tun_sshtimeout, tun_on_err
# library vars: newline, sshtunnel_exitval
# library functions: sshtunnelcmd(), logstatus(), logstatusquiet(),
#                    sendalert(), addexitcallback(), closesshtunnel(),
#                    do_exit()
# utilities: nc, printf, sleep, kill, expr, [
# FDs: 3
# bashisms: ${!var}, printf -v [v3.1]
#
[ "${skip_opensshtunnel+X}" = "" ] && \
opensshtunnel () {
  # apply default
  tunpid_var="tunpid"

  # get value, if set
  [ "$1" != "" ] && tunpid_var="$1"

  # save tun_descr
  printf -v "${tunpid_var}_descr" "%s" "$tun_descr"

  # log that we're running the command
  logstatusquiet "running SSH tunnel command for $tun_descr"
  printf "%s\n" "running SSH tunnel command for $tun_descr" >&3

  # run the command and get the PID
  sshtunnelcmd "$tunpid_var" "noauto" >&3 2>&1
  tunpid_l="${!tunpid_var}"

  # register the exit callback
  [ "$2" = "" ] && addexitcallback "closesshtunnel" "$tunpid_var"

  # make sure it's actually working;
  # see http://mywiki.wooledge.org/ProcessManagement#Starting_a_.22daemon.22_and_checking_whether_it_started_successfully
  waited="1"  # will be 1 once we actually enter the loop
  while sleep 1; do
    # some versions of nc print success messages; we don't want the
    # clutter, especially if quiet="yes"
    nc -z "$tun_localhost" "$tun_localport" > /dev/null 2>&1 && break

    # not working yet, but is it still running?
    if kill -0 "$tunpid_l" > /dev/null 2>&1; then  # quiet if already dead
      # expr is more portable than $(())
      waited=$(expr "$waited" + 1)

      if [ "$waited" -ge "$tun_sshtimeout" ]; then
        kill "$tunpid_l" > /dev/null 2>&1  # quiet if it's already dead
        wait "$tunpid_l"
        # so we know it's not running anymore
        printf -v "$tunpid_var" "%s" ""

        case "$tun_on_err" in
          phase)
            sendalert "could not establish SSH tunnel for $tun_descr (timed out);${newline}aborting $tun_descr" log
            phaseerr="$sshtunnel_exitval"
            return 1  # abort this phase of the script
            ;;
          *)  # exit
            sendalert "could not establish SSH tunnel for $tun_descr (timed out); exiting" log
            do_exit "$sshtunnel_exitval"
            ;;
        esac
      fi
    else  # process is already dead
      wait "$tunpid_l"
      sshexit="$?"

      # so we know it's not running anymore
      printf -v "$tunpid_var" "%s" ""

      case "$tun_on_err" in
        phase)
          sendalert "could not establish SSH tunnel for $tun_descr (status code $sshexit);${newline}aborting $tun_descr" log
          phaseerr="$sshtunnel_exitval"
          return 1  # abort this phase of the script
          ;;
        *)  # exit
          sendalert "could not establish SSH tunnel for $tun_descr (status code $sshexit); exiting" log
          do_exit "$sshtunnel_exitval"
          ;;
      esac
    fi  # if kill -0
  done  # while sleep 1

  logstatus "SSH tunnel for $tun_descr established"

  return 0
}

#
# close an SSH tunnel, including logging
# (tunnel must have been opened with opensshtunnel())
#
# $1 is the name of a global variable that contains the ssh PID, to
# differentiate between multiple tunnels; if unset or null, it defaults to
# "tunpid"
#
# if $2 is unset or null, the callback function to kill the ssh process when
# the script exits will be unregistered (see opensshtunnel()); to prevent
# this, make $2 non-null (suggested value: "noauto")
#
# (to set $2 while leaving $1 as the default, use "" for $1)
#
# can be run even if the tunnel already died / was closed / was killed,
# but should not be run before the tunnel was started, or the logs won't
# make sense
#
# "local" vars: tunpid_var, tunpid_l, descr_l
# global vars: (contents of $1, or tunpid, and the corresponding *_descr)
# library functions: copyvar(), logstatus(), removeexitcallback()
# utilities: printf, kill, [
# bashisms: ${!var}, printf -v [v3.1]
#
[ "${skip_closesshtunnel+X}" = "" ] && \
closesshtunnel () {
  # apply default
  tunpid_var="tunpid"

  # get value, if set
  [ "$1" != "" ] && tunpid_var="$1"

  # get the PID and the descr
  tunpid_l="${!tunpid_var}"
  copyvar "${tunpid_var}_descr" "descr_l"

  if [ "$tunpid_l" != "" ]; then
    kill "$tunpid_l" > /dev/null 2>&1  # don't complain if it's already dead
    wait "$tunpid_l"
    printf -v "$tunpid_var" "%s" ""  # so we know it's been closed

    logstatus "SSH tunnel for $descr_l closed"
  else
    logstatus "SSH tunnel for $descr_l was already closed"
  fi

  # unregister the exit callback
  [ "$2" = "" ] && removeexitcallback "closesshtunnel" "$tunpid_var"
}


###################################
# database calls and manipulations
###################################

#
# run a database command
#
# $1 is the command to run
#
# dbms_prefix must be one of the accepted values (currently "mysql" or
# "postgres")
#
# when using an SSH tunnel, set host to "localhost" (or "127.0.0.1" /
# "::1" / etc. as necessary) and port to the local port of the tunnel
#
# (in the notes below, [dbms] = the value of $dbms_prefix)
#
# [dbms]_options must be an indexed, non-sparse array
#
# global vars: dbms_prefix, cmdexitval
# config settings: [dbms]_user, [dbms]_pwfile, [dbms]_protocol, [dbms]_host,
#                  [dbms]_port, [dbms]_socketfile, [dbms]_options,
#                  [dbms]_connectdb
# library functions: begincmdprint(), endcmdprint()
# utilities: mysql, psql
# files: $[dbms]_pwfile, $[dbms]_socketfile
# bashisms: arrays
#
[ "${skip_dbcmd+X}" = "" ] && \
dbcmd () {
  case "$dbms_prefix" in
    mysql)
      begincmdprint
      # --defaults-extra-file must be the first option if present
      mysql \
        ${mysql_pwfile:+"--defaults-extra-file=$mysql_pwfile"} \
        ${mysql_user:+-u "$mysql_user"} \
        ${mysql_protocol:+"--protocol=$mysql_protocol"} \
        ${mysql_host:+-h "$mysql_host"} \
        ${mysql_port:+-P "$mysql_port"} \
        ${mysql_socketfile:+-S "$mysql_socketfile"} \
        ${mysql_connectdb:+"$mysql_connectdb"} \
        "${mysql_options[@]}" \
        ${1+-e "$1"}
      endcmdprint 2>/dev/null
      ;;
    postgres)
      begincmdprint
      PGPASSFILE=${postgres_pwfile:+"$postgres_pwfile"} \
        psql \
        ${postgres_user:+-U "$postgres_user"} \
        ${postgres_host:+-h "$postgres_host"} \
        ${postgres_port:+-p "$postgres_port"} \
        ${postgres_connectdb:+-d "$postgres_connectdb"} \
        "${postgres_options[@]}" \
        ${1+-c "$1"}
      endcmdprint 2>/dev/null
      ;;
  esac

  return "$cmdexitval"
}

#
# run a get-database-list command
#
# (may not be possible/straightforward for all DBMSes)
#
# dbms_prefix must be one of the accepted values (currently "mysql" or
# "postgres")
#
# when using an SSH tunnel, set host to "localhost" (or "127.0.0.1" /
# "::1" / etc. as necessary) and port to the local port of the tunnel
#
# some options are pre-included:
#   MySQL:
#     -BN -e "SHOW DATABASES;"
#   PostgreSQL:
#     -At -c "SELECT datname FROM pg_catalog.pg_database;"
#
# (in the notes below, [dbms] = the value of $dbms_prefix)
#
# [dbms]_options must be an indexed, non-sparse array
#
# global vars: dbms_prefix, cmdexitval
# config settings: [dbms]_user, [dbms]_pwfile, [dbms]_protocol, [dbms]_host,
#                  [dbms]_port, [dbms]_socketfile, [dbms]_connectdb,
#                  [dbms]_options
# library functions: begincmdprint(), endcmdprint()
# utilities: mysql, psql
# files: $[dbms]_pwfile, $[dbms]_socketfile
# bashisms: arrays
#
[ "${skip_dblistcmd+X}" = "" ] && \
dblistcmd () {
  case "$dbms_prefix" in
    mysql)
      begincmdprint
      # --defaults-extra-file must be the first option if present
      mysql \
        ${mysql_pwfile:+"--defaults-extra-file=$mysql_pwfile"} \
        ${mysql_user:+-u "$mysql_user"} \
        ${mysql_protocol:+"--protocol=$mysql_protocol"} \
        ${mysql_host:+-h "$mysql_host"} \
        ${mysql_port:+-P "$mysql_port"} \
        ${mysql_socketfile:+-S "$mysql_socketfile"} \
        "${mysql_options[@]}" \
        -BN -e "SHOW DATABASES;"
      endcmdprint 2>/dev/null
      ;;
    postgres)
      begincmdprint
      PGPASSFILE=${postgres_pwfile:+"$postgres_pwfile"} \
        psql \
        ${postgres_user:+-U "$postgres_user"} \
        ${postgres_host:+-h "$postgres_host"} \
        ${postgres_port:+-p "$postgres_port"} \
        ${postgres_connectdb:+-d "$postgres_connectdb"} \
        "${postgres_options[@]}" \
        -At -c "SELECT datname FROM pg_catalog.pg_database;"
      endcmdprint 2>/dev/null
      ;;
  esac

  return "$cmdexitval"
}

#
# convert DB name escape sequences to the real characters
# used, e.g., on the output of dblistcmd()
#
# $1 = DB name to un-escape
#
# sequences to un-escape:
#
#   MySQL:
#     \n -> newline
#     \t -> tab
#     \\ -> \
#
#   PostgreSQL:
#     (none; DB names with newlines or tabs may cause problems)
#
# (that is, this function will carry out the mappings above, which are the
# reverse of the mappings used by the DBMSes)
#
# dbms_prefix must be one of the accepted values (currently "mysql" or
# "postgres")
#
# global vars: dbms_prefix
# library vars: tab
# utilities: printf, sed
#
[ "${skip_dbunescape+X}" = "" ] && \
dbunescape () {
  case "$dbms_prefix" in
    mysql)
      # note: \\ must be last; \t isn't portable in sed
      printf "%s\n" "$1" | \
        sed \
          -e 's/^\\n/\n/' -e 's/\([^\]\)\\n/\1\n/g' \
          -e "s/^\\\\t/$tab/" -e "s/\\([^\\]\)\\\\t/\\1$tab/g" \
          -e 's/\\\\/\\/g'
      ;;
    postgres)
      printf "%s\n" "$1"  # just echo the input
      ;;
  esac
}


###########################
# backups and file syncing
###########################

#
# run an rsync command
#
# for "tunnel" mode, SSH tunnel must be opened/closed separately; use
# "localhost" (or "127.0.0.1" / "::1" / etc.) for the host (in
# rsync_source/dest) and set rsync_port to the local port of the tunnel
#
# rsync_sshoptions can't contain spaces in "nodaemon" mode
#
# rsync_sshoptions, rsync_options, and rsync_source must be indexed,
# non-sparse arrays
#
# global vars: cmdexitval
# config settings: rsync_mode, rsync_pwfile, rsync_port, rsync_sshkeyfile,
#                  rsync_sshport, rsync_sshoptions, rsync_filterfile,
#                  rsync_options, rsync_source, rsync_dest
# library functions: begincmdprint(), endcmdprint()
# utilities: rsync, ssh
# files: $rsync_sshkeyfile, $rsync_pwfile, $rsync_filterfile
# bashisms: arrays
#
[ "${skip_rsynccmd+X}" = "" ] && \
rsynccmd () {
  case "$rsync_mode" in
    tunnel|direct)
      begincmdprint
      rsync \
        ${rsync_port:+"--port=$rsync_port"} \
        ${rsync_pwfile:+"--password-file=$rsync_pwfile"} \
        ${rsync_filterfile:+-f "merge $rsync_filterfile"} \
        "${rsync_options[@]}" \
        "${rsync_source[@]}" \
        "$rsync_dest"
      endcmdprint 2>/dev/null
      ;;
    nodaemon)
      begincmdprint
      # the ssh command has to be on one line, and every way I tried to embed
      # it had problems; this is the best method I can come up with, although
      # it breaks with spaces in the options array
      RSYNC_RSH="ssh ${rsync_sshkeyfile:+-i "$rsync_sshkeyfile"} ${rsync_sshport:+-p "$rsync_sshport"} ${rsync_sshoptions[@]}" \
        rsync \
        ${rsync_filterfile:+-f "merge $rsync_filterfile"} \
        "${rsync_options[@]}" \
        "${rsync_source[@]}" \
        "$rsync_dest"
      endcmdprint 2>/dev/null
      ;;
    local)
      begincmdprint
      rsync \
        ${rsync_filterfile:+-f "merge $rsync_filterfile"} \
        "${rsync_options[@]}" \
        "${rsync_source[@]}" \
        "$rsync_dest"
      endcmdprint 2>/dev/null
      ;;
  esac

  return "$cmdexitval"
}

#
# run an rdiff-backup command
#
# rsync_sshoptions can't contain spaces
#
# rdb_sshoptions and rdb_options must be indexed arrays
#
# "local" vars: rdb_cmdopt_tmp, rschemastr
# global vars: cmdexitval
# config settings: rdb_mode, rdb_sshkeyfile, rdb_sshport, rdb_sshoptions,
#                  rdb_options, rdb_cmdopt, rdb_source, rdb_dest
# library functions: copyarray(), begincmdprint(), endcmdprint()
# utilities: rdiff-backup, ssh, [
# files: $rdb_sshkeyfile
# bashisms: arrays, array+=() [v3.1]
#
[ "${skip_rdbcmd+X}" = "" ] && \
rdbcmd () {
  # use a copy so we don't change the real array, below
  copyarray "rdb_cmdopt" "rdb_cmdopt_tmp" exact

  # put rdb_source in the rdb_cmdopt_tmp array; this lets us omit it
  # completely with "${[@]}" instead of leaving a "" in the command,
  # if it's not set
  if [ "$rdb_source" != "" ]; then
    rdb_cmdopt_tmp+=("$rdb_source")
  fi

  case "$rdb_mode" in
    remote)
      # the ssh command has to be on one line, and every way I tried to embed
      # it had problems; this is the best method I can come up with, although
      # it breaks with spaces in the options array
      rschemastr="ssh ${rdb_sshkeyfile:+-i "$rdb_sshkeyfile"} ${rdb_sshport:+-p "$rdb_sshport"} ${rdb_sshoptions[@]} %s rdiff-backup --server"
      begincmdprint
      rdiff-backup \
        --remote-schema "$rschemastr" \
        "${rdb_options[@]}" \
        "${rdb_cmdopt_tmp[@]}" \
        "$rdb_dest"
      endcmdprint 2>/dev/null
      ;;
    local)
      begincmdprint
      rdiff-backup \
        "${rdb_options[@]}" \
        "${rdb_cmdopt_tmp[@]}" \
        "$rdb_dest"
      endcmdprint 2>/dev/null
      ;;
  esac

  return "$cmdexitval"
}

#
# run an rdiff-backup prune command; this is a wrapper around rdbcmd()
#
# "local" vars: rdbcmdexit, rdb_cmdopt_bak, rdb_source_bak
# config settings: rdb_cmdopt, rdb_source, rdb_prune
# library functions: copyarray(), rdbcmd()
# bashisms: arrays
#
[ "${skip_rdbprunecmd+X}" = "" ] && \
rdbprunecmd () {
  copyarray "rdb_cmdopt" "rdb_cmdopt_bak" exact
  rdb_cmdopt=(--remove-older-than "$rdb_prune" --force)
  rdb_source_bak="$rdb_source"
  rdb_source=""

  rdbcmd
  rdbcmdexit="$?"

  rdb_source="$rdb_source_bak"
  copyarray "rdb_cmdopt_bak" "rdb_cmdopt" exact
  return "$rdbcmdexit"
}
