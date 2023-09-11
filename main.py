from utils import init_driver
from selenium.webdriver.common.by import By
import time


class WyyMusicIdSpider:
    def __init__(self, userid: str, username: str, music_list_id: str, headless: bool):
        self.user_id_url = f'https://music.163.com/#/user/home?id={userid}'
        self.username = username
        self.music_list_id = music_list_id
        self.songsAll = []
        self.songs10 = []
        self.songs = []
        # 默认2页
        self.page_total = 2
        self.driver = init_driver('chrome', headless)
        self.get_all_music_id()

    def get_all_music_id(self):
        # 获取 所有歌曲id列表+名字
        self.driver.get(self.user_id_url)
        self.driver.switch_to.frame('g_iframe')
        self.driver.find_element(by=By.ID, value='songsall').click()
        self.driver.find_element(by=By.XPATH, value='*//div[@class="more"]/a[1]').click()
        self.driver.find_element(by=By.ID, value='songsall').click()
        # 获取歌id
        idList = self.driver.find_elements(by=By.XPATH, value='*//span[@class="txt"]/a')
        # 获取歌名
        nameList = self.driver.find_elements(by=By.XPATH, value='*//span[@class="txt"]/a/b')
        for music_id, name in zip(idList, nameList):
            self.songsAll.append(
                {"name": name.text,
                 "id": int(music_id.get_attribute('href').split('=')[1])})
        return self.songsAll

    def get_music_context(self):
        for one_music in self.songsAll:
            url = f'https://music.163.com/#/song?id={one_music["id"]}'
            self.driver.get(url)
            self.driver.switch_to.frame('g_iframe')
            context_total = int(
                self.driver.find_element(by=By.XPATH, value='*//div[@class="m-cmmt"]/div[3]/div/a[10]').text)
            if context_total > 4000:
                self.page_total = int(context_total / 10 * 9)
            for i in range(1, self.page_total):
                # 所有评论
                elements = self.driver.find_elements(by=By.XPATH, value='//div[@class="cnt f-brk"]')
                # 评论人a标签，从中获取userid`
                for index, element in enumerate(elements):
                    if element.text.__contains__(self.username):
                        artice = element.text.split('：')
                        sp = '\n'
                        if artice[0] == self.username:
                            # 评论时间
                            times = self.driver.find_elements(by=By.XPATH, value='//div[@class="rp"]')
                            comment = f"""{artice[1]}  时间：{times[index].text.split(sp)[0]}"""
                            f = open("comments.txt", "a+", encoding='utf-8')
                            f.seek(0)
                            strAll = f.read()
                            if strAll.__contains__(comment) is False:
                                commentAndSongName = f"""\n歌曲：{one_music["name"]}\n第{str(i)}页：{artice[1]}  时间：{times[index].text.split(sp)[0]}"""
                                f.write(commentAndSongName)
                            # 关闭打开的文件
                            f.close()
                            print(
                                f"""歌曲：{one_music["name"]}\n第{str(i)}页：{artice[1]}  时间：{times[index].text.split(sp)[0]}""")
                print(f'{i}页 结束')
                self.driver.execute_script("var q=document.documentElement.scrollTop=1000000")
                self.driver.find_element(by=By.XPATH, value='*//div[@class="m-cmmt"]/div[3]/div/a[11]').click()
            self.driver.close()


if __name__ == '__main__':
    a = WyyMusicIdSpider('278734300', '弦上有春秋--', '8260424910', True)
    a.get_music_context()
