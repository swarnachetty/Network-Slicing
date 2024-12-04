# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 16:00:36 2024

@author: lzr511
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable

class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            nn.Linear(100, 128),
            nn.LeakyReLU(0.01),
            nn.BatchNorm1d(128),
            nn.Linear(128, 256),
            nn.LeakyReLU(0.01),
            nn.BatchNorm1d(256),
            nn.Linear(256, 512),
            nn.LeakyReLU(0.01),
            nn.BatchNorm1d(512),
            nn.Linear(512, 1024),
            nn.LeakyReLU(0.01),
            nn.Linear(1024, 2),
            nn.Tanh()
        )

    def forward(self, input):
        return self.main(input)

class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.main = nn.Sequential(
            nn.Linear(2, 512),
            nn.LeakyReLU(0.01),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.01),
            nn.Linear(256, 128),
            nn.LeakyReLU(0.01),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, input):
        return self.main(input)

# Create the generator and discriminator networks
generator = Generator()
discriminator = Discriminator()

# Optimizers
optimizer_G = optim.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
optimizer_D = optim.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))

# Loss function
criterion = nn.BCELoss()


import numpy as np

def train(generator, discriminator, epochs, batch_size):
    for epoch in range(epochs):
        # Generate random noise
        noise = Variable(torch.randn(batch_size, 100))
        real_data = Variable(torch.randn(batch_size, 2))  # Simulate real network data
        real_labels = Variable(torch.ones(batch_size, 1))
        fake_labels = Variable(torch.zeros(batch_size, 1))
        
        # Generate fake data from the generator
        fake_data = generator(noise)
        
        # Reset gradients
        optimizer_D.zero_grad()
        
        # Train discriminator on real data
        output_real = discriminator(real_data)
        loss_real = criterion(output_real, real_labels)
        
        # Train discriminator on fake data
        output_fake = discriminator(fake_data.detach())  # detach to avoid training generator now
        loss_fake = criterion(output_fake, fake_labels)
        
        # Backprop and optimize
        loss_D = loss_real + loss_fake
        loss_D.backward()
        optimizer_D.step()
        
        # Train generator
        optimizer_G.zero_grad()
        output = discriminator(fake_data)
        loss_G = criterion(output, real_labels)
        loss_G.backward()
        optimizer_G.step()
        
        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{epochs} | Loss D: {loss_D.item()} | Loss G: {loss_G.item()}")

# Train the model
train(generator, discriminator, epochs=100, batch_size=32)
