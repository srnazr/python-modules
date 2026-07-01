import sys

print("=== Player Score Analytics ===")
if len(sys.argv) > 1:
    scores = []
    for score in range(1, len(sys.argv)):
        try:
            scores.append(int(sys.argv[score]))
        except ValueError:
            print(f"Invalid parameter: \'{sys.argv[score]}\'")
    if len(scores) > 0:
        print("Scores processed:", scores)
        print("Total players:", len(scores))
        print("Average score:", sum(scores) / len(scores))
        print("High score:", max(scores))
        print("Low score:", min(scores))
        print("Score range:", max(scores) - min(scores))
    else:
        print("No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ... ")
else:
    print("No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ... ")

