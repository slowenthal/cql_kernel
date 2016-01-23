import StringIO
from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF
from cassandra.cluster import Cluster
# from cqlsh import setup_cqlruleset
import sys
import cqlsh
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

    # TODO
    @property
    def banner(self):
        # if self._banner is None:
        #     self._banner = check_output(['CQL', '--version']).decode('utf-8')
        # Todo get right version

        self._banner = "CQL Version x"
        return self._banner

    language_info = {'name': 'CQL',
                     'codemirror_mode': 'sql',
                     'mimetype': 'text/x-cassandra',
                     'file_extension': '.cql'}

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_cql()


    def _start_cql(self):
        c = Cluster(["localhost"])
        self.cqlshell = Shell("127.0.0.1", 9042, use_conn = c )
        self.cqlshell.use_paging = False
        self.outStringWriter = StringIO.StringIO()
        self.cqlshell.query_out = self.outStringWriter
        self.cqlshell.stdout = self.outStringWriter

        cqlsh.setup_cqlruleset(cql3handling)
        cqlsh.setup_cqldocs(cql3handling)

        # cql3handling
        pass

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):


        cleanCode = code.strip()

        if not cleanCode:
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        if cleanCode[-1] != ';':
            cleanCode += ";"

        self.outStringWriter.truncate(0)

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = self.outStringWriter
        sys.stderr = self.outStringWriter

        self.cqlshell.onecmd(cleanCode)

        sys.stdout = old_stdout
        sys.stderr = old_stderr


        interrupted = False

        if not silent:

            outputStr = self.outStringWriter.getvalue()

            # CQL rows come back as HTML
            if outputStr[:2] == '\n<':
                mime_type = 'text/html'
            else:
                mime_type = 'text/plain'

            stream_content = {'execution_count': self.execution_count, 'data': {mime_type: outputStr}}

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

        return {'status': 'ok', 'execution_count': self.execution_count,
                'payload': [], 'user_expressions': {}}

    def do_complete(self, code, cursor_pos):
        code = code[:cursor_pos].strip()

        default = {'matches': [], 'cursor_start': 0,
                   'cursor_end': cursor_pos, 'metadata': dict(),
                   'status': 'ok'}

        # if not code or code[-1] == ' ':
        #     return default
        #
        matches = cql3handling.CqlRuleSet.cql_complete(code, "", cassandra_conn=self.cqlshell,
                                                   startsymbol='cqlshCommand')

        if not matches:
            return default

        tokens = code.replace(';', ' ').split()
        if not tokens:
            return default

        return {'matches': sorted(matches), 'cursor_start': cursor_pos,
                'cursor_end': cursor_pos, 'metadata': dict(),
                'status': 'ok'}


