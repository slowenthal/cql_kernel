import io
import os
from ipykernel.kernelbase import Kernel

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from ssl import SSLContext, PROTOCOL_TLSv1_2

# from cqlsh import setup_cqlruleset
import sys
from . import cqlsh
from cqlshlib import cql3handling

from .cqlsh import Shell
import re

__version__ = '1.0.1'

version_pat = re.compile(r'version (\d+(\.\d+)+)')


class CQLKernel(Kernel):
    implementation = 'cqljupyter'
    implementation_version = __version__
    banner = "CQL kernel"
    language = "CQL"
    language_info = {'name': 'CQL',
                     'codemirror_mode': 'sql',
                     'mimetype': 'text/x-cassandra',
                     'file_extension': '.cql'}
    @property
    def language_version(self):
        m = version_pat.search(self.banner)
        return m.group(1)

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.hostname = os.environ.get('CASSANDRA_HOSTNAME', 'localhost')
        self.port = int(os.environ.get('CASSANDRA_PORT', "9042"))
        self.user = os.environ.get('CASSANDRA_USER')
        self.pwd = os.environ.get('CASSANDRA_PWD')
        self.ssl = os.environ.get('CASSANDRA_SSL') == "True"
        self._start_cql()

    def _start_cql(self):
        print(f"INFO ssl {self.ssl}")
        if self.user:
            auth_provider = PlainTextAuthProvider(username=self.user, password=self.pwd)
        else:
            auth_provider = None

        if self.ssl:
            c = Cluster([self.hostname], port=self.port, ssl_context=SSLContext(PROTOCOL_TLSv1_2))
        else:
            c = Cluster([self.hostname], auth_provider=auth_provider)

        # ssl_options=sslhandling.ssl_settings(hostname, CONFIG_FILE) if ssl else None

        print("about to connect ", self.user, self.pwd, flush=True)
        self.cqlshell = Shell(self.hostname, self.port, username=self.user, password=self.pwd,  use_conn=c)
        self.cqlshell.use_paging = False
        self.outStringWriter = io.StringIO()
        self.cqlshell.query_out = self.outStringWriter
        self.cqlshell.stdout = self.outStringWriter

        cqlsh.setup_cqlruleset(cql3handling)
        cqlsh.setup_cqldocs(cql3handling)

        # cql3handling
        pass

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):

        clean_code = code.strip()

        if not clean_code:
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        # HTML magic
        if clean_code[:6].upper() == "%%HTML":
            outputstr = clean_code[6:].strip()
        else:
            # This is a regular query
            if clean_code[-1] != ';':
                clean_code += ";"

            self.outStringWriter.truncate(0)

            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = self.outStringWriter
            sys.stderr = self.outStringWriter

            self.cqlshell.onecmd(clean_code)

            sys.stdout = old_stdout
            sys.stderr = old_stderr
            outputstr = self.outStringWriter.getvalue().strip()

        if not silent:

            # Format desc commands with codemirror (cool feature)

            if code.strip()[:4] == 'desc':
                outputstr = '<script>var x = CodeMirror.fromTextArea(document.getElementById("desc%d"), {readOnly: true, mode:"text/x-cassandra"} )</script><textarea id="desc%d">%s</textarea>' % (
                    self.execution_count, self.execution_count, outputstr)

            # CQL rows come back as HTML

            if outputstr[:1] == '<':
                mime_type = 'text/html'
            else:
                mime_type = 'text/plain'

            stream_content = {'execution_count': self.execution_count, 'data': {mime_type: outputstr}}

            self.send_response(self.iopub_socket, 'execute_result', stream_content)

        # if exitcode:
        #     return {'status': 'error', 'execution_count': self.execution_count,
        #             'ename': '', 'evalue': str(exitcode), 'traceback': []}
        # else:

        return {'status': 'ok', 'execution_count': self.execution_count,
                'payload': [], 'user_expressions': {}}

    def do_complete(self, code, cursor_pos):
        code = code[:cursor_pos]

        default = {'matches': [], 'cursor_start': 0,
                   'cursor_end': cursor_pos, 'metadata': dict(),
                   'status': 'ok'}

        # if not code or code[-1] == ' ':
        #     return default
        #

        # Find the rightmost of blank, . , <, (

        index = max(code.rfind(' '),
                    code.rfind('.'),
                    code.rfind('<'),
                    code.rfind('('))
        completed = code[:index + 1]
        partial = code[index + 1:]

        matches = cql3handling.CqlRuleSet.cql_complete(completed, partial, cassandra_conn=self.cqlshell,
                                                       startsymbol='cqlshCommand')

        if not matches:
            return default

        tokens = code.replace(';', ' ').split()
        if not tokens:
            return default

        return {'matches': sorted(matches), 'cursor_start': cursor_pos - len(partial),
                'cursor_end': cursor_pos, 'metadata': dict(),
                'status': 'ok'}
