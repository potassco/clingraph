"""
Graphviz integration to generate gifs
"""

import os
import logging
from .graphviz import render
try:
    import imageio.v2 as imageio
    import numpy
except ImportError:
    raise RuntimeError("imageio module has to be installed to save gifs") from None
try:
    from PIL import Image
except ImportError:
    raise RuntimeError("pillow module has to be installed to save gifs") from None
log = logging.getLogger('custom')

def save_gif(graphs, directory='out', name_format="movie", engine="dot", fps=1, sort="asc-str"):
    """
    Generates a gif for the given graphs

    Args:
        graphs (dic|list[dic]): A dictionary of graphviz objects where the keys are the graph names.
                Or a list of such dictionaries, each element corresponding to a model.
        directory (str): Path to the directory where to write
        name_format (str): The file name for the gif can include `{model_number}`
        engine (str): The engine used for rendering
        fps (int): The number of frames per second
        sort (str): How to sort the images used to generate the gif
                ``asc-str`` Sort ascendent based on the graph name,
                ``desc-str`` Sort descendent based on the graph name,
                ``asc-int`` Sort descendent based on the graph name converted to an interger,
                ``desc-int`` Sort descendent based on the graph name converted to an integer,
                ``name1,...,namex`` A string with the order of the graph names separated by `,`
    Returns:
        [dic | list[dic]]: A dictionary with the paths where the gifss where saved as values for each graph.
                Or a list of such dictionaries, each element corresponding to a model.
    """
    is_multi = isinstance(graphs,list)
    if not is_multi:
        graphs = [graphs]
    images_dir = os.path.join(directory, 'images')
    img_name_format = 'gif_image_{graph_name}_{model_number}'
    render(graphs,
            directory = images_dir,
            format="png",
            engine=engine,
            name_format=img_name_format)
    all_keys = []
    for graph in graphs:
        if graph is None:
            all_keys.append(None)
            continue
        keys = list(graph.keys())
        if sort in ["asc-str","asc-int","desc-str","desc-int",]:
            l_key = str if sort[-3:] == 'str' else int
            l_reverse =  sort[:3] == 'desc'
            keys.sort(key = l_key, reverse = l_reverse)
            ordered_keys = keys
        else:
            ordered_keys = sort.split(',')
            for k in ordered_keys:
                if not k in keys:
                    raise ValueError(f"Invalid graph name in sort: {k}")
        all_keys.append(ordered_keys)
    paths = []
    for model_n,graph in enumerate(graphs):
        if graph is None:
            continue
        name = name_format.replace('{graph_name}','movie').replace('{model_number}',str(model_n))
        gif_path = os.path.join(directory, f'{name}.gif')
        images = []
        max_x = 0
        max_y = 0
        for k in all_keys[model_n]:
            img_path = img_name_format.replace('{graph_name}',k)
            img_path = img_path.replace('{model_number}',str(model_n))+".png"
            img_arr = imageio.imread(os.path.join(images_dir, img_path),mode="RGBA")
            x,y,_ = img_arr.shape
            max_x = x if x>max_x else max_x
            max_y = y if y>max_y else max_y
            images.append(img_arr)
        for idx,img in enumerate(images):
            p_img= Image.fromarray(img).resize((max_y, max_x))
            images[idx]=numpy.asarray(p_img)


        os.makedirs(os.path.dirname(gif_path), exist_ok=True)

        duration = int(1000 * 1/float(fps))
        imageio.mimsave(gif_path,
                        images, duration=duration)
        paths.append({'all':gif_path})

    if not is_multi:
        return paths[0]
    return paths
