from transformers import pipeline
import pandas as pd
from tqdm import tqdm

def get_emotion(classifier, plot):
    
    prediction = classifier(plot)
    emotion = max(prediction[0], key=lambda x: x['score'])
    label = emotion['label']
    value = emotion['score']
    return label, value

def main():
    classifier = pipeline("text-classification",model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
    df = pd.read_csv('data/final_plot_release_cleaned.csv')
    for index, row in tqdm(df.iterrows(), total=len(df)):

        label, value = get_emotion(classifier,row['plot_summary'])
        df.loc[index, 'emotion'] = label
        df.loc[index, 'emotion_score'] = value

if __name__ == "__main__":
    main()