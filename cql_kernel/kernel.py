import StringIO
import codecs
import os

from ipykernel.kernelbase import Kernel

import sys
from cql_kernel import cqlsh
from cqlshlib_cql_kernel import cql3handling


from cql_kernel.cqlsh import Shell
import re

__version__ = '0.2'

version_pat = re.compile(r'version (\d+(\.\d+)+)')

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
        self.hostname = os.environ.get('CASSANDRA_HOSTNAME','localhost')
        self._start_cql()


    def _start_cql(self):
        # c = Cluster([self.hostname])
        # self.cqlshell = Shell("127.0.0.1", 9042, use_conn = c )
        self.cqlshell = Shell(self.hostname, 9042, encoding="utf-8")
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


        # Very very cheal HTML magic
        if cleanCode[:6].upper() == "%%HTML":
            outputStr = cleanCode[6:].strip()
        else:
            # This is a regular query
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
            outputStr = self.outStringWriter.getvalue().strip()

        if not silent:


            #Format desc commands with codemirror (cool feature)

            if code.strip()[:4] == 'desc':
                outputStr = '<script>var x = CodeMirror.fromTextArea(document.getElementById("desc%d"), {readOnly: true, mode:"text/x-cassandra"} )</script><textarea id="desc%d">%s</textarea>' % (self.execution_count, self.execution_count,outputStr)

            # CQL rows come back as HTML

            if outputStr[:1] == '<':
                mime_type = 'text/html'
            else:
                mime_type = 'text/plain'

            stream_content = {'execution_count': self.execution_count, 'data': {mime_type: outputStr}}

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
        completed = code[:index+1]
        partial = code[index+1:]

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


