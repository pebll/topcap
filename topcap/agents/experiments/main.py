import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# Mock data: same as above
episodes = [
    # ([[state1], [f21, f22, f23]], [reward1, reward2])
    ([[0.8, 0.5, 0.2], [0.6, 0.7, 0.1], [0.3, 0.9, 0.4]], [1, 2, 3]),
    ([[0.5, 0.4, 0.6], [0.7, 0.3, 0.2]], [2, 1]),
    ([[0.9, 0.1, 0.3], [0.4, 0.6, 0.5], [0.2, 0.8, 0.7]], [1, 1, 2]),
]
episodes.extend(episodes)
episodes.extend(episodes)

# Initialize weights randomly

def v_function(features, weights):
    """V(s) = w · f(s)"""
    return np.dot(features, weights)

def grad_v_function(features, weights):
    """V(s) = f(s)"""
    return features

# Training
def train_custom():
    w = np.random.randn(3)
    print(f"Initial weights: {w}")
    alpha = 0.1  # learning rate
    gamma = 0.9  # discount factor
    for training_step, (episode_states, episode_rewards) in enumerate(episodes):
        # Compute returns (Monte Carlo)
        print(f"Training step: {training_step+1}")
        returns = []
        G = 0
        for r in reversed(episode_rewards):
            G = r + gamma * G
            returns.insert(0, G)
        print(f"Rewards: {episode_rewards}")
        print(f"Returns: {returns}")
        
        # Update weights for each state-return pair
        total_loss = 0
        for state, G_target in zip(episode_states, returns):
            state = np.array(state)
            
            # Prediction
            v_pred = v_function(state, w)
            
            # Error
            error = (G_target - v_pred)
            
            # Gradient descent: w ← w + α * error * features
            w = w + alpha * error * grad_v_function(state, w)
            
            total_loss += error**2
        
        print(f"Loss: {total_loss / len(episode_states):.4f}")

# Test prediction
    test_state = np.array([0.8, 0.5, 0.2])
    print(f"\nV(test_state) = {v_function(test_state, w):.4f}")
    print(f"Learned weights: {w}")

def train_torch():
# V-Function: linear with 3 features
    v_net = nn.Linear(3, 1, bias=False)
    optimizer = optim.SGD(v_net.parameters(), lr=0.1)
    loss_fn = nn.MSELoss()

    gamma = 0.9  # discount factor

# Training
    for episode_states, episode_rewards in episodes:
        # Compute returns (Monte Carlo)
        returns = []
        G = 0
        for r in reversed(episode_rewards):
            G = r + gamma * G
            returns.insert(0, G)

        # Convert to tensors
        states_tensor = torch.tensor(episode_states, dtype=torch.float32)
        returns_tensor = torch.tensor(returns, dtype=torch.float32).unsqueeze(1)

        # Forward pass
        predictions = v_net(states_tensor)

        # Loss and backprop
        loss = loss_fn(predictions, returns_tensor)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Loss: {loss.item():.4f}")

# Test prediction
    test_state = torch.tensor([[0.8, 0.5, 0.2]], dtype=torch.float32)
    print(f"\nV(test_state) = {v_net(test_state).item():.4f}")
    w = v_net.weight
    print(f"Learned weights: {w}")

train_custom()
print(f"TORCH:")
print()
train_torch()



