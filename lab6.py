def alpha_beta(depth, node_index, is_maximizing, values, alpha, beta):
    if depth == 3:
        print("Visited leaf:", values[node_index])
        return values[node_index]

    if is_maximizing:
        best = float('-inf')
        for i in range(2): 
            val = alpha_beta(depth + 1, node_index * 2 + i, False, values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)

            if beta <= alpha:
                print("Pruned at depth", depth, "with alpha =", alpha, "beta =", beta)
                break
        return best
    else:
        best = float('inf')
        for i in range(2):
            val = alpha_beta(depth + 1, node_index * 2 + i, True, values, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)

            if beta <= alpha:
                print("Pruned at depth", depth, "with alpha =", alpha, "beta =", beta)
                break
        return best


values = [3, 5, 6, 9, 1, 2, 0, -1]

print("Optimal value:", alpha_beta(0, 0, True, values, float('-inf'), float('inf')))
