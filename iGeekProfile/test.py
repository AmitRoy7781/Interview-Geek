import pyimgur

CLIENT_ID = "487285bb8012d86"
PATH = "/home/amit-roy/Pictures/cube.jpg"

im = pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH, title="Amit")
print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.size)
print(uploaded_image.type)