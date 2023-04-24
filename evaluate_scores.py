import numpy as np
import pandas as pd
from evaluate import load
from sacrebleu.metrics import BLEU
from rouge import Rouge

from visualize_scores import *
from config import *


def evaluate_data(valid_data, reference_col, predicted_col):
    data = []
    for _, row in valid_data.iterrows():

        data.append(
            {
                "text": row[predicted_col],
                "ref": [row[reference_col]]
            },
        )
    bleu_scorer_obj = BLEU()
    rouge_scorer_obj = Rouge()

    ## Blue Score
    bleu_score = []
    for d in data:
        score = bleu_scorer_obj.sentence_score(
            hypothesis=d['text'],
            references=d['ref'],
        )
        bleu_score.append(score.score/100)

    bleu_score = np.average(np.asarray(bleu_score))

    ## Rouge Score
    rouge_score = []
    for d in data:
        score = rouge_scorer_obj.get_scores(
            hyps=[d['text']],
            refs=d['ref'],
        )
        rouge_score.append(score[0]["rouge-l"]["f"])

    rouge_score = np.average(np.asarray(rouge_score))

    ## Exact match
    exact_match_metric = load("exact_match")
    exact_match = exact_match_metric.compute(predictions=valid_data[predicted_col], references=valid_data[reference_col])

    ## Bert Score
    # bert_scores = {}
    # bertscore = load("bertscore")
    # bert_results = bertscore.compute(predictions=valid_data[predicted_col], references=valid_data[reference_col], model_type="distilbert-base-uncased")

    # bert_scores['precision'] = round(sum(bert_results['precision'])/len(bert_results['precision']), 2)
    # bert_scores['recall'] = round(sum(bert_results['recall'])/len(bert_results['recall']), 2)
    # bert_scores['f1'] = round(sum(bert_results['f1'])/len(bert_results['f1']), 2)

    return {
        "exact_match": exact_match['exact_match'],
        "bleu_score": bleu_score,
        "rouge-l_score": rouge_score
        # "bertscore": bert_scores
    }

if __name__ == '__main__':

    data = pd.read_excel(file_name, index_col = 'Unnamed: 0')
    columns = data.columns

    info_cols.append(reference_col)
    predicted_cols = list(set(columns) - set(info_cols))

    results = {}

    for col in predicted_cols:
        results[col] = evaluate_data(data, reference_col = reference_col, predicted_col = col)

    print(results)

    bar_plot_scores(results, file_name = visualization_name, width = width)
