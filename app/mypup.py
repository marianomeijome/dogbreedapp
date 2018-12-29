from fastai.conv_learner import *

arch=resnext101_64
sz=299
PATH = 'data/dogid'
label_csv = f'{PATH}/labels.csv'
n = len(list(open(label_csv)))-1
val_idxs = get_cv_idxs(n)


tfms = tfms_from_model(arch, sz, aug_tfms=transforms_side_on, max_zoom=1.1)
data = ImageClassifierData.from_csv(PATH, 'train' , label_csv, test_name='test', val_idxs=val_idxs, tfms=tfms, suffix='.jpg')
trn_tfms, val_tfms = tfms
learn = ConvLearner.pretrained(arch, data, precompute=False)
learn.load('my_pup')


# In[4]:


def predictMyPup(fn):
    im = val_tfms(open_image(fn)) #from dataset.py
    log_preds_single = learn.predict_array(im[None])
    breedID = np.argmax(log_preds_single)
    class_probs = np.exp(log_preds_single) # If you want the probabilities of the classes
#    accuracy = class_probs[0].argsort()[0:1]
    breedName = data.classes[breedID]
    return breedName


# In[5]:


def topThree(fn):
    im = val_tfms(open_image(fn))
    log_preds_single = learn.predict_array(im[None])
    arr = np.exp(log_preds_single)
    top3 = arr[0].argsort()[-3:][::-1]
    top_score = data.classes[top3[0]] +'\t'+ '%.2f'%(arr[0][top3[0]]*100)
    second_score = data.classes[top3[1]] +'\t'+ '%.2f'%(arr[0][top3[1]]*100)
    third_score = data.classes[top3[2]] +'\t'+ '%.2f'%(arr[0][top3[2]]*100)
    scores = [top_score, second_score, third_score]
    return scores


# In[6]:


#fn = PATH+'mydogs/IMG_3604.jpg'
#Image.open(fn).resize((250,250))


# In[7]:


#predictMyPup(fn)


# In[8]:


#topThree(fn)


# In[ ]:


#conda install -c peterjc123 pytorch-cpu

