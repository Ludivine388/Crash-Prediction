# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import torch
import torch.nn as nn
import torch.autograd as autograd
import os
from models import base_model
from models import networks
import sys
import h5py
import os.path
from skimage.io import imsave
from models import hourglass

import torchvision.utils as vutils

class Pix2PixModel(base_model.BaseModel):

    def name(self):
        return 'Pix2PixModel'

    def __init__(self, opt, _isTrain=False):
        self.initialize(opt)

        self.mode = opt.mode

        # single_view -> num_input =3
        # two_view -> num_input = 6
        # two_view_k -> num_input = 7,
        # help = "single_view", "two_view" (no human keypoints), two_view_k" (with human keypoints)'
        self.num_input = 3

        if self.mode == 'Ours_Bilinear':
            print(
                '===================================  DIW NETWORK TRAIN FROM %s==================================='
                % self.mode)

            new_model = hourglass.HourglassModel(self.num_input)

            print(
                '=================================== Loading Pretrained Model OURS ==================================='
            )

            if not _isTrain:
                model_parameters = self.load_network(
                    new_model, 'G', 'best_depth_Ours_Bilinear_inc_3')

                new_model.load_state_dict(model_parameters)

            new_model = torch.nn.parallel.DataParallel(
                new_model.cuda(), device_ids=range(torch.cuda.device_count()))

            self.netG = new_model

        else:
            print('ONLY SUPPORT Ours_Bilinear')
            sys.exit()

        self.old_lr = opt.lr
        self.netG.train()

        if True:
            self.criterion_joint = networks.JointLoss(opt)
            # initialize optimizers
            self.optimizer_G = torch.optim.Adam(
                self.netG.parameters(), lr=opt.lr, betas=(0.9, 0.999))
            self.scheduler = networks.get_scheduler(self.optimizer_G, opt)
            print('---------- Networks initialized -------------')
            networks.print_network(self.netG)
            print('-----------------------------------------------')

    def set_writer(self, writer):
        self.writer = writer

    def set_input(self, stack_imgs, targets):
        self.input = stack_imgs
        self.targets = targets

    def forward(self):

        # run first network
        self.input_images = autograd.Variable(self.input.cuda(), requires_grad=False)
        human_mask = 1.0 - autograd.Variable(
            self.targets['env_mask'].cuda(), requires_grad=False).unsqueeze(1)
        keypoints_img = autograd.Variable(
            self.targets['keypoints_img'].cuda(), requires_grad=False).unsqueeze(1)

        # stack inputs
        stack_inputs = None

        stack_inputs = self.input_images

        self.prediction_d, self.pred_confidence = self.netG.forward(
            stack_inputs)
        self.prediction_d = self.prediction_d.squeeze(1)
        self.pred_confidence = self.pred_confidence.squeeze(1)

    def get_image_paths(self):
        return self.image_paths

    # logging 
    def write_summary(self,
                      mode_name,
                      input_images,
                      prediction_d,
                      pred_confidence,
                      targets,
                      n_iter,
                      loss=None):

        invere_depth_pred = torch.exp(-prediction_d.data.cpu()).unsqueeze(1).repeat(
            1, 3, 1, 1)

        invere_depth_gt = 1.0 / \
            targets['depth_gt'].unsqueeze(1).repeat(1, 3, 1, 1)
        gt_mask = targets['gt_mask'].unsqueeze(1).repeat(1, 3, 1, 1)

        invere_depth_gt = invere_depth_gt * gt_mask
        min_depth, max_depth = np.percentile(
            invere_depth_pred.numpy(), [1, 99])
        invere_depth_pred[invere_depth_pred > max_depth] = 0.0
        invere_depth_pred[invere_depth_pred < min_depth] = 0.0

        inv_depth_mask = invere_depth_pred * gt_mask

        human_mask = 1.0 - targets['env_mask'].unsqueeze(1).repeat(1, 3, 1, 1)
        input_confidence = targets['input_confidence'].unsqueeze(1).repeat(
            1, 3, 1, 1)
        pred_confidence_saved = pred_confidence.data.unsqueeze(
            1).repeat(1, 3, 1, 1)

        if loss:
            self.writer.add_scalar(mode_name + '/loss', loss, n_iter)

        self.writer.add_image(
            mode_name + '/image',
            vutils.make_grid(
                input_images[:8, :, :, :].data.cpu(), normalize=True),
            n_iter)
        self.writer.add_image(
            mode_name + '/pred_full',
            vutils.make_grid(invere_depth_pred[:8, :, :, :], normalize=True),
            n_iter)
        self.writer.add_image(
            mode_name + '/pred_mask',
            vutils.make_grid(inv_depth_mask[:8, :, :, :], normalize=True), n_iter)
        self.writer.add_image(
            mode_name + '/pred_confidence',
            vutils.make_grid(
                pred_confidence_saved[:8, :, :, :], normalize=True),
            n_iter)

        self.writer.add_image(
            mode_name + '/gt_depth',
            vutils.make_grid(invere_depth_gt[:8, :, :, :], normalize=True), n_iter)
        self.writer.add_image(
            mode_name + '/gt_mask',
            vutils.make_grid(gt_mask[:8, :, :, :], normalize=True), n_iter)

        self.writer.add_image(
            mode_name + '/human_mask',
            vutils.make_grid(human_mask[:8, :, :, :], normalize=True), n_iter)
        self.writer.add_image(
            mode_name + '/input_confidence',
            vutils.make_grid(input_confidence[:8, :, :, :], normalize=True), n_iter)

    def backward_G(self, n_iter):
        # Combined loss
        self.loss_joint = self.criterion_joint(self.input_images, self.prediction_d,
                                               self.pred_confidence, self.targets)
        print('Train loss is %f ' % self.loss_joint)

        # add to tensorboard
        if n_iter % 100 == 0:
            self.write_summary('Train', self.input_images, self.prediction_d,
                               self.pred_confidence, self.targets, n_iter,
                               self.loss_joint)

        self.loss_joint_var = self.criterion_joint.get_loss_var()
        self.loss_joint_var.backward()

    def optimize_parameters(self, n_iter):
        self.forward()
        self.optimizer_G.zero_grad()
        self.backward_G(n_iter)
        self.optimizer_G.step()

    def run_and_save(self, input_, targets, save_path):
        assert (self.num_input == 3)
        input_imgs = autograd.Variable(input_.cuda(), requires_grad=False)

        stack_inputs = input_imgs

        prediction_d, pred_confidence = self.netG.forward(stack_inputs)
        pred_log_d = prediction_d.squeeze(1)
        pred_d = torch.exp(pred_log_d)

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        for i in range(0, len(targets['img_1_path'])):

            dir = save_path + targets['img_1_path'][i].split('/')[-2]

            if not os.path.exists(dir):
                os.makedirs(dir)

            saved_img = np.transpose(
                input_imgs[i, :, :, :].cpu().numpy(), (1, 2, 0))

            pred_d_ref = pred_d.data[i, :, :].cpu().numpy()

            output_path = dir + '/' + \
                targets['img_1_path'][i].split('/')[-1]
            print(output_path)
            disparity = 1. / pred_d_ref
            disparity = disparity / np.max(disparity)
            disparity = np.tile(np.expand_dims(disparity, axis=-1), (1, 1, 3))
            saved_imgs = np.concatenate((saved_img, disparity), axis=1)
            saved_imgs = (saved_imgs*255).astype(np.uint8)

            imsave(output_path, saved_imgs)

    def switch_to_eval(self):
        self.netG.eval()

    def save(self, label):
        self.save_network(self.netG, 'G', label, self.gpu_ids)

    def update_learning_rate(self):
        self.scheduler.step()
        lr = self.optimizer_G.param_groups[0]['lr']
        print('Current learning rate = %.7f' % lr)
