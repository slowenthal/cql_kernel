from ipykernel.kernelapp import IPKernelApp
from .kernel import CQLKernel
IPKernelApp.launch_instance(kernel_class=CQLKernel)
