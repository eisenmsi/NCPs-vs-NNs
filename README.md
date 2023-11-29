# NCPs vs. NNs

This repository provides a comparative analysis between Neural Circuit Policies (NCPs) and classical neural networks (NNs). The scripts included here enable users to execute experiments to observe the performance and computational time required for different models. Specifically, it contains experiments related to predicting sine values and behavior cloning in an Atari game environment.

## Overview

Neural Circuit Policies (NCPs) represent a novel approach to machine learning, differing significantly from classical neural networks (NNs). This repository aims to offer a side-by-side comparison of these two paradigms, showcasing their strengths and weaknesses in specific tasks.

## Experiments

### 1. Sine Value Prediction

The repository contains scripts to train and evaluate both NCPs and NNs on the task of predicting sine values. Users can execute these scripts and compare the performance metrics, such as accuracy and computational time, between the two approaches.

#### Running Sine Value Prediction Experiment

To execute the sine value prediction experiment, follow these steps:

1. Install dependencies using [Poetry](https://python-poetry.org/):

    ```bash
    poetry install
    ```

2. Run the experiment (for example):

    ```bash
    python LTC_sine.py
    ```

### 2. Atari Game Behavior Cloning

Another experiment involves behavior cloning in an Atari game environment, illustrating the differences in performance and training efficiency between NCPs and NNs.

#### Running Atari Game Behavior Cloning Experiment

To execute the behavior cloning experiment, follow these steps:

1. Install dependencies using [Poetry](https://python-poetry.org/):

    ```bash
    poetry install
    ```

2. Run the experiment (for example):

    ```bash
    python LTC_Atari.py
    ```

## Speed Comparison

In the conducted experiments, classical neural networks (NNs) showed faster computational times compared to Neural Circuit Policies (NCPs). This observation might vary based on the specific models, datasets, and hardware configurations.

## Installation

Ensure you have Poetry installed on your system. You can install the required libraries by running:

```bash
poetry install
```

## Dependencies

This project uses Poetry as a package manager.

## Contributions

Contributions to this repository are welcome! If you find any issues or want to improve the comparison between NCPs and NNs, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License.
