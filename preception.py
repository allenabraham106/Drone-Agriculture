import cv2


def parser(image_path):
    image = cv2.imread(image_path)
    resized = cv2.resize(image, (800, 800))
    b, g, r = cv2.split(resized)
    yield_zones = {}
    for row in range(40):
        for col in range(40):
            block_g = g[row * 20 : (row + 1) * 20, col * 20 : (col + 1) * 20]
            block_r = r[row * 20 : (row + 1) * 20, col * 20 : (col + 1) * 20]
            avg_g = block_g.mean()
            avg_r = block_r.mean()
            excess_green = avg_g - avg_r
            print(f"Sample values: {excess_green:.2f}")
            if excess_green >= 20:
                yield_zones[(row, col)] = "high"
            elif excess_green >= 5:
                yield_zones[(row, col)] = "medium"
            else:
                yield_zones[(row, col)] = "low"
    return yield_zones


if __name__ == "__main__":
    zones = parser("Feild.jpg")
    print(zones)