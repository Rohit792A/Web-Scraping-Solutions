from transformers import AutoProcessor,MarkupLMForQuestionAnswering
import pickle

processor = AutoProcessor.from_pretrained("microsoft/markuplm-base-finetuned-websrc")
model = MarkupLMForQuestionAnswering.from_pretrained("microsoft/markuplm-base-finetuned-websrc")


# save the iris classification model as a pickle file
model_pkl_file = "model.pkl"  

with open(model_pkl_file, 'wb') as file:  
    pickle.dump(model, file)

processor_pkl_file = "processor.pkl"  

with open(processor_pkl_file, 'wb') as file:  
    pickle.dump(processor, file)

