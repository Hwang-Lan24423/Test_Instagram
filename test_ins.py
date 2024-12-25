from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import unittest


class Instagram(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=D:\\WorkSpace\\Python\\profile")  # change path to folder profile
        print("Initializing ChromeDriver...")
        self.driver = webdriver.Chrome(options=options)
        print("Opening Instagram login page...")
        self.driver.get("https://www.instagram.com/accounts/login/")
        self.driver.implicitly_wait(30)
        print("Instagram login page opened.")

    def test_tym_post(self):
        link_post = self.link_post
        print(f"Navigating to post: {link_post}")
        self.driver.get(f'https://www.instagram.com/p/{link_post}/')
        self.driver.implicitly_wait(30)
        time.sleep(5)  # Increased wait time
        print("Checking like status...")
        checklike = self.driver.find_element(By.XPATH, "//*[@fill='currentColor' and @height='24' and (@aria-label='Like' or @aria-label='Unlike')]").get_attribute('aria-label')
        time.sleep(5)
        print("Trạng thái:", checklike)
        if checklike.strip() == "Unlike":
            print("Bài viết đã được Like => Kết thúc tiến trình")
            return
        elif checklike.strip() == "Like":
            print("Bài viết chưa được Like => Tiến hành Like")
            self.driver.find_element(By.XPATH, '//span[@class="xp7jhwk"]').click()
            time.sleep(5)  # Increased wait time
            checklike = self.driver.find_element(By.XPATH, "//*[@fill='currentColor' and @height='24' and (@aria-label='Like' or @aria-label='Unlike')]").get_attribute('aria-label')
            time.sleep(5)
            print("Trạng thái sau khi Like:", checklike)
            if checklike.strip() == "Unlike":
                self.assertEqual(checklike, "Unlike")
                print("Like bài viết thành công => Passed")
            else:
                print("Like bài viết thất bại => Failed")

    def test_cmt_post(self):
        user = self.user
        link_post = self.link_post
        content = self.content
        self.driver.implicitly_wait(30)
        print(f"Navigating to post: {link_post}")
        self.driver.get(f'https://www.instagram.com/p/{link_post}/')
        self.driver.implicitly_wait(30)
        print("Adding comment...")
        self.driver.find_element(By.XPATH, "//textarea[contains(@aria-label,'Add a comment…')]").send_keys(f"{content}")
        time.sleep(5)  # Increased wait time
        try:
            self.driver.find_element(By.XPATH, '//div[@class="_aidp"]').click()
        except:
            print("Retrying to find the comment button...")
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//div[@class="_aidp"]').click()
        time.sleep(5)  # Increased wait time
        us = self.driver.find_element(By.XPATH, f'//span[div="{user}"]/div/a/div/div/span').text
        cont = self.driver.find_element(By.XPATH, f'//div[span="{content}"]/span').text
        # lấy all cmt
        a = self.driver.find_element(By.XPATH, '//div[@class="x78zum5 xdt5ytf x1iyjqo2"]').text
        # print(a.split("Reply"))
        for cmt in a.split("Reply"):
            if us in cmt and cont in cmt:
                print(cmt)
                self.assertEqual(cont, content)
                print(f"Tồn tại User: {us} và bình luận: {cont} => Passed")
                return

    def test_follow_user(self):
        user_profile = self.user_profile
        print(f"Navigating to user profile: {user_profile}")
        self.driver.get(f'https://www.instagram.com/{user_profile}/')
        self.driver.implicitly_wait(30)
        time.sleep(5)  # Increased wait time
        print("Checking follow status...")
        follow_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Follow') or contains(text(), 'Following')]")
        follow_status = follow_button.text
        print("Trạng thái:", follow_status)
        if follow_status == "Following":
            print("User đã được Follow => Kết thúc tiến trình")
            return
        elif follow_status == "Follow":
            print("User chưa được Follow => Tiến hành Follow")
            follow_button.click()
            time.sleep(5)  # Increased wait time
            follow_status = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Following')]").text
            print("Trạng thái sau khi Follow:", follow_status)
            if follow_status == "Following":
                self.assertEqual(follow_status, "Following")
                print("Follow user thành công => Passed")
            else:
                print("Follow user thất bại => Failed")

    def test_unfollow_user(self):
        user_profile = self.user_profile
        print(f"Navigating to user profile: {user_profile}")
        self.driver.get(f'https://www.instagram.com/{user_profile}/')
        self.driver.implicitly_wait(30)
        time.sleep(5)  # Increased wait time
        print("Checking follow status...")
        follow_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Follow') or contains(text(), 'Following')]")
        follow_status = follow_button.text
        print("Trạng thái:", follow_status)
        if follow_status == "Follow":
            print("User chưa được Follow => Kết thúc tiến trình")
            return
        elif follow_status == "Following":
            print("User đã được Follow => Tiến hành Unfollow")
            follow_button.click()
            time.sleep(5)  # Increased wait time
            unfollow_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Unfollow')]")
            unfollow_button.click()
            time.sleep(5)  # Increased wait time
            follow_status = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Follow')]").text
            print("Trạng thái sau khi Unfollow:", follow_status)
            if follow_status == "Follow":
                self.assertEqual(follow_status, "Follow")
                print("Unfollow user thành công => Passed")
            else:
                print("Unfollow user thất bại => Failed")

    # def test_search(self):
    #     search_query = self.search_query
    #     print(f"Searching for: {search_query}")
    #     self.driver.get("https://www.instagram.com/")
    #     self.driver.implicitly_wait(30)
    #     time.sleep(5)  # Increased wait time
    #     search_box = self.driver.find_element(By.XPATH, "//input[@placeholder='Search']")
    #     search_box.send_keys(search_query)
    #     time.sleep(5)  # Increased wait time
    #     search_box.send_keys(Keys.RETURN)
    #     time.sleep(5)  # Increased wait time
    #     search_box.send_keys(Keys.RETURN)
    #     time.sleep(5)  # Increased wait time
    #     print("Search results displayed")
    #     # Add assertions or further checks as needed

    def tearDown(self):
        print("Closing browser...")
        self.driver.close()


if __name__ == "__main__":
    Instagram.link_post = 'DC9o_1QxzHL'
    Instagram.content = "Hello bro"
    Instagram.user = "hlanz_03"
    Instagram.user_profile = ""  # Replace with the actual user profile to test
    #Instagram.search_query = "example_search"  # Replace with the actual search query to test
    unittest.main()