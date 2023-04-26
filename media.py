from PIL import Image, ImageDraw, ImageFont

import config


def dict_to_table(data, filename):
    # 设置表格样式
    font_size = 16
    cell_height = 30  # 标题高
    row_height = 30  # 行高
    line_color = (128, 128, 128)  # 文字颜色
    bg_color = (255, 255, 255)  # 背景颜色

    # 定义表头和列宽
    header = ['任务ID', '发送对象', '发送方式', '下一次触发时间', '创建时间', '发送内容']
    header_width = [100, 100, 100, 200, 200, 300]

    # 计算表格的总宽度和高度
    table_width = sum(header_width) + 5
    table_height = (len(data) + 1) * cell_height + 5

    # 创建一张白色背景的图片
    img = Image.new('RGB', (table_width, table_height), color='white')

    # 获取画笔
    draw = ImageDraw.Draw(img)

    # 设置字体
    font = ImageFont.truetype(config.conf().get("ttf"), size=font_size, encoding="unic")

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

if __name__ == '__main__':
    pass