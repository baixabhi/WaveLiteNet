import torch.nn as nn
import torch.nn.functional as F

class SEBlock(nn.Module):

    """More efficient Squeeze-and-Excitation block with fewer parameters"""

    def __init__(self, channels, reduction=16):
        super(SEBlock, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        reduced_channels = max(channels // reduction, 8)  # Ensure minimum of 8 channels
        self.fc = nn.Sequential(
            nn.Linear(channels, reduced_channels, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(reduced_channels, channels, bias=False),
            nn.Hardsigmoid(inplace=True)  # Replace sigmoid with hardsigmoid for efficiency
        )


    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y

class InvertedResidual(nn.Module):
    def __init__(self, inp, oup, stride, expand_ratio, use_se=True):
        super(InvertedResidual, self).__init__()
        self.stride = stride
        assert stride in [1, 2]

        hidden_dim = round(inp * expand_ratio)
        self.use_res_connect = self.stride == 1 and inp == oup
        self.use_shortcut_conv = self.stride == 1 and inp != oup

        layers = []
        if expand_ratio != 1:
            layers.extend([
                nn.Conv2d(inp, hidden_dim, 1, 1, 0, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6(inplace=True)
            ])

        layers.extend([
            # Depthwise convolutional
            nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(inplace=True)

        ])

        if use_se:
            layers.append(SEBlock(hidden_dim, reduction=16))
        # Pointwise conv
        layers.extend([
            nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False),
            nn.BatchNorm2d(oup)
        ])

        self.conv = nn.Sequential(*layers)

        # Optional shortcut convolution for channel matching
        if self.use_shortcut_conv:
            self.shortcut = nn.Sequential(
                nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
                nn.BatchNorm2d(oup)
            )

    def forward(self, x):
        if self.use_res_connect:
            return x + self.conv(x)
        elif self.use_shortcut_conv:
            return self.shortcut(x) + self.conv(x)
        else:
            return self.conv(x)

class WMobNetv2(nn.Module):
    def __init__(self, num_classes=4, width_mult=0.75):
        super(WMobNetv2, self).__init__()
        block = InvertedResidual
        input_channel = int(32 * width_mult)  # Reduced initial channels
        last_channel = int(1280 * width_mult)  # Reduced final channels

        # First layer
        self.features = [nn.Sequential(
            nn.Conv2d(3, input_channel, 3, 2, 1, bias=False),
            nn.BatchNorm2d(input_channel),
            nn.ReLU6(inplace=True)
        )]

        # Optimized inverted residual settings
        inverted_residual_setting = [

            # t, c, n, s
            [1, int(16 * width_mult), 1, 1],  # Reduced first block

            [4, int(24 * width_mult), 2, 2],  # Reduced expansion ratio

            [4, int(32 * width_mult), 3, 2],  # Reduced expansion ratio

            [4, int(64 * width_mult), 3, 2],  # Reduced expansion ratio

            [4, int(96 * width_mult), 2, 1],  # Reduced expansion ratio

            [6, int(160 * width_mult), 2, 2],

            [6, int(320 * width_mult), 1, 1],

        ]

        for t, c, n, s in inverted_residual_setting:
            output_channel = c
            for i in range(n):
                stride = s if i == 0 else 1
                self.features.append(block(input_channel, output_channel, stride, expand_ratio=t))
                input_channel = output_channel

        # Last convolution
        self.features.append(nn.Sequential(
            nn.Conv2d(input_channel, last_channel, 1, 1, 0, bias=False),
            nn.BatchNorm2d(last_channel),
            nn.ReLU6(inplace=True)
        ))

        self.features = nn.Sequential(*self.features)

        # Efficient classifier head
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Dropout(0.1),  # Reduced dropout
            nn.Linear(last_channel, num_classes)
        )

        # Initialize weights
        self._initialize_weights()

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
