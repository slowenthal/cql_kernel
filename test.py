from cql_kernel.kernel import CQLKernel

cqlkernel = CQLKernel.instance()


# foo = cqlkernel.do_execute("select * from system.local xxx;", False)
foo = cqlkernel.cqlshell.onecmd("help;")
foo = cqlkernel.cqlshell.onecmd("select * from system.localsdf;")
foo = cqlkernel.cqlshell.onecmd("describe keyspace retail;")

x = 10



