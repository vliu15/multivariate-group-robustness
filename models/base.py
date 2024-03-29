from abc import abstractmethod

import torch.nn as nn


class ClassificationModel(nn.Module):
    """Abstract model that handles forward i/o for classification models"""

    def supervised_step(self, batch, subgroup=False, first_batch_loss=None):
        _, x, y, g, w = batch
        if not subgroup:
            loss_dict, metrics_dict = self.forward(x, y, w, first_batch_loss)
        else:
            loss_dict, metrics_dict = self.forward_subgroup(x, y, g, w, first_batch_loss)
        return loss_dict, metrics_dict

    @abstractmethod
    def forward_subgroup(self, x, y, g, w, first_batch_loss):
        pass

    @abstractmethod
    def predict(self, x):
        pass

    def inference_step(self, batch):
        _, x, y, _, _ = batch
        yh = self.predict(x)
        return {"y": y, "yh": yh}
