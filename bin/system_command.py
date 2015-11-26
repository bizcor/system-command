#!/usr/bin/env python

import subprocess


def system_command(cmd, return_state=False, show_output=False, show_error=False,
                   exception_on_error=True, echo=False,
                   show_state=False, cwd=None, env=None):
    """ use Popen to execute system command.
        arguments:
        . return_state:
            If True, return a dict including the command and args executed, the
            return code from the command, and the stdout and stderr of the
            command.  Note these will be the empty string if 'show_output' and
            'show_error', respectively, are given.  The default is to return
            the return code from command execution.
        . show_output:
            If True, send stdout of the command to stdout rather than captureu
            it in a command state dict (which is returned if 'return_state' is
            given)
        . show_error
            If True, send stderr of the command to stderr rather than capture
            it in a command state dict (which is returned if 'return_state'
            is given)
        . exception_on_error
            If True, raise RuntimeError if the return code from the command is
            non-zero
        . echo
            If True, print the command being executed to stdout
        . show_state
            If True, print the command_state dict to stdout after running the
            command
        . cwd
            Passed directly to Popen (which documentation see)
        . env
            Passed directly to Popen (which documentation see)
    """

    if echo:
        print('executing => {}'.format(cmd))

    stdout_ = stderr_ = None
    if not show_output:
        stdout_ = subprocess.PIPE
    if not show_error:
        stderr_ = subprocess.PIPE

    p = subprocess.Popen(cmd, stdout=stdout_, stderr=stderr_, cwd=cwd, env=env)
    cmd_stdout, cmd_stderr = p.communicate()
    cmd_status = p.returncode

    command_state = {
        'cmd': cmd,
        'status': cmd_status,
        'stdout': cmd_stdout,
        'stderr': cmd_stderr,
    }

    if cmd_status != 0 and exception_on_error is True:
        if exception_on_error:
            raise RuntimeError(str(command_state))

    if show_state:
        print(command_state)

    if return_state:
        return command_state
    else:
        return command_state['status']
