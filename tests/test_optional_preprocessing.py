from microbundlecompute import optional_preprocessing as op
from microbundlecompute import image_analysis as ia
from pathlib import Path
import numpy as np
import cv2
import glob


def files_path():
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("files").resolve()
    return data_path


def example_path(example_name):
    data_path = files_path()
    ex_path = data_path.joinpath(example_name).resolve()
    return ex_path


def movie_path(example_name):
    ex_path = example_path(example_name)
    mov_path = ex_path.joinpath("movie").resolve()
    return mov_path


def glob_movie(example_name):
    folder_path = example_path(example_name)
    movie_path = folder_path.joinpath("movie").resolve()
    name_list = glob.glob(str(movie_path) + '/*.TIF')
    name_list.sort()
    name_list_path = []
    for name in name_list:
        name_list_path.append(Path(name))
    return name_list


def test_rename_folder():
    folder_path = example_path("io_testing_examples")
    new_folder_name = "test_create_folder_%i" % (np.random.random() * 1000000)
    folder_name = "old_name"
    _ = ia.create_folder(folder_path,folder_name)
    new_folder_name = "new_name"
    new_folder_path = op.rename_folder(folder_path, folder_name, new_folder_name)
    assert new_folder_path.is_dir


def test_apply_image_kernel():
    array = np.random.random((10, 10))
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    known = cv2.filter2D(array, -1, kernel)
    found = op.apply_image_kernel(array, kernel)
    assert np.allclose(known, found)


def test_filter_all_images():
    folder_path = movie_path("example_image_filter")
    path_list = ia.image_folder_to_path_list(folder_path)
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    filtered_img_list = op.filter_all_images(path_list, kernel)
    assert len(path_list) == len(filtered_img_list)


def test_run_image_filtering():
    folder_path = example_path("example_image_filter")
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    filtered_img_list = op.filter_all_images(folder_path, kernel)
    raw_images = glob_movie(folder_path)
    assert len(filtered_img_list) == len(raw_images)



    