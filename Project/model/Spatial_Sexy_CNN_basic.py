"""
CNN with 3 conv layers and a fully connected classification layer
"""
import torch
import torch.nn as nn


class Spatial_Sexy_CNN_Basic(nn.Module):
    """
    :var conv1   : torch.nn.Conv2d
    :var conv2   : torch.nn.Conv2d
    :var conv3   : torch.nn.Conv2d
        The first three convolutional layers of the network

    :var fc      : torch.nn.Linear
        Final fully connected layer
    """

    def __init__(self, num_classes):
        """
        :param num_classes: the number of classes in the dataset
        """
        super(Spatial_Sexy_CNN_Basic, self).__init__()
        # First layer
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 24, kernel_size=7, stride=1),
            nn.Softsign()
        )
        # Second layer
        self.conv2 = nn.Sequential(
            nn.Conv2d(24, 48, kernel_size=4, stride=2),
            nn.Softsign()
        )
        # Polling layer
        self.pool1 = nn.AvgPool2d(3)
        self.alpha = nn.Parameter(torch.ones(1, 1, 4, 4))
        self.upscale = nn.Upsample(scale_factor=3)

        # Third layer
        self.conv3 = nn.Sequential(
            nn.Conv2d(48, 72, kernel_size=3, stride=1),
            nn.Softsign()
        )

        # Classification layer
        self.fc = nn.Sequential(
            nn.Linear(288, num_classes)
        )

    def forward(self, x):
        """
        Computes forward pass on the network
        :param x: torch.Tensor
            The input to the model
        :return: torch.Tensor
            Activations of the fully connected layer
        """
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.pool1((self.upscale(self.alpha).mul(x)).exp()).log().mul(self.alpha.pow(-1))
        x = self.conv3(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x
