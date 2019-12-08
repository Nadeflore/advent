with open("input8") as f:
    data = f.read()

    width = 25
    height = 6

    layersize = width * height
    layerscount = int(len(data) / layersize)

    layers = [data[i * layersize : (i + 1) * layersize] for i in range(layerscount)]

    fewerzerolayer = min(layers, key=lambda e: e.count('0'))

    print("First part nb1 * nb2 = {}".format(fewerzerolayer.count('1') * fewerzerolayer.count('2')))

    result = ['2'] * layersize

    for layer in layers:
        result = [l if r == '2' else r for l, r in zip(layer, result)]

    result = ''.join(result)

    # Replace for better visual
    result = result.replace('0', ' ').replace('1', '#')

    for j in range(height):
        print(result[j * width : (j + 1) * width])
