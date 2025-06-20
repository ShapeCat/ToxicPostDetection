import pytest
import tensorflow as tf
from .image import ImagePreprocessor


WHITE_JPEG = tf.image.encode_jpeg(tf.ones((2, 2, 3), dtype=tf.uint8) * tf.constant(255, dtype=tf.uint8))
WHITE_PNG = tf.image.encode_png(tf.ones((2, 2, 3), dtype=tf.uint8) * tf.constant(255, dtype=tf.uint8))


@pytest.fixture
def jpeg_image_fixture(tmp_path):
    img_path = tmp_path / "test_image.jpeg"
    tf.io.write_file(str(img_path), WHITE_JPEG)
    return img_path


@pytest.fixture
def png_image_fixture(tmp_path):
    img_path = tmp_path / "test_image.png"
    tf.io.write_file(str(img_path), WHITE_PNG)
    return img_path


def test_default_initialization_success():
    image_dir = "./dir"
    preprocessor = ImagePreprocessor(image_dir)
    assert preprocessor.image_dir == image_dir
    assert preprocessor.img_size == (224, 224)
    assert preprocessor.image_model == "efficientnet"


def test_custom_initialization_success():
    image_dir = "./dir"
    custom_image_size = (15, 15)
    custom_image_model = 'mobilenet'
    preprocessor = ImagePreprocessor(
                                image_dir,
                                img_size=custom_image_size,
                                image_model=custom_image_model
                                     )
    assert preprocessor.image_dir == image_dir
    assert preprocessor.img_size == custom_image_size
    assert preprocessor.image_model == custom_image_model


def test_load_valid_jpeg_file_success(jpeg_image_fixture, png_image_fixture):
    def test_image_loading(fixture):
        preprocessor = ImagePreprocessor(fixture.parent)
        tensor = preprocessor.load_from_file(fixture.name)
        assert isinstance(tensor, tf.Tensor)
        assert tensor.shape == (224, 224, 3)
        assert not tf.reduce_all(tf.equal(tensor, tf.zeros_like(tensor)))
    test_image_loading(jpeg_image_fixture)
    test_image_loading(png_image_fixture)


def test_load_missing_file_return_empty():
    
    preprocessor = ImagePreprocessor("/invalid/path")
    tensor = preprocessor.load_from_file("not_excists.jpg")
    assert isinstance(tensor, tf.Tensor)
    assert tensor.shape == (224, 224, 3)
    assert tf.reduce_all(tensor == 0)


@pytest.mark.parametrize("image_name", ["", None])
def test_load_empty_filename_return_empty(image_name):
    preprocessor = ImagePreprocessor("/data")
    tensor = preprocessor.load_from_file(image_name)
    assert tf.reduce_all(tensor == 0)


def test_load_from_invalid_file_return_empty(tmp_path):
    invalid_file = tmp_path / "invalid.jpg"
    invalid_file.write_text("text") 
    preprocessor = ImagePreprocessor(tmp_path)
    tensor = preprocessor.load_from_file(invalid_file.name)
    assert tf.reduce_all(tensor == 0)


def test_load_from_url_success(requests_mock):
    def test_image_loading(url, image):
        requests_mock.get(url, content=image)
        preprocessor = ImagePreprocessor("")
        tensor = preprocessor.load_from_url(url) 
        assert isinstance(tensor, tf.Tensor)
        assert tensor.shape == (224, 224, 3)
        assert not tf.reduce_all(tf.equal(tensor, tf.zeros_like(tensor)))
    test_image_loading("https://images.com/image.jpg", tf.convert_to_tensor(WHITE_JPEG).numpy())
    test_image_loading("https://images.com/image.png", tf.convert_to_tensor(WHITE_PNG).numpy())


def test_load_from_url_not_found_return_empty(requests_mock):
    url = "http://images.com/image.jpg"
    requests_mock.get(url, status_code=404)    
    preprocessor = ImagePreprocessor("")
    tensor = preprocessor.load_from_url(url)
    assert requests_mock.last_request.url == url
    assert tf.reduce_all(tensor == 0)


@pytest.mark.parametrize("image_name", ["", None])
def test_load_from_empty_url_return_empty(image_name):
    preprocessor = ImagePreprocessor("")
    tensor = preprocessor.load_from_url(image_name)
    assert tf.reduce_all(tensor == 0)


def test_preprocessing_with_mobilenet_success(requests_mock, mocker):
    url = "http://images.com/image.jpg"
    requests_mock.get(url, content=tf.convert_to_tensor(WHITE_JPEG).numpy())
    preprocessor = ImagePreprocessor("", image_model="mobilenet")
    mocker = mocker.patch("keras.applications.mobilenet.preprocess_input")
    preprocessor.load_from_url(url)
    mocker.assert_called_once()


def test_preprocessing_with_efficientnet_success(requests_mock, mocker):
    url = "http://images.com/image.jpg"
    requests_mock.get(url, content=tf.convert_to_tensor(WHITE_JPEG).numpy())
    preprocessor = ImagePreprocessor("", image_model="efficientnet")
    mocker = mocker.patch("keras.applications.efficientnet.preprocess_input")
    preprocessor.load_from_url(url)
    mocker.assert_called_once()
