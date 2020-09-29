import win32gui
import win32api
import win32con
import cv2
import numpy as np
from typing import Union
from common.window import Window
from os import walk


class Actions:
    @staticmethod
    def image_path_to_cv_object(filename: str) -> np.ndarray:
        return cv2.imread(filename)

    @staticmethod
    def calc_image_hash(filename: Union[str, np.ndarray], hash_size: int = 7) -> str:
        if isinstance(filename, str):
            image = Actions.image_path_to_cv_object(filename)
        else:
            image = filename

        resized = cv2.resize(image, (hash_size, hash_size), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
        avg = gray_image.mean()  # Среднее значение пикселя
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу
        # Рассчитаем хэш
        _hash = ""
        for x in range(hash_size):
            for y in range(hash_size):
                val = threshold_image[x, y]
                if val == 255:
                    _hash += "1"
                else:
                    _hash += "0"
        return _hash

    @staticmethod
    def compare_hash(hash1: str, hash2: str) -> int:
        len_hash = len(hash1)
        if len_hash != len(hash2):
            raise ValueError("Hash lengths of pictures not equal")
        i = 0
        count = 0
        while i < len_hash:
            if hash1[i] != hash2[i]:
                count = count + 1
            i = i + 1
        return count

    @staticmethod
    def compare_images(image1: Union[str, np.ndarray], image2: Union[str, np.ndarray]) -> int:
        if isinstance(image1, str):
            image1 = Actions.image_path_to_cv_object(image1)
        if isinstance(image2, str):
            image2 = Actions.image_path_to_cv_object(image2)

        return Actions.compare_hash(Actions.calc_image_hash(image1), Actions.calc_image_hash(image2))

    @staticmethod
    def find_patt(image: np.ndarray, patt: np.ndarray, thres: float = 0.6):
        img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (patt_h, patt_w) = patt.shape[:2]
        res = cv2.matchTemplate(img_grey, patt, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res > thres)
        result_point = list(next(zip(*loc[::-1])))
        result_point[0] += int(patt_h / 2)
        result_point[1] += int(patt_w / 2)
        return result_point

    @staticmethod
    def show_picture(img):
        cv2.imshow("image", img)
        cv2.waitKey(0)

    @staticmethod
    def define_location(window: Window):
        current_img = window.get_screenshot_from_window()
        location_path = "data/locations/"
        location_files = []
        for dir_path, dir_names, file_names in walk(location_path):
            for file_name in file_names:
                location_files.append((file_name.split(".")[0], location_path + file_name))

        current_location = min(map(lambda location: (location[0], Actions.compare_images(current_img, location[1])),
                                   location_files), key=lambda obj: obj[1])
        current_location = current_location[0] if current_location[1] <= 10 else None

        """
        print(current_location)
        for location_file in location_files:
            compare = Actions.compare_images(current_img, location_file[1])
            if compare <= 9:
                current_location = location_file[0]
            print(location_file[0], compare)
        """

        print(f"Current location: {current_location}")

    @staticmethod
    def save_image(image: np.ndarray, filename) -> None:
        cv2.imwrite(filename, image)



