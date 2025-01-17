import urllib.request
import zipfile
import os
import gdown


def get_file_from_pysilcam_blob(filename):
    '''Downloads a specified filename from the pysilcam.blob into the working dir. if it doesn't already exist

    only works for known filenames that are on this blob

    Parameters
    ----------
    filename : string
        known filename on the blob

    '''
    if os.path.exists(filename):
        return filename
    url = 'https://pysilcam.blob.core.windows.net/test-data/' + filename
    urllib.request.urlretrieve(url, filename)


def get_example_silc_image():
    '''calls `get_file_from_pysilcam_blob` for a silcam iamge

    Returns
    -------
    string
        filename
    '''
    filename = 'D20181101T142731.838206.silc'
    get_file_from_pysilcam_blob(filename)
    return filename


def get_example_model():
    '''Downloads and unzips an example trained CNN model from the pysilcam.blob
    into the working dir. if it doesn't already exist.

    Returns
    -------
    string
        model_filename
    '''
    model_filename = 'keras_model.h5'
    if os.path.exists(model_filename):
        return model_filename
    # -- Download and unzip the model --#
    url = 'https://github.com/SINTEF/PySilCam/wiki/ml_models/keras_model.zip'
    model_filename = 'keras_model.zip'
    urllib.request.urlretrieve(url, model_filename)
    with zipfile.ZipFile(model_filename, 'r') as zipit:
        zipit.extractall()
    model_filename = 'keras_model.h5'
    return model_filename


def get_example_hologram_and_background():
    '''calls `get_file_from_pysilcam_blob` for a raw hologram, and its associated background image.

    Returns
    -------
    string
        holo_filename

    string
        holo_background_filename
    '''
    holo_filename = '001-2082.pgm'
    holo_background_filename = 'imbg-' + holo_filename
    get_file_from_pysilcam_blob(holo_filename)
    get_file_from_pysilcam_blob(holo_background_filename)
    return holo_filename, holo_background_filename


def get_folder_from_holo_repository(foldername="holo_test_data_01"):
    '''Downloads a specified folder from the holo testing repository into the working dir. if it doesn't already exist

    only works for known folders that are on the GoogleDrive repository
    by default will download a known-good folder. Additional elif statements can be added to implement additional folders.

    Parameters
    ----------
    foldername : string
        known filename on the blob

    '''
    if foldername == "holo_test_data_01":
        url = 'https://drive.google.com/drive/folders/1yNatOaKdWwYQp-5WVEDItoibr-k0lGsP?usp=share_link'

    elif foldername == "holo_test_data_02":
        url = "https://drive.google.com/drive/folders/1E5iNSyfeKcVMLVe4PNEwF2Q2mo3WVjF5?usp=share_link"

    else:
        foldername == "holo_test_data_01"
        url = 'https://drive.google.com/drive/folders/1yNatOaKdWwYQp-5WVEDItoibr-k0lGsP?usp=share_link'

    gdown.download_folder(url, quiet=True, use_cookies=False)
    return foldername
