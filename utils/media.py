from PIL import Image, ImageDraw, ImageFont

from utils import config
from utils.log_utils import log
import urllib


def dict_to_table(data, filename, header, header_width):
    # 设置表格样式
    font_size = 16
    cell_height = 30  # 标题高
    row_height = 30  # 行高
    line_color = (128, 128, 128)  # 文字颜色
    bg_color = (255, 255, 255)  # 背景颜色

    # 计算表格的总宽度和高度
    table_width = sum(header_width) + 5
    table_height = (len(data) + 1) * cell_height + 5

    # 创建一张白色背景的图片
    img = Image.new('RGB', (table_width, table_height), color='white')

    # 获取画笔
    draw = ImageDraw.Draw(img)

    # 设置字体
    font = ImageFont.truetype(config.get("ttf"), size=font_size, encoding="unic")

    # 画表头
    x, y = 0, 0
    for i in range(len(header)):
        draw.rectangle((x, y, x + header_width[i], y + cell_height), outline='black', width=1, fill=line_color)
        draw.text((x + 5, y + 3), header[i], font=font, fill=bg_color)
        x += header_width[i]

    # 画数据
    y += row_height
    for i in range(len(data)):
        x = 0
        for j in range(len(header)):
            draw.rectangle((x, y, x + header_width[j], y + row_height), outline='black', width=1, fill=bg_color)
            draw.text((x + 5, y + 3), str(data[i][header[j]]), font=font, fill=line_color)
            x += header_width[j]
        y += row_height

        # 将生成的图片保存到本地文件
        img.save(filename)
        # img.show()


def get_img_media_id_by_url(img_url, img_file_name):
    """
    * 上传临时素菜
    * 1、临时素材media_id是可复用的。
    * 2、媒体文件在微信后台保存时间为3天，即3天后media_id失效。
    * 3、上传临时素材的格式、大小限制与公众平台官网一致。
    """
    resource = urllib.request.urlopen(img_url)
    f_name = img_file_name
    with open(f_name, 'wb') as f:
        f.write(resource.read())
    return get_img_media_id(r"./img_media.jpg")


def get_img_media_id(robot, img_file_name):
    media_json = robot.client.upload_media("image", open(img_file_name, "rb"))  ## 临时素材
    # media_json = myRobot.client.upload_permanent_media("image", open(r"./img_media.jpg", "rb")) ##永久素材
    media_id = media_json['media_id']
    # media_url = media_json['url']
    log.debug(f'微信素材id={media_id}, file_name={img_file_name}')
    return media_id


if __name__ == '__main__':
    pass
