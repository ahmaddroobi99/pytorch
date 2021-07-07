import torch
import torch.nn.quantized._reference as nnqr
import torch.nn.functional as F

class ConvReLU1d(nnqr.Conv1d):
    _FLOAT_MODULE = torch.nn.intrinsic.ConvReLU1d

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x_dequant = x.dequantize()
        weight_dequant = self._qweight.dequantize()
        float_result = F.conv1d(
            x_dequant, weight_dequant, self._bias, self._conv1d_stride,  # type: ignore[has-type]
            self._conv1d_padding, self._conv1d_dilation, self.groups)  # type: ignore[has-type]
        float_result = F.relu(float_result, inplace=True)
        # NEEDFIX: we don't have dtype in the Linear module APIs right now!
        result = torch.quantize_per_tensor(
            float_result, self.scale, self.zero_point, torch.quint8)
        return result

    def _get_name(self):
        return "QuantizedConvReLU1d(Reference)"


class ConvReLU2d(nnqr.Conv2d):
    _FLOAT_MODULE = torch.nn.intrinsic.ConvReLU2d

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x_dequant = x.dequantize()
        weight_dequant = self._qweight.dequantize()
        float_result = F.conv2d(
            x_dequant, weight_dequant, self._bias, self.stride,
            self.padding, self.dilation, self.groups)
        float_result = F.relu(float_result, inplace=True)
        # NEEDFIX: we don't have dtype in the Linear module APIs right now!
        result = torch.quantize_per_tensor(
            float_result, self.scale, self.zero_point, torch.quint8)
        return result

    def _get_name(self):
        return "QuantizedConvReLU2d(Reference)"

    def to_float(self):
        conv_module = torch.nn.Conv2d(self.in_channels, self.out_channels, self.kernel_size, self.stride, self.padding, self.dilation, self.groups, self._bias is not None, self.padding_mode)        
        conv_module.weight = torch.nn.Parameter(self._qweight.dequantize())
        conv_module.bias = torch.nn.Parameter(self._bias)
        float_module = torch.nn.intrinsic.ConvReLU2d(conv_module, torch.nn.ReLU())
        return float_module

class ConvReLU3d(nnqr.Conv3d):
    _FLOAT_MODULE = torch.nn.intrinsic.ConvReLU3d

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x_dequant = x.dequantize()
        weight_dequant = self._qweight.dequantize()
        float_result = F.conv3d(
            x_dequant, weight_dequant, self._bias, self.stride,
            self.padding, self.dilation, self.groups)
        float_result = F.relu(float_result, inplace=True)
        # NEEDFIX: we don't have dtype in the Linear module APIs right now!
        result = torch.quantize_per_tensor(
            float_result, self.scale, self.zero_point, torch.quint8)
        return result

    def _get_name(self):
        return "QuantizedConvReLU3d(Reference)"
