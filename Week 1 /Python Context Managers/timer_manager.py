image=get_image("https://www.python.org/static/community_logos/python-logo.png")

with timer():
    image.show()
    process_with_numpy(image)


with timer():
    image.show()
    process_with_pytorch(image)