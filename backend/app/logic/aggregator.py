from collections import defaultdict

def aggregate_violations(events):
    """
    events: [
        {
            "frame": int,
            "violations": [
                {"violation": str, "severity": str}
            ]
        }
    ]
    """

    aggregated = defaultdict(list)

    for e in events:
        for v in e.get("violations", []):
            aggregated[v["violation"]].append(e["frame"])

    return dict(aggregated)
