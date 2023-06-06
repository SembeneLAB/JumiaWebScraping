import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import streamlit as st

def scrape_jumia(url):
    # Send a GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the product containers on the page
        products = soup.find_all('div', {'class': 'itm'})

        # Create a list to store the product information
        product_info = []

        # Iterate over each product container and extract relevant information
        for product in products:
            # Extract the product title
            title = product.find('div', {'class': 'name'}).text.strip()

            # Extract the product price
            price = product.find('div', {'class': 'prc'}).text.strip()

            link = product.find('a', {'class': 'core'})['href']

            discount = product.find('div', {'class': 'bdg _dsct'}).text.strip()

            # Extract the product image URL
            image_url = product.find('img', {'class': 'img'})['data-src']

            # Append the product information to the list
            product_info.append({
                'title': title,
                'price': price,
                'discount': discount,
                'image_url': image_url,
                'link': link
            })

        # Display the products in a row with three products per row
        for i in range(0, len(product_info), 3):
            row = product_info[i:i+3]
            st.write('<div style="display: flex; flex-direction: row;">', unsafe_allow_html=True)
            for product in row:
                st.write('<div style="margin: 10px; text-align: center;">', unsafe_allow_html=True)
                st.subheader(product['title'])
                st.image(product['image_url'], width=200)
                st.write(f"Price: {product['price']}")
                st.write(f"Discount: {product['discount']}")
                st.markdown(f"[Product Link](https://www.jumia.com.ng/{product['link']})")
                st.write('</div>', unsafe_allow_html=True)
            st.write('</div>', unsafe_allow_html=True)

    else:
        st.write("Error accessing the website.")

# URL of the Jumia page to scrape
url = 'https://www.jumia.com.ng/smartphones/'

# Call the function to start scraping
scrape_jumia(url)
