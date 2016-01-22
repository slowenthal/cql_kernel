from cql_kernel.kernel import CQLKernel
from cqlshlib.cql3handling import CqlRuleSet

cqlkernel = CQLKernel.instance()



# foo = cqlkernel.do_execute("select * from system.local xxx;", False)
foo = CqlRuleSet.cql_complete("CREATE", "", cassandra_conn=cqlkernel,
                                           startsymbol='cqlshCommand')

foo = cqlkernel.cqlshell.onecmd("consistency quorum;")
foo = cqlkernel.cqlshell.onecmd("help;")
foo = cqlkernel.cqlshell.onecmd("select * from system.localsdf;")
foo = cqlkernel.cqlshell.onecmd("describe keyspace retail;")

x = 10



