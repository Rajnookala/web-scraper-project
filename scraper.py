import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Function to scrape G2 reviews
def scrape_g2_reviews(company_name, start_date, end_date):
    url = f"https://www.g2.com/products/salesforce-salesforce-sales-cloud/video-reviews"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    # Send request to the URL
    response = requests.get(url, headers=headers)
    
    # Check if request is successful
    if response.status_code != 200:
        print("Error: Unable to fetch data")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    reviews = []
    
    # Find reviews container (based on G2's page structure, may need to adjust based on actual HTML structure)
    review_elements = soup.find_all('div', class_='review__content')
    
    for review in review_elements:
        # Extract review title, description, date, rating, and reviewer
        title = review.find('h2', class_='review__title').text.strip() if review.find('h2', class_='review__title') else 'No Title'
        description = review.find('div', class_='review__description').text.strip() if review.find('div', class_='review__description') else 'No Description'
        date = review.find('span', class_='review__date').text.strip() if review.find('span', class_='review__date') else 'Unknown Date'
        rating = review.find('span', class_='star-rating__value').text.strip() if review.find('span', class_='star-rating__value') else 'No Rating'
        reviewer = review.find('span', class_='user__name').text.strip() if review.find('span', class_='user__name') else 'Anonymous'
        
        # Convert review date to datetime object for comparison
        try:
            review_date = datetime.strptime(date, '%b %d, %Y')
        except ValueError:
            review_date = None
        
        # Check if the review falls within the specified time range
        if review_date and start_date <= review_date <= end_date:
            reviews.append({
                'title': title,
                'description': description,
                'date': date,
                'reviewer': reviewer,
                'rating': rating
            })
    
    return reviews

# Function to scrape Capterra reviews
def scrape_capterra_reviews(company_name, start_date, end_date):
    url = f"https://www.g2.com/products/salesforce-salesforce-sales-cloud/video-reviews"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    # Send request to the URL
    response = requests.get(url, headers=headers)
    
    # Check if request is successful
    if response.status_code != 200:
        print("Error: Unable to fetch data")
        return []
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    reviews = []
    
    # Find reviews container (based on Capterra's page structure, may need to adjust based on actual HTML structure)
    review_elements = soup.find_all('div', class_='review-card')
    
    for review in review_elements:
        # Extract review title, description, date, rating, and reviewer
        title = review.find('h4', class_='review-title').text.strip() if review.find('h4', class_='review-title') else 'No Title'
        description = review.find('p', class_='review-body').text.strip() if review.find('p', class_='review-body') else 'No Description'
        date = review.find('span', class_='review-date').text.strip() if review.find('span', class_='review-date') else 'Unknown Date'
        rating = review.find('span', class_='rating-stars').text.strip() if review.find('span', class_='rating-stars') else 'No Rating'
        reviewer = review.find('span', class_='reviewer-name').text.strip() if review.find('span', class_='reviewer-name') else 'Anonymous'
        
        # Convert review date to datetime object for comparison
        try:
            review_date = datetime.strptime(date, '%b %d, %Y')
        except ValueError:
            review_date = None
        
        # Check if the review falls within the specified time range
        if review_date and start_date <= review_date <= end_date:
            reviews.append({
                'title': title,
                'description': description,
                'date': date,
                'reviewer': reviewer,
                'rating': rating
            })
    
    return reviews

# Main function to handle inputs and generate output
def scrape_reviews(company_name, start_date, end_date, source='G2'):
    # Validate input dates
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return
    
    # Scrape reviews based on the source
    if source.lower() == 'g2':
        reviews = scrape_g2_reviews(company_name, start_date, end_date)
    elif source.lower() == 'capterra':
        reviews = scrape_capterra_reviews(company_name, start_date, end_date)
    else:
        print("Error: Unsupported source. Please choose either 'G2' or 'Capterra'.")
        return
    
    # Output the reviews to a JSON file
    with open(f'{company_name}_reviews.json', 'w') as json_file:
        json.dump(reviews, json_file, indent=4)
    
    print(f"Reviews saved to {company_name}_reviews.json")

# Example usage
scrape_reviews('salesforce-salesforce-sales-cloud', '2023-01-01', '2023-12-31', 'G2')
