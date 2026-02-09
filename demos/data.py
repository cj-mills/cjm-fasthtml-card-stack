"""Sample data for card stack demos."""

SAMPLE_ITEMS = [
    "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
    "The core idea is to feed data into an algorithm, let it find patterns, and then use those patterns to make predictions or decisions on new, unseen data.",
    "There are three main paradigms: supervised learning, unsupervised learning, and reinforcement learning. Each addresses a fundamentally different type of problem.",
    "In supervised learning, the algorithm is trained on labeled examples — input-output pairs where the correct answer is known. The goal is to learn a mapping from inputs to outputs.",
    "Classification and regression are the two primary supervised learning tasks. Classification predicts discrete categories, while regression predicts continuous numerical values.",
    "Common supervised algorithms include linear regression, logistic regression, decision trees, random forests, support vector machines, and neural networks.",
    "Unsupervised learning works with unlabeled data. The algorithm must discover hidden structure, groupings, or patterns without any guidance about what the correct output should be.",
    "Clustering is the most common unsupervised task — grouping similar data points together. K-means, DBSCAN, and hierarchical clustering are widely used approaches.",
    "Dimensionality reduction is another key unsupervised technique. Methods like PCA and t-SNE compress high-dimensional data into fewer dimensions while preserving important structure.",
    "Reinforcement learning trains an agent to make sequences of decisions by interacting with an environment. The agent receives rewards or penalties and learns to maximize cumulative reward.",
    "The training process in supervised learning involves minimizing a loss function — a measure of how far the model's predictions are from the true values.",
    "Gradient descent is the optimization algorithm most commonly used to minimize the loss. It iteratively adjusts model parameters in the direction that reduces the error.",
    "Overfitting occurs when a model learns the training data too well, including its noise and outliers, and performs poorly on new data. It is one of the central challenges in machine learning.",
    "Regularization techniques like L1, L2, and dropout help prevent overfitting by adding constraints that discourage overly complex models.",
    "The bias-variance tradeoff is a fundamental concept. High bias means the model is too simple and underfits; high variance means it is too complex and overfits.",
    "Cross-validation is a technique for evaluating model performance by splitting data into multiple train-test folds, reducing the risk of evaluation bias from a single split.",
    "Feature engineering — the process of creating, selecting, and transforming input variables — often has more impact on model performance than the choice of algorithm.",
    "Neural networks are composed of layers of interconnected nodes. Each connection has a learnable weight, and each node applies a nonlinear activation function to its inputs.",
    "Deep learning refers to neural networks with many layers. These architectures can automatically learn hierarchical feature representations from raw data.",
    "Convolutional neural networks (CNNs) are specialized for grid-like data such as images. They use learnable filters that detect local patterns like edges, textures, and shapes.",
    "Recurrent neural networks (RNNs) and their variants like LSTMs are designed for sequential data. They maintain hidden state that carries information across time steps.",
    "Transformers replaced RNNs for most sequence tasks by using self-attention mechanisms that can relate any position in a sequence to any other position in parallel.",
    "Large language models like GPT and Claude are transformer-based models trained on massive text corpora. They learn to predict the next token and develop broad language understanding.",
    "Transfer learning allows a model pretrained on a large dataset to be fine-tuned on a smaller, task-specific dataset. This dramatically reduces the data and compute needed for new tasks.",
    "The field continues to evolve rapidly, with active research in areas like multimodal learning, efficient architectures, alignment, interpretability, and learning from human feedback.",
]

# Simulated VAD (Voice Activity Detection) audio chunks with timestamps
# Format: (start_seconds, end_seconds, label)
SAMPLE_AUDIO_CHUNKS = [
    (0.0, 3.2, "Speech detected"),
    (3.8, 7.1, "Speech detected"),
    (7.5, 12.4, "Speech detected"),
    (13.0, 15.8, "Speech detected"),
    (16.2, 21.5, "Speech detected"),
    (22.0, 26.3, "Speech detected"),
    (27.1, 31.9, "Speech detected"),
    (32.5, 38.2, "Speech detected"),
    (39.0, 44.7, "Speech detected"),
    (45.3, 50.1, "Speech detected"),
    (51.0, 56.8, "Speech detected"),
    (57.5, 62.3, "Speech detected"),
    (63.0, 68.9, "Speech detected"),
    (69.5, 75.2, "Speech detected"),
    (76.0, 81.4, "Speech detected"),
]
