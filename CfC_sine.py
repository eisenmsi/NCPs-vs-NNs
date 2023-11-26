import numpy as np
import torch
import torch.nn as nn
import torch.utils.data as data
import pytorch_lightning as pl
from ncps.wirings import AutoNCP
from ncps.torch import CfC
import matplotlib.pyplot as plt
import seaborn as sns
from pytorch_lightning.loggers import WandbLogger
import time


def generate_sine_data(N):
    data_x = np.stack(
        [np.sin(np.linspace(0, 3 * np.pi, N)), np.cos(np.linspace(0, 3 * np.pi, N))],
        axis=1,
    )
    data_x = np.expand_dims(data_x, axis=0).astype(np.float32)
    # Target output is a sine with double the frequency of the input signal
    data_y = np.sin(np.linspace(0, 6 * np.pi, N)).reshape([1, N, 1]).astype(np.float32)
    return data_x, data_y


if __name__ == "__main__":
    N = 48  # Length of the time-series
    out_features = 1
    in_features = 2

    # Input feature is a sine and a cosine wave
    data_x, data_y = generate_sine_data(N)
    print("data_x.shape:", str(data_x.shape))
    print("data_y.shape:", str(data_y.shape))

    data_x = torch.Tensor(data_x)
    data_y = torch.Tensor(data_y)
    dataloader = data.DataLoader(
        data.TensorDataset(data_x, data_y), batch_size=1, shuffle=True, num_workers=4
    )

    # Let's visualize the training data
    sns.set()
    plt.figure(figsize=(6, 4))
    plt.plot(data_x[0, :, 0], label="Input feature 1")
    plt.plot(data_x[0, :, 1], label="Input feature 1")
    plt.plot(data_y[0, :, 0], label="Target output")
    plt.ylim((-1, 1))
    plt.title("Training data")
    plt.legend(loc="upper right")
    plt.show()

    # LightningModule for training a RNNSequence module
    class SequenceLearner(pl.LightningModule):
        def __init__(self, model, lr=0.005):
            super().__init__()
            self.model = model
            self.lr = lr

        def training_step(self, batch, batch_idx):
            x, y = batch
            y_hat, _ = self.model.forward(x)
            y_hat = y_hat.view_as(y)
            loss = nn.MSELoss()(y_hat, y)
            self.log("train_loss", loss, prog_bar=True)
            return {"loss": loss}

        def validation_step(self, batch, batch_idx):
            x, y = batch
            y_hat, _ = self.model.forward(x)
            y_hat = y_hat.view_as(y)
            loss = nn.MSELoss()(y_hat, y)

            self.log("val_loss", loss, prog_bar=True)
            return loss

        def test_step(self, batch, batch_idx):
            # Here we just reuse the validation_step for testing
            return self.validation_step(batch, batch_idx)

        def configure_optimizers(self):
            return torch.optim.Adam(self.model.parameters(), lr=self.lr)

    wiring = AutoNCP(16, out_features)  # 16 units, 1 motor neuron

    CfC_model = CfC(in_features, wiring, batch_first=True)
    learn = SequenceLearner(CfC_model, lr=0.01)
    wandb_logger = WandbLogger(log_model="all", project="CfC_sine")
    trainer = pl.Trainer(
        logger=wandb_logger,
        log_every_n_steps=1,
        max_epochs=400,
        gradient_clip_val=1,  # Clip gradient to stabilize training
    )

    # Let's visualize how CfC initialy performs before the training
    sns.set()
    with torch.no_grad():
        prediction = CfC_model(data_x)[0].numpy()
    plt.figure(figsize=(6, 4))
    plt.plot(data_y[0, :, 0], label="Target output")
    plt.plot(prediction[0, :, 0], label="NCP output")
    plt.ylim((-1, 1))
    plt.title("Before training")
    plt.legend(loc="upper right")
    plt.show()

    start = time.process_time()
    start_2 = time.time()

    # Train the model for 400 epochs (= training steps)
    trainer.fit(learn, dataloader)

    end = time.process_time()
    end_2 = time.time()

    print("Process time: " + str(end - start) + " s")
    print("Wall-clock time: " + str(end_2 - start_2) + " s")

    # How does the trained model now fit to the sinusoidal function?
    sns.set()
    with torch.no_grad():
        prediction = CfC_model(data_x)[0].numpy()
    plt.figure(figsize=(6, 4))
    plt.plot(data_y[0, :, 0], label="Target output")
    plt.plot(prediction[0, :, 0], label="NCP output")
    plt.ylim((-1, 1))
    plt.title("After training")
    plt.legend(loc="upper right")
    plt.show()
