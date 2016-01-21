from cql_kernel.kernel import CQLKernel

cqlkernel = CQLKernel.instance()


# foo = cqlkernel.do_execute("select * from system.local xxx;", False)
foo = cqlkernel.do_execute("select * from system.local;", False)
foo = cqlkernel.do_execute("describe keyspace retail;", False)

foo = cqlkernel.cqlshell.onecmd("describe keyspace retail;")
foo = cqlkernel.cqlshell.onecmd("select * from system.local;")

x = 10



