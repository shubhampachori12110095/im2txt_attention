# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Model wrapper class for performing inference with a ShowAndTellModel."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function



from im2txt import show_and_tell_model
from im2txt.inference_utils import inference_wrapper_base


class InferenceWrapper(inference_wrapper_base.InferenceWrapperBase):
  """Model wrapper class for performing inference with a ShowAndTellModel."""

  def __init__(self):
    super(InferenceWrapper, self).__init__()

  def build_model(self, model_config):
    model = show_and_tell_model.ShowAndTellModel(model_config, mode="inference")
    model.build()
    return model

  def feed_image(self, sess, encoded_image):
    initial_state,image_embedding = sess.run(fetches=["lstm/initial_state:0","lstm/image_embedding_print:0"],
                             feed_dict={"image_feed:0": encoded_image})
    #print("image embedding")
    #print(image_embedding)
    return initial_state

  def inference_step(self, sess, input_feed, state_feed,encoded_image):
    softmax_output, state_output,alpha_ti,alpha_ti_diff,z_i,word_imbeddings = sess.run(
        fetches=["softmax:0", "lstm/state:0","lstm/alpha_ti:0","lstm/alpha_ti_diff:0","lstm/z_i:0","lstm/word_imbeddings:0"],
        feed_dict={
            "input_feed:0": input_feed,
            "lstm/state_feed:0": state_feed,
            "image_feed:0": encoded_image
        })
    
    # print("print lstm inner variables!")
    # print("state_out_put")
    # print(state_output)
    # print("alpha_ti")
    # print(alpha_ti)
    '''
    print("alpha_ti_diff")
    print(alpha_ti_diff)
    print("z_i")
    print(z_i)
    print("word_imbeddings")
    print(word_imbeddings)
    '''
    return softmax_output, state_output, None
