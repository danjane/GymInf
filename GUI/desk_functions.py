def standard_pairs_layout(columns, rows):
    num_possible_columns = 3*columns//2 - 1
    num_possible_rows = 2*rows - 1
    pairs = [(x, y)
             for y in range(num_possible_rows)
             for x in range(num_possible_columns)
             if x % 3 < 2 if y % 2 == 0]
    return pairs
