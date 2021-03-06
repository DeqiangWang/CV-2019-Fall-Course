import torch.nn as nn
from torch.autograd import Function
from torch.autograd.function import once_differentiable

from maskrcnn_benchmark import _C


class _RIE_Cuda_ForwardBackward(Function):
    @staticmethod
    def forward(ctx, input, nOrientation):
        ctx.save_for_backward(input)
        ctx.nOrientation = nOrientation
        output, mainDirection = _C.rie_alignfeature_forward(input, nOrientation)
        ctx.mainDirection = mainDirection
        return output

    @staticmethod
    @once_differentiable
    def backward(ctx, grad_output):
        nOrientation = ctx.nOrientation
        mainDirection = ctx.mainDirection

        grad_input = _C.rie_alignfeature_backward(grad_output, mainDirection, nOrientation)
        return grad_input, None, None


class ORAlign2d(nn.Module):
    def __init__(self, nOrientation=8):
        super(ORAlign2d, self).__init__()

    def forward(self, input, nOrientation):
        return _RIE_Cuda_ForwardBackward.apply(input, nOrientation)
