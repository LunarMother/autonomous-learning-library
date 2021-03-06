from torch.optim import Adam
from all.agents import VPG
from all.approximation import VNetwork, FeatureNetwork
from all.logging import DummyWriter
from all.policies import SoftmaxPolicy
from .models import fc_relu_features, fc_policy_head, fc_value_head


def vpg(
        # Common settings
        device="cpu",
        discount_factor=0.99,
        # Adam optimizer settings
        lr=5e-3,
        # Batch settings
        min_batch_size=500,
):
    """
    Vanilla Policy Gradient classic control preset.

    Args:
        device (str): The device to load parameters and buffers onto for this agent.
        discount_factor (float): Discount factor for future rewards.
        last_frame (int): Number of frames to train.
        lr (float): Learning rate for the Adam optimizer.
        min_batch_size (int): Continue running complete episodes until at least this many
            states have been seen since the last update.
    """
    def _vpg(env, writer=DummyWriter()):
        feature_model = fc_relu_features(env).to(device)
        value_model = fc_value_head().to(device)
        policy_model = fc_policy_head(env).to(device)

        feature_optimizer = Adam(feature_model.parameters(), lr=lr)
        value_optimizer = Adam(value_model.parameters(), lr=lr)
        policy_optimizer = Adam(policy_model.parameters(), lr=lr)

        features = FeatureNetwork(
            feature_model,
            feature_optimizer,
            writer=writer
        )
        v = VNetwork(
            value_model,
            value_optimizer,
            writer=writer
        )
        policy = SoftmaxPolicy(
            policy_model,
            policy_optimizer,
            writer=writer
        )
        return VPG(features, v, policy, discount_factor=discount_factor, min_batch_size=min_batch_size)
    return _vpg


__all__ = ["vpg"]
