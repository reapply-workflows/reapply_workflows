from typing import Any, List

import numpy as np
from sklearn import tree

from backend.inference_core.intent_contract import Prediction
from backend.inference_core.prediction_stats import getStats


def get_mask_from_exp(data, exp):
    feature, op, val, mask = None, None, None, None
    if ">=" in exp:
        op = ">="
        feature, val = exp.split(">=")
    else:
        op = "<="
        feature, val = exp.split("<=")
    feature = feature.strip()
    val = float(val.strip())
    if op == ">=":
        mask = data[feature] >= val
    else:
        mask = data[feature] <= val

    return mask


def get_mask_from_rules(data, rules):
    mask = None

    for rule in rules:
        m = None
        for exp in rule:
            if m is None:
                m = get_mask_from_exp(data, exp)
            else:
                m &= get_mask_from_exp(data, exp)
        if mask is None:
            mask = m
        else:
            mask |= m
    return mask


def get_decision_paths(model: tree.DecisionTreeClassifier, data, selection):
    selected_rows = data.loc[selection.astype(bool), :]

    d_path = model.decision_path(selected_rows)
    paths = set()

    leaf_id = model.apply(selected_rows)
    feature = model.tree_.feature
    threshold = model.tree_.threshold

    for sample_id in range(len(selected_rows.index)):
        node_idx = d_path.indices[
            d_path.indptr[sample_id] : d_path.indptr[sample_id + 1]
        ]

        rules = []

        for node_id in node_idx:
            if leaf_id[sample_id] == node_id:
                continue

            sign = None
            if selected_rows.iloc[sample_id, feature[node_id]] <= threshold[node_id]:
                sign = " <= "
            else:
                sign = " >= "

            rule = (
                data.columns[feature[node_id]]
                + sign
                + str(round(threshold[node_id], 2))
            )

            rules.append(rule)
        paths.add(tuple(rules))

    paths = [[rule for rule in path] for path in paths]
    return paths


def range_intent(dataset, dimensions, selection, max_depth=None) -> List[Prediction]:
    selection = np.array(selection)
    selected_ids = dataset.loc[selection.astype(bool), "id"]
    data = dataset[dimensions]
    clf = tree.DecisionTreeClassifier(max_depth=max_depth)
    clf.fit(data, selection)

    rules = get_decision_paths(clf, data, selection)

    mask: Any = get_mask_from_rules(data, rules)
    member_ids = dataset.loc[mask, "id"].tolist()
    current_depth = clf.get_depth()

    intent = "Range" if max_depth is None else "SimplifiedRange"

    rank = 1 / (pow(current_depth, 2) + 1)

    algorithm = "DecisionTree"

    pred = Prediction(
        rank=rank,
        intent=intent,
        memberIds=member_ids,
        dimensions=dimensions,
        info={"depth": clf.get_depth(), "rules": rules},
        algorithm=algorithm,
        membership=getStats(member_ids, selected_ids.tolist()),
        description=f"Range-{algorithm}",
    )

    if current_depth > 1 and max_depth is None:
        new_pred = range_intent(dataset, dimensions, selection, current_depth - 1)
        pred_list = []
        pred_list.append(pred)
        pred_list.extend(new_pred)
        return pred_list

    return [pred]
