import os
import time

from config import params
from logger_settings import logger
from fb_selenium_client import FaceBookClient


def login_fb() -> FaceBookClient:
    fb_client = FaceBookClient(
        username=params.username,
        password=params.password,
        hidden=True,
        driver_path=params.chrome_driver_path)

    logger.info("Login Facebook ...")
    login_status = fb_client.login_facebook()
    logger.info(f"Login status: {login_status}")

    return fb_client


def save_users_id_from_liked_post(fb_client: FaceBookClient, post_url: str, name_file: str):
    """
    Get List with ID users, who liked post_url
    """

    try:
        fb_client.driver.get(post_url)
        logger.info(f"Open page {post_url}")
        if fb_client.save_html_page_users_who_likes_post(name_file):
            users_id = fb_client.get_all_liked_person_links(name_file)

            if users_id:
                return users_id

        return False

    except Exception as ex:
        logger.error(f"Catch mistake during work 'save_users_id_from_liked_post': {ex}")
        return False


def main():
    fb_client = login_fb()
    # 'https://www.facebook.com/groups/sarcasmandmemes'
    fb_client.driver.get('https://www.facebook.com/groups/sarcasmandmemes')#'https://www.facebook.com/groups/2610322019099604')
    status = fb_client.save_html_page_with_all_posts(os.path.join(params.temp_dir, 'NEW_DATA_12_53.html'))
    logger.info(f"Status save page: {status}")

    # fb_client.driver.get(
    #     'https://www.facebook.com/photo/?fbid=122115821234114931&set=gm.995798404817743&idorvanity=216436106087314')
    # # fb_client.while_not_xpath('//*[@aria-label="Join group"]', wait=5)
    # logger.info('Open Site')
    # fb_client.get_users_who_likes_post()
    logger.info('Close After 3 seconds ...')
    time.sleep(3)
    fb_client.driver.quit()
    #


def test():
    fb_client = FaceBookClient(
        username=params.username,
        password=params.password,
        hidden=False,
        driver_path=params.chrome_driver_path)

    fb_client.login_facebook()
    fb_client.driver.get('https://www.facebook.com/groups/2610322019099604')
    time.sleep(5)
    fb_client.save_current_page(os.path.join(params.temp_dir, 'TEST_12_47.html'))
    fb_client.get_all_posts_links(os.path.join(params.temp_dir, 'TEST_12_47.html'))


if __name__ == "__main__":
    # main()
    # test()

    fb_client = FaceBookClient(
        username=params.username,
        password=params.password,
        hidden=False,
        driver_path=params.chrome_driver_path)
        # chrome_location_path=r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')

    fb_client.driver.get('https://2ip.ru/')
    time.sleep(3)

    fb_client.login_facebook()
    fb_client.driver.get('https://www.facebook.com/groups/abatterwaytofarm')
    time.sleep(20)


# 'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z' ссылка на пост без фото
