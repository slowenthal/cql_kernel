from cql_kernel.kernel import CQLKernel

cqlkernel = CQLKernel.instance()


foo = cqlkernel.do_execute("select * from system.local xxx;", False)

x = 10



