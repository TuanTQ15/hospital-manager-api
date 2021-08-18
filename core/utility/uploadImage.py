import cloudinary.uploader as up
import cloudinary

cloudinary.config(
    cloud_name="ptithcm",
    api_key="649875216812692",
    api_secret="JGU8KM7qbRLHeM86XAT_HG5XQCA"
)


def uploadFile(file_upload):
    try:
        return up.upload(file_upload)['url']
    except:
        return "https://res.cloudinary.com/ptithcm/image/upload/v1629283355/default_user.png"
