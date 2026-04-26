import random

yield_colours = {
    "low" : (255, 255, 0),
    "medium" : (255, 165, 0),
    "high" : (0, 200, 0)
}

def generate_farm(rows, cols):
    yeild_zone = {

    }
    num_seeds = random.randint(3, 7)
    seeds = [(random.randint(0, rows-1), random.randint(0, cols-1)) for _ in range(num_seeds)]
    for row in range(rows):
        for col in range(cols):
            min_dist = min(abs(row - s[0]) + abs(col - s[1]) for s in seeds) + random.uniform(-3, 3)
            if min_dist < 5: 
                yeild_zone[(row, col)] = "high"
            elif min_dist < 10:
                yeild_zone[(row, col)] = "medium"
            else: 
                yeild_zone[(row, col)] = "low"
    return yeild_zone