import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np


def make_request(html):
    """Makes a request given an html

    Takes an html string and make a request.

    Args:
        html (string): html string

    Returns:
        requests.Response object

    """
    return requests.get(html)


def get_soup(request):
    """Takes a html request to be parsed

    Get a request object parsed

    Args:
        request (requests.Response object): takes the return value of make_request

    Returns:
        Beautiful Soup Object

    """
    return BeautifulSoup(request.content, "html.parser")


def process_user_profile_pic(soup: BeautifulSoup, img_path=None):
    """Finds the user profile picture given its soup

    Finds and saves the user profile picture locally.

    Args:
        soup (Beautiful Soup object): the beautiful soup object to be analyzed

    Returns:
        tuple: returns the username of the profile and the link to access the image

    """
    # find the img tag with the user's profile picture
    res = soup.findAll("img", {"data-testid": "user-entity-image"})
    src = res[0].get("src")
    # this is the profile image
    pic = make_request(f"{src}")
    # this is the user name
    head = soup.find("head")
    title = head.find("title")
    username = title.text.split(" ")[0]
    if pic.status_code == 200:
        path = img_path if img_path else f"./images/{username}.jpg"
        with open(path, "wb") as f:
            f.write(pic.content)
    else:
        raise Exception("Failed to fetch picture")
    return (username, src)


def get_public_playlists_albums(soup: BeautifulSoup, img_path=None):
    """Fetches and saves the public playlist album pictures

    Given a user's profile's soup, fetches and saves all the album pictures of the public playlists the user has.

    Args:
        soup (BeautifulSoup object): return value of get_soup
        img_path (string): the path to save the image. If none, the program will save to images directory.

    Returns:
        tuple: returns username and the number of public playlists found

    """
    res = soup.findAll("img")[1:]
    head = soup.find("head")
    title = head.find("title")
    username = title.text.split(" ")[0]
    for i in range(0, len(res)):
        ele = res[i]
        src = ele.get("src")
        pic = make_request(f"{src}")
        if pic.status_code == 200:
            path = img_path if img_path else f"./images/{username}_playlist_{i}.jpg"
            with open(path, "wb") as f:
                f.write(pic.content)
    return (username, len(res))


def get_individual_album_covers_from_mosaic(link, img_path=None):
    """Take one mosaic album cover and save four individual covers from it

    This is the function to get individual pictures from a mosaic album cover

    Args:
        link (string): The link of the mosaic album picture
        img_path (string): the path to save the image. If none, the program will save to images directory.

    Returns:
        list: a list of individual album picture links

    """
    # For example: "https://mosaic.scdn.co/300/ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164fc6"
    if "https://mosaic.scdn.co/" not in link:
        raise Exception("Invalid mosaic link, please make sure the link starts with https://mosaic.scdn.co/300/")
    split_link = link.split("/")
    if len(split_link) != 5:
        raise Exception("Depracated mosaic link, please try a new link")
    imgs = split_link[-1]
    li_imgs = []
    if len(imgs) != 160:
        return Exception("Sorry this link cannot be broken down")
    pre = "https://lite-images-i.scdn.co/image/"
    for i in range(0, 4):
        li_imgs.append(pre + imgs[i * 40 : (i + 1) * 40])
        pic = make_request(pre + imgs[i * 40 : (i + 1) * 40])
        if pic.status_code == 200:
            path = img_path if img_path else f"./images/mosaic_{i}.jpg"
            with open(path, "wb") as f:
                f.write(pic.content)
    return li_imgs


def get_playlist_profile_pic(soup, img_path=None):
    """Fetches and saves the cover picture of a playlist

    Args:
        soup (BeautifulSoup object): return value of get_soup
        img_path (string): the path to save the image. If none, the program will save to images directory.

    Returns:
        tuple: the name of the playlist and the link of the image

    """
    res = soup.findAll("img")[0]
    # find playlist name
    name = soup.find("h1")
    playlist_name = name.text
    pic = make_request(res.get("src"))
    if pic.status_code == 200:
        path = img_path if img_path else f"./images/{playlist_name}_profile.jpg"
        with open(path, "wb") as f:
            f.write(pic.content)
    return (playlist_name, res.get("src"))


def process_artist_album(soup: BeautifulSoup, img_path=None):
    """Gets and saves the album covers given an artist

    Given the soup of the artist page, fetches all the album covers on that page and saves them locally.

    Args:
        soup (BeautifulSoup object): Return value of get_soup
        img_path (string): the path to save the image. If none, the program will save to images directory.

    Returns:
        list: a list of dictionaries, each dictionary contains the albumName, albumLink, albumImageUrl, and albumSlug

    """
    # Find the h2 tag with text of Albums
    albumHeading = soup.find("h2", string="Albums")

    # Get the parent section
    albumSection = albumHeading.find_parent("div").find_parent("div")

    # Find all albums in the album section
    albums = albumSection.findAll("div")[1:]

    # Iterate through each album and get the data needed
    albumObj = []
    for album in albums:
        atag = album.find("a")
        if atag is None:
            continue
        href = f"{atag['href']}"
        albumName = atag.find("span").text
        albumSlug = albumName.replace(" ", "-").lower()
        albumImage = atag.find("img").get("src")
        albumDetails = {
            "albumName": albumName,
            "albumLink": href,
            "albumImageUrl": albumImage,
            "albumSlug": albumSlug,
        }

        albumObj.append(albumDetails)

        # Download the image at the image URL and save it in an images folder
        pic = make_request(f"{albumImage}")
        if pic.status_code == 200:
            path = img_path if img_path else f"./images/{albumSlug}.jpg"
            with open(path, "wb") as f:
                f.write(pic.content)
    return albumObj


def filter_all_other_color(path_to_img, threshold_low, threshold_high):
    """Returns a new image that only contains color within a certain range

    Given the path to an image and the range of color that needs to be saved, will return a new image with the pixels only within the range.

    Args:
        path_to_img (string): the path to the image
        threshold_low (tuple): the low BGR threshold
        threshold_high (tuple): the upper-end of the BGR threshold

    Returns:
        np.array: the image in pixel

    """
    img = cv2.imread(path_to_img)
    assert img is not None, "file could not be read, check with os.path.exists()"
    mask = cv2.inRange(img, threshold_low, threshold_high)
    masked_img = mask > 0
    new_img = np.zeros_like(img, np.uint8)
    # Set each pixel
    new_img[masked_img] = img[masked_img]
    return new_img


def filter_this_color(path_to_img, threshold_low, threshold_high):
    """Returns a new image that contains all colors except the color within a certain range

    Given the path to an image and the range of color that does not need, will return a new image with the pixels outside of the range.

    Args:
        path_to_img (string): the path to the image
        threshold_low (tuple): the low BGR threshold
        threshold_high (tuple): the upper-end of the BGR threshold

    Returns:
        np.array: the image in pixel

    """
    img = cv2.imread(path_to_img)
    assert img is not None, "file could not be read, check with os.path.exists()"
    mask = cv2.inRange(img, threshold_low, threshold_high)
    masked_img = ~mask > 0
    new_img = np.zeros_like(img, np.uint8)
    # Set each pixel
    new_img[masked_img] = img[masked_img]
    return new_img


def smooth_img(path_to_img, threshold=(5, 5)):
    """Returns a new image that is blurred

    Given the path to an image and optional parameter that blurs the image by a certain degree, the function returns a function that is blurred

    Args:
        path_to_img (string): the path to the image
        threshold: the optional parameter that determines the kernel size

    Returns:
        np.array: the image in pixel

    """
    img = cv2.imread(path_to_img)
    assert img is not None, "file could not be read, check with os.path.exists()"
    return cv2.blur(img, threshold)


def return_most_common_color(path_to_img):
    """Returns the most common color in the image

    Given the path to an image, returns the most common color in the image

    Args:
        path_to_img (string): the path to the image

    Returns:
        tuple: the BGR value of that color and its count

    """
    img = cv2.imread(path_to_img)
    assert img is not None, "file could not be read, check with os.path.exists()"

    pix_d = {}
    for i in range(0, len(img)):
        for j in range(0, len(img[0])):
            pix = img[i][j]
            tup = (pix[0], pix[1], pix[2])
            if tup in pix_d:
                pix_d[tup] += 1
            else:
                pix_d[tup] = 1

    maxi = (None, float('-inf'))
    for ele, val in pix_d.items():
        if val > maxi[1]:
            maxi = (ele, val)

    return maxi


def overlay_two_images(path_to_img1, path_to_img2, weight1, weight2):
    """Returns the overlay of two images

    Given the paths to two images and how much each image should weight in the final image, returns their overlay.

    Args:
        path_to_img1 (string): the path to the first image
        path_to_img2 (string): the path to the second image
        weight1 (double): how much the first image should weigh from 0 to 1
        weight2 (double): how much the second image should weigh from 0 to 1

    Returns:
        np.array: the blended image in pixel

    """
    img1 = cv2.imread(path_to_img1)
    assert img1 is not None, "file could not be read, check with os.path.exists()"
    img2 = cv2.imread(path_to_img2)
    assert img2 is not None, "file could not be read, check with os.path.exists()"
    # check if the two sizes match
    if len(img1) != len(img2) or len(img1[0]) != len(img2[0]):
        raise Exception("The two image sizes are different")
    return cv2.addWeighted(img1, weight1, img2, weight2, 0)
