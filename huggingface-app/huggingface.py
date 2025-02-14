from transformers import AutoModelForSequenceClassification,AutoTokenizer
from datasets import load_dataset

#加载数据集
datasets_name = "imdb"
task = "sentiment_analysis"

dataset = load_dataset(datasets_name)
dataset = dataset.shuffle()

#加载模型和分词器
model_name = "bert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name,num_labels=2)

data = dataset["train"]["text"][:10] #取前10条数据
inputs = tokenizer(data,return_tensors="pt",padding=True,truncation=True)
#将编码后的张量传入模型
outputs = model(**inputs)

#获取预测结果和标签
predictions = outputs.logits.argmax(dim=-1)
labels = dataset["train"]["label"][:10]

for i , (prediction,label) in enumerate(zip(predictions,labels)):
    prediction_label = "正面评论" if prediction == 1 else "负面评论"
    true_label = "正面评论" if label == 1 else "负面评论"
    print(f"样本{i+1}：预测结果: {prediction_label}，真实标签: {true_label}")