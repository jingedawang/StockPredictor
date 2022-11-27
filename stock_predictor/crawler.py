from playwright.sync_api import sync_playwright

import constants


class Crawler:
    """
    Web crawler for stock list.

    Use playwright to download the stock list from the official websites of Shanghai Stock Exchange and Shenzhen Stock Exchange.
    """

    def __init__(self) -> None:
        """
        Initialize the Playwright engine and do some prerequisite works.
        """
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context()
        self.context.add_init_script(
            # Following JavaScript code sets navigator.webdriver to false during page initialization to avoid
            # anti-crawler.
            """
            navigator.webdriver = false
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            })
            """
        )

    def __enter__(self):
        """
        Do nothing when entering the crawler context.
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the resources when exiting from the crawler context.
        """
        self.close()
    
    def reset(self):
        """
        Reset the crawler to re-initialize the browser and context.
        """
        self.context.close()
        self.context = self.browser.new_context()
        self.context.add_init_script(
            # Following JavaScript code sets navigator.webdriver to false during page initialization to avoid
            # anti-crawler.
            """
            navigator.webdriver = false
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            })
            """
        )
    
    def close(self):
        """
        Close the browser and playwright objects.
        """
        self.browser.close()
        self.playwright.stop()
    
    def crawl_shanghai_stock_list(self, save_path: str):
        """
        Crawl the stock list Excel file from Shanghai Stock Exchange.
        """
        page = self.context.new_page()
        page.goto(constants.SHANGHAI_STOCK_EXCHANGE_URL)
        with page.expect_download() as download_info:
            page.click('.tableDownload')
        download_info.value.save_as(save_path)
        page.close()

    def crawl_shenzhen_stock_list(self, save_path: str):
        """
        Crawl the stock list Excel file from Shenzhen Stock Exchange.
        """
        page = self.context.new_page()
        page.goto(constants.SHENZHEN_STOCK_EXCHANGE_URL)
        with page.expect_download() as download_info:
            page.click('.btn-default-excel')
        download_info.value.save_as(save_path)
        page.close()