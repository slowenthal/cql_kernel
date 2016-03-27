import sys
from cql_kernel.kernel import CQLKernel
from cqlshlib_cql_kernel.cql3handling import CqlRuleSet

cqlkernel = CQLKernel.instance()

def cutcode(code):
    index = code.rfind(' ')
    completed = code[:index+1]
    partial = code[index+1:]

    print 'completed: "%s"' % completed
    print 'partial:   "%s"' % partial

    completions = CqlRuleSet.cql_complete(completed, partial, cassandra_conn=cqlkernel,
                                  startsymbol='cqlshCommand')
    print completions



cutcode("create")
cutcode("create ")
cutcode("create t")

# foo = cqlkernel.do_execute("select * from system.local xxx;", False)
foo = CqlRuleSet.cql_complete("CREATE", "", cassandra_conn=cqlkernel,
                                           startsymbol='cqlshCommand')

print foo
foo = CqlRuleSet.cql_complete("CREATE ", "T", cassandra_conn=cqlkernel,
                                           startsymbol='cqlshCommand')

print foo
foo = CqlRuleSet.cql_complete( "USE", "", cassandra_conn=cqlkernel,
                              startsymbol='cqlshCommand')


print foo

foo = CqlRuleSet.cql_complete( "", "CREATE", cassandra_conn=cqlkernel,
                              startsymbol='cqlshCommand')

print foo
foo = CqlRuleSet.cql_complete( "CREATE ", "", cassandra_conn=cqlkernel,
                              startsymbol='cqlshCommand')


print foo

foo = cqlkernel.cqlshell.onecmd("consistency quorum;")
foo = cqlkernel.cqlshell.onecmd("help;")
cqlkernel.cqlshell.query_out = sys.stdout

foo = cqlkernel.cqlshell.onecmd("select * from system.local;")
foo = cqlkernel.cqlshell.onecmd("describe keyspace retail;")

x = 10



