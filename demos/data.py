"""Sample data for card stack demos."""

# Items with a mix of normal and very long text to test overflow scrolling.
# Item 3 (index 2) and item 8 (index 7) are intentionally oversized to
# exceed a typical card stack viewport height.
OVERFLOW_ITEMS = [
    "This is a normal-length item that fits comfortably in the card stack viewport without any overflow issues.",
    "Another standard item. The card stack should display this alongside context cards above and below.",
    # Intentionally very long — simulates a poorly-split transcript segment or
    # a user merging many segments into one massive block.
    (
        "This is an oversized segment that simulates what happens when NLTK fails to split "
        "properly due to lack of punctuation in the source transcript text or when the user "
        "merges many text segments into a single large card. "
        "The quick brown fox jumps over the lazy dog near the riverbank where the willows sway "
        "gently in the afternoon breeze and the sunlight filters through the canopy creating "
        "dappled patterns on the mossy ground below. "
        "Meanwhile the birds sing their evening songs as the temperature begins to drop and the "
        "shadows lengthen across the meadow stretching toward the old stone wall that marks the "
        "boundary of the ancient estate. "
        "The groundskeeper walks slowly along the gravel path checking each gate and fence post "
        "making sure everything is secure before nightfall when the deer come down from the hills "
        "to graze on the tender grass that grows in the sheltered valley. "
        "In the distance the church bell rings marking the hour and the sound carries across the "
        "still air reaching the farmhouses scattered along the ridge where families are gathering "
        "for their evening meals around wooden tables worn smooth by generations of daily use. "
        "The old clock on the mantelpiece ticks steadily marking each second with mechanical "
        "precision as the fire crackles in the hearth sending sparks up the chimney into the "
        "darkening sky above. "
        "Tomorrow will bring new challenges and opportunities but for now the world is at peace "
        "and the gentle rhythm of rural life continues as it has for centuries in this quiet "
        "corner of the countryside where time seems to move at its own unhurried pace. "
        "The farmer checks his almanac noting the phases of the moon and the predicted weather "
        "patterns for the coming week planning his work accordingly because the harvest waits "
        "for no one and the grain must be brought in before the autumn rains begin. "
        "His wife tends the kitchen garden pulling weeds and checking the ripeness of the "
        "tomatoes that hang heavy on their vines supported by wooden stakes driven into the "
        "rich dark soil that has been cultivated by this family for five generations. "
        "Their children play in the orchard climbing apple trees and building forts from fallen "
        "branches while the family dog watches patiently from the porch occasionally barking at "
        "a passing rabbit or squirrel that ventures too close to the vegetable patch."
    ),
    "Back to normal length. This item follows the oversized one to verify context cards still render properly after scrolling.",
    "Standard item number five. The card stack should handle the transition between normal and oversized items smoothly.",
    "Another regular item. Navigation should work identically for normal-sized cards — arrow keys, scroll wheel, click-to-focus.",
    "Item seven is also normal length. The auto-adjust system should still calculate the correct visible count for these items.",
    # Second oversized item — tests that overflow works at different positions in the list
    (
        "Here is another intentionally oversized segment placed later in the list to verify that "
        "the overflow scrolling behavior works regardless of the item's position in the dataset. "
        "The card stack must handle this gracefully whether the user arrives here by navigating "
        "down from the top or up from the bottom or by clicking directly on this card. "
        "When machine learning models process natural language they must handle sequences of "
        "varying lengths and the challenge of maintaining context across long passages of text "
        "is one of the fundamental problems in computational linguistics that researchers have "
        "been working to solve for decades using increasingly sophisticated architectures. "
        "The transformer architecture introduced the self-attention mechanism which allows the "
        "model to weigh the importance of different parts of the input sequence when producing "
        "each element of the output enabling much longer effective context windows than were "
        "possible with recurrent neural networks that processed tokens sequentially. "
        "Training these models requires enormous computational resources including thousands "
        "of GPUs running for weeks or months on datasets containing billions of tokens of text "
        "scraped from the internet and curated to remove harmful or low-quality content. "
        "The resulting models can generate remarkably fluent and coherent text that is often "
        "indistinguishable from human writing though they still struggle with factual accuracy "
        "mathematical reasoning and maintaining consistency across very long documents. "
        "Fine-tuning these foundation models on specific tasks using smaller curated datasets "
        "and techniques like reinforcement learning from human feedback has proven to be an "
        "effective way to align model behavior with human preferences and values. "
        "The rapid pace of progress in this field has raised important questions about the "
        "societal implications of increasingly capable AI systems and the need for thoughtful "
        "governance frameworks that balance innovation with safety and fairness."
    ),
    "Item nine is back to normal. This verifies that navigating past the second oversized item works correctly.",
    "The tenth and final item. All navigation patterns — keyboard arrows, page up/down, first/last — should work across the full list including oversized items.",
]

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
