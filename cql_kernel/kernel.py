import StringIO
from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF
from cassandra.cluster import Cluster
from cqlsh import setup_cqlruleset
from cqlshlib import cql3handling

from subprocess import check_output
from cqlsh import Shell

from os import unlink

import base64
import imghdr
import re
import signal
import urllib

__version__ = '0.2'

version_pat = re.compile(r'version (\d+(\.\d+)+)')

from .images import (
    extract_image_filenames, display_data_for_image, image_setup_cmd
)


class CQLKernel(Kernel):
    implementation = 'cql_kernel'
    implementation_version = __version__


    @property
    def language_version(self):
        m = version_pat.search(self.banner)
        return m.group(1)

    _banner = None

    @property
    def banner(self):
        if self._banner is None:
            self._banner = check_output(['CQL', '--version']).decode('utf-8')
        return self._banner

    language_info = {'name': 'CQL',
                     'codemirror_mode': 'shell',
                     'mimetype': 'text/x-sh',
                     'file_extension': '.sh'}

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_cql()


    def _start_cql(self):
        c = Cluster(["localhost"])
        self.cqlshell = Shell("127.0.0.1", 9042, use_conn = c )
        self.cqlshell.use_paging = False
        self.outputString = StringIO.StringIO()
        self.cqlshell.query_out = self.outputString

        setup_cqlruleset(cql3handling)

        # cql3handling
        pass

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):


        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        self.outputString.truncate(0)
        self.cqlshell.perform_statement(code)

        # print(self.outputString.getvalue())

        interrupted = False

        if not silent:
            # image_filenames, output = extract_image_filenames(output)

            # Send standard output
            # stream_content = {'name': 'stdout', 'text': self.outputString.getvalue()}
            # self.send_response(self.iopub_socket, 'stream', stream_content)
            stream_content = {'execution_count': 5, 'data': {'text/html':  self.outputString.getvalue()}}
            self.send_response(self.iopub_socket, 'execute_result', stream_content)

        #     # Send images, if any
        #     for filename in image_filenames:
        #         try:
        #             data = display_data_for_image(filename)
        #         except ValueError as e:
        #             message = {'name': 'stdout', 'text': str(e)}
        #             self.send_response(self.iopub_socket, 'stream', message)
        #         else:
        #             self.send_response(self.iopub_socket, 'display_data', data)
        #
        # if interrupted:
        #     return {'status': 'abort', 'execution_count': self.execution_count}
        #
        # try:
        #     exitcode = int(self.bashwrapper.run_command('echo $?').rstrip())
        # except Exception:
        #     exitcode = 1
        #
        # if exitcode:
        #     return {'status': 'error', 'execution_count': self.execution_count,
        #             'ename': '', 'evalue': str(exitcode), 'traceback': []}
        # else:
        #     return {'status': 'ok', 'execution_count': self.execution_count,
        #             'payload': [], 'user_expressions': {}}

    def do_complete(self, code, cursor_pos):
        code = code[:cursor_pos]
        default = {'matches': [], 'cursor_start': 0,
                   'cursor_end': cursor_pos, 'metadata': dict(),
                   'status': 'ok'}

        if not code or code[-1] == ' ':
            return default

        tokens = code.replace(';', ' ').split()
        if not tokens:
            return default

        matches = []
        token = tokens[-1]
        start = cursor_pos - len(token)

        if token[0] == '$':
            # complete variables
            cmd = 'compgen -A arrayvar -A export -A variable %s' % token[1:] # strip leading $
            output = self.bashwrapper.run_command(cmd).rstrip()
            completions = set(output.split())
            # append matches including leading $
            matches.extend(['$'+c for c in completions])
        else:
            # complete functions and builtins
            cmd = 'compgen -cdfa %s' % token
            output = self.bashwrapper.run_command(cmd).rstrip()
            matches.extend(output.split())
            
        if not matches:
            return default
        matches = [m for m in matches if m.startswith(token)]

        return {'matches': sorted(matches), 'cursor_start': start,
                'cursor_end': cursor_pos, 'metadata': dict(),
                'status': 'ok'}


