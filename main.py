from selenium import webdriver
from PIL import Image
import os
import subprocess

# Number of captchas to generate
num_captchas = 5  # Set the desired number of captchas

# Site to get the captcha from
website = "https://sitebuilder.homestead.com/~site/siteapps/captchaImage.action"

if not os.path.exists("captcha"):
    os.makedirs("captcha")

# Function to download and crop the captcha image
def get_captcha(driver, iteration):
    # Save the screenshot of the entire page in the captcha folder
    image_path = f"captcha/captcha_{iteration}.png"
    driver.save_screenshot(image_path)

    # Open the screenshot using Pillow
    image = Image.open(image_path)

    # Get the dimensions of the screenshot
    image_width, image_height = image.size

    # Define the captcha image size
    captcha_width = 95
    captcha_height = 30

    # Calculate the coordinates of the cropping box (centered)
    left = (image_width - captcha_width) // 2
    upper = (image_height - captcha_height) // 2
    right = left + captcha_width
    lower = upper + captcha_height

    # Crop the image using the calculated coordinates
    cropped_image = image.crop((left, upper, right, lower))

    # Save the image
    cropped_image.save(image_path)
    print(f"Captcha {iteration} saved.")

# Function to prompt the user for the captcha solution and rename the file
def prompt_for_captcha_solution(iteration):
    # Open the captcha image from the captcha folder
    image_path = f"captcha/captcha_{iteration}.png"
    image = Image.open(image_path)
    image.show()  # Display the captcha image

    # Prompt the user to input the captcha solution
    captcha_value = input(f"Enter the captcha value for image {iteration}: ")

    # Close the image viewer by killing the process (platform-dependent)
    # For Windows
    if os.name == 'nt':
        subprocess.run(['taskkill', '/F', '/IM', 'Photos.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # For macOS
    elif os.name == 'posix':
        subprocess.run(['pkill', 'Preview'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Rename the image to the user's input in the captcha folder
    new_image_path = f"captcha/{captcha_value}.png"
    os.rename(image_path, new_image_path)
    print(f"Captcha {iteration} saved as {new_image_path}")


if __name__ == "__main__":
    # Open the browser
    driver = webdriver.Chrome()

    # Loop to generate multiple captchas
    for i in range(num_captchas):
        driver.get(website)
        get_captcha(driver, i + 1)

    # Close the browser after all iterations
    driver.quit()

    # After all captchas are generated, loop through each one and prompt for input
    for i in range(num_captchas):
        prompt_for_captcha_solution(i + 1)  # Prompt user to solve captcha

    print("All captchas processed.")
