from pinterest_scraper import PinterestScraper

# Define query for searching images
pattern_scraper = PinterestScraper("wavy pattern")
pattern_scraper.run()

# or scrape your own pinterest board
#pattern_scraper = PinterestScraper("user_name","board_name")
#pattern_scraper.run()