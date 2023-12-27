from file_utils import load_files, save_to_json_file
from soup_utils import SoupHelper, get_value_by_content_and_selector
from model import ChessInformation, DataInformation, DataEncoder, \
    PhoneInformation, StarInformation, ClothingInformation, JigsawInformation, AngleGrinderInformation
from cast_utils import cast_int, cast_float, cast_bool
from stat_utils import calculate_stat, calculate_frequency
from text_utils import substring_with_regex, exclude_substring, get_value_from_substring, \
    get_value_from_substring_with_exclude


def parse_html_with_chess_information(html: str):
    helper = SoupHelper(html)
    chess_info = ChessInformation()
    chess_info.type = helper.get_substring_value_by_selector("div.chess-wrapper div span")
    chess_info.tournament = helper.get_substring_value_by_selector("h1.title")
    chess_info.city = helper.parse_value_by_selector("p.address-p",
                                                     lambda item: get_value_from_substring_with_exclude(item, ':',
                                                                                                        'Начало', 1))
    chess_info.date = helper.parse_value_by_selector("p.address-p", lambda item: get_value_from_substring(item, ':'))
    chess_info.round_count = cast_int(helper.get_substring_value_by_selector("span.count"))
    chess_info.time_control = helper.get_substring_value_by_selector("span.year")
    chess_info.min_rating = cast_int(helper.get_substring_value_by_selector("span.year + span"))
    chess_info.url_img = helper.get_value_attr_by_selector("img", "src")
    chess_info.rating = cast_float(
        helper.get_substring_value_by_selector("div.chess-wrapper div:last-child span:first-child"))
    chess_info.count_view = cast_int(
        helper.get_substring_value_by_selector("div.chess-wrapper div:last-child span:last-child"))
    return chess_info


def parse_html_with_phone_information(html: str):
    helper = SoupHelper(html)
    phone_info = PhoneInformation()
    phone_info.id = cast_int(helper.get_value_attr_by_selector("a[data-id]", "data-id"))
    phone_info.model = helper.get_value_by_selector("div.product-item span")
    phone_info.screen_size_inch = cast_float(substring_with_regex(phone_info.model, r'^.*"', '"'))
    phone_info.memory_storage_gb = cast_int(substring_with_regex(phone_info.model, r'\d*GB', 'GB'))
    phone_info.price_rub = cast_int(helper.parse_value_by_selector("price",
                                                                   lambda raw: exclude_substring("₽", raw)))
    phone_info.bonus = helper.get_num_value_by_selector("strong")
    phone_info.processor = helper.get_value_by_selector('li[type="processor"]')
    phone_info.ram_gb = helper.get_num_value_by_selector('li[type="ram"]')
    phone_info.count_sim = helper.get_num_value_by_selector('li[type="sim"]')
    phone_info.matrix = helper.get_value_by_selector('li[type="matrix"]')
    phone_info.resolution = helper.get_value_by_selector('li[type="resolution"]')
    phone_info.size_camera_mp = helper.get_num_value_by_selector('li[type="camera"]')
    phone_info.acc_mah = helper.get_num_value_by_selector('li[type="acc"]')
    return phone_info


def parse_html_with_phone_information_list(html: str) -> list:
    helper = SoupHelper(html)
    elements = helper.get_elements_by_selector("div.pad")
    return list(map(lambda item: parse_html_with_phone_information(str(item)), elements))


def parse_xml_with_star_information(xml: str) -> StarInformation:
    helper = SoupHelper(xml, 'xml')
    star_info = StarInformation()
    star_info.name = helper.get_value_by_selector('name')
    star_info.constellation = helper.get_value_by_selector('constellation')
    star_info.spectral_class = helper.get_value_by_selector('spectral-class')
    star_info.radius = cast_int(helper.get_value_by_selector('radius'))
    star_info.rotation_day = helper.get_float_num_value_by_selector('rotation')
    star_info.age_b_years = helper.get_float_num_value_by_selector('age')
    star_info.distance_m_km = helper.get_float_num_value_by_selector('distance')
    star_info.absolute_magnitude_m_km = helper.get_float_num_value_by_selector('absolute-magnitude')
    return star_info


def parse_xml_with_clothing_information_list(xml: str) -> list:
    helper = SoupHelper(xml, 'xml')
    elements = helper.get_elements_by_selector("clothing")
    return list(map(lambda item: parse_xml_with_clothing_information(str(item)), elements))


def parse_xml_with_clothing_information(xml: str) -> ClothingInformation:
    helper = SoupHelper(xml, 'xml')
    clothing_info = ClothingInformation()
    clothing_info.id = cast_int(helper.get_value_by_selector('id'))
    clothing_info.name = helper.get_value_by_selector('name')
    clothing_info.category = helper.get_value_by_selector('category')
    clothing_info.size = helper.get_value_by_selector('size')
    clothing_info.color = helper.get_value_by_selector('color')
    clothing_info.material = helper.get_value_by_selector('material')
    clothing_info.price = cast_int(helper.get_value_by_selector('price'))
    clothing_info.rating = cast_float(helper.get_value_by_selector('rating'))
    clothing_info.reviews = cast_int(helper.get_value_by_selector('reviews'))
    clothing_info.new = cast_bool(helper.get_value_by_selector('new'), '+', '-')
    clothing_info.exclusive = cast_bool(helper.get_value_by_selector('exclusive'), 'yes', 'no')
    clothing_info.sporty = cast_bool(helper.get_value_by_selector('sporty'), 'yes', 'no')
    return clothing_info


def parse_html_with_jigsaw_information(html: str) -> JigsawInformation:
    helper = SoupHelper(html)
    jigsaw_information = JigsawInformation()
    jigsaw_information.name = helper.get_value_by_selector('h1[data-qa="get-product-title"]')
    jigsaw_information.price = cast_int(helper.get_value_attr_by_selector('meta[itemprop="price"]', 'content'))
    items = helper.get_elements_by_selector('div[data-qa="specification-item"]')
    items_str = list(map(lambda item: str(item), items))
    jigsaw_information.type = get_value_by_content_and_selector(items_str,
                                                                'Тип',
                                                                'span[itemprop="value"]',
                                                                lambda helper, selector: helper.get_value_by_selector(
                                                                    selector))
    jigsaw_information.power_wt = get_value_by_content_and_selector(items_str,
                                                                    'Мощность',
                                                                    'span[itemprop="value"]',
                                                                    lambda helper,
                                                                           selector: helper.get_num_value_by_selector(
                                                                        selector))
    jigsaw_information.net_weight = get_value_by_content_and_selector(items_str,
                                                                      'Вес нетто',
                                                                      'span[itemprop="value"]',
                                                                      lambda helper,
                                                                             selector: helper.get_float_num_value_by_selector(
                                                                          selector))
    jigsaw_information.max_cutting_thickness_wood_mm = get_value_by_content_and_selector(items_str,
                                                                                         'Мах толщина пропила (дерево)',
                                                                                         'span[itemprop="value"]',
                                                                                         lambda helper,
                                                                                                selector: helper.get_num_value_by_selector(
                                                                                             selector))
    jigsaw_information.max_cutting_thickness_metal_mm = get_value_by_content_and_selector(items_str,
                                                                                          'Мах толщина пропила (металла)',
                                                                                          'span[itemprop="value"]',
                                                                                          lambda helper,
                                                                                                 selector: helper.get_num_value_by_selector(
                                                                                              selector))
    jigsaw_information.pendulum_stroke = cast_bool(get_value_by_content_and_selector(items_str,
                                                                                     'Маятниковый ход',
                                                                                     'span[itemprop="value"]',
                                                                                     lambda helper,
                                                                                            selector: helper.get_value_by_selector(
                                                                                         selector)), 'да', 'нет')
    jigsaw_information.handle_shape = get_value_by_content_and_selector(items_str,
                                                                        'Форма ручки',
                                                                        'span[itemprop="value"]',
                                                                        lambda helper,
                                                                               selector: helper.get_value_by_selector(
                                                                            selector))
    jigsaw_information.saw_stroke_mm = get_value_by_content_and_selector(items_str,
                                                                         'Ход пилки',
                                                                         'span[itemprop="value"]',
                                                                         lambda helper,
                                                                                selector: helper.get_num_value_by_selector(
                                                                             selector))
    return jigsaw_information


def parse_html_with_angle_grinder_information_list(html):
    helper = SoupHelper(html)
    elements = helper.get_elements_by_selector('div[data-qa="products-tile-horizontal"]')
    return list(map(lambda item: parse_html_with_angle_grinder_information(str(item)), elements))


def parse_html_with_angle_grinder_information(html):
    helper = SoupHelper(html)
    angle_grinder_info = AngleGrinderInformation()
    angle_grinder_info.name = helper.get_value_attr_by_selector('a[data-qa="product-name"]', 'title')
    angle_grinder_info.price = helper.get_num_value_by_selector('p[data-qa="product-price-current"]')
    angle_grinder_info.rating = helper.get_num_value_by_selector('a[data-qa="product-rating"] span')
    angle_grinder_info.power_wt = helper.get_num_value_by_selector('ul li:nth-child(1) span')
    angle_grinder_info.disk_diameter_mm = helper.get_num_value_by_selector('ul li:nth-child(2) span')
    angle_grinder_info.rpm = helper.get_value_by_selector('ul li:nth-child(3) span')
    angle_grinder_info.maintaining_constant_rpm_under_load = cast_bool(
        helper.get_value_by_selector('ul li:nth-child(4) span'), 'да', 'нет')
    angle_grinder_info.connect_vacuum_cleaner = cast_bool(helper.get_value_by_selector('ul li:nth-child(5) span'), 'да',
                                                          'нет')
    angle_grinder_info.smooth_start = cast_bool(helper.get_value_by_selector('ul li:nth-child(6) span'), 'да', 'нет')
    angle_grinder_info.net_weight = helper.get_float_num_value_by_selector('ul li:nth-child(7) span')
    return angle_grinder_info


def parse_html_task_1():
    files_as_str = load_files('1_zip_var_51')
    chess_information_list = list(map(lambda html: parse_html_with_chess_information(html), files_as_str))
    sorted_chess_information_list = sorted(chess_information_list, key=lambda item: item.rating, reverse=True)
    filtered_chess_information_list = list(filter(lambda item: 2200 < item.min_rating < 2300,
                                                  chess_information_list))
    stat = calculate_stat("count_view", lambda item: item.count_view, chess_information_list)
    frequency = calculate_frequency("type", lambda item: item.type, chess_information_list)
    result = DataInformation(chess_information_list, sorted_chess_information_list,
                             filtered_chess_information_list, stat, frequency)
    save_to_json_file(result, DataEncoder, "task_1_answer.json")


def parse_html_task_2():
    files_as_str = load_files('2_zip_var_51')
    phone_information_list = map(lambda html: parse_html_with_phone_information_list(html), files_as_str)
    phone_information_flat_list = sum(phone_information_list, [])
    sorted_data = sorted(phone_information_flat_list, key=lambda item: item.price_rub, reverse=True)
    filtered_data = list(filter(lambda item: (item.count_sim is not None and item.count_sim == 2) and
                                             (item.ram_gb is not None and item.ram_gb > 8),
                                phone_information_flat_list))
    stat = calculate_stat("price_rub", lambda item: item.price_rub, phone_information_flat_list)
    frequency = calculate_frequency("matrix", lambda item: item.matrix, phone_information_flat_list)
    result = DataInformation(phone_information_flat_list, sorted_data, filtered_data, stat, frequency)
    save_to_json_file(result, DataEncoder, "task_2_answer.json")


def parse_xml_task_3():
    files_as_str = load_files('3_zip_var_51')
    star_information_list = list(map(lambda xml: parse_xml_with_star_information(xml), files_as_str))
    sorted_data = sorted(star_information_list, key=lambda item: item.age_b_years)
    filtered_data = list(filter(lambda item: item.constellation == 'Телец' or item.age_b_years > 3.0,
                                star_information_list))
    stat = calculate_stat("radius", lambda item: item.radius, star_information_list)
    frequency = calculate_frequency("constellation", lambda item: item.constellation, star_information_list)
    result = DataInformation(star_information_list, sorted_data, filtered_data, stat, frequency)
    save_to_json_file(result, DataEncoder, "task_3_answer.json")


def parse_xml_task_4():
    files_as_str = load_files('4_zip_var_51')
    clothing_information_list = map(lambda xml: parse_xml_with_clothing_information_list(xml), files_as_str)
    clothing_information_flat_list = sum(clothing_information_list, [])
    sorted_data = sorted(clothing_information_flat_list, key=lambda item: item.price, reverse=True)
    filtered_data = list(
        filter(lambda item: (item.new is not None and item.new) and item.rating > 4.0, clothing_information_flat_list))
    stat = calculate_stat("price", lambda item: item.price, clothing_information_flat_list)
    frequency = calculate_frequency("category", lambda item: item.category, clothing_information_flat_list)
    result = DataInformation(clothing_information_flat_list, sorted_data, filtered_data, stat, frequency)
    save_to_json_file(result, DataEncoder, "task_4_answer.json")


def parse_html_task_5_single():
    files_as_str = load_files('5_custom_single')
    jigsaw_information_list = list(map(lambda html: parse_html_with_jigsaw_information(html), files_as_str))
    sorted_data = sorted(jigsaw_information_list, key=lambda item: item.price, reverse=True)
    filtered_data = list(filter(lambda item: item.handle_shape == 'грибовидная', jigsaw_information_list))
    stat = calculate_stat("price", lambda item: item.price, jigsaw_information_list)
    frequency = calculate_frequency('handle_shape', lambda item: item.handle_shape, jigsaw_information_list)
    result = DataInformation(jigsaw_information_list, sorted_data, filtered_data, stat, frequency)
    save_to_json_file(result, DataEncoder, "task_5_single_answer.json")


def parse_html_task_5_list():
    files_as_str = load_files('5_custom_list')
    angle_grinder_information_list = map(lambda html: parse_html_with_angle_grinder_information_list(html),
                                         files_as_str)
    angle_grinder_information_flat_list = sum(angle_grinder_information_list, [])
    sorted_data = sorted(angle_grinder_information_flat_list, key=lambda item: item.price)
    filtered_data = list(filter(lambda item: (item.rating is not None and item.rating > 500)
                                             and (item.power_wt is not None and item.power_wt > 1000),
                                angle_grinder_information_flat_list))
    stat = calculate_stat("price", lambda item: item.price, angle_grinder_information_flat_list)
    frequency = calculate_frequency('power_wt', lambda item: item.power_wt, angle_grinder_information_flat_list)
    result = DataInformation(angle_grinder_information_flat_list, sorted_data, filtered_data, stat, frequency)
    save_to_json_file(result, DataEncoder, "task_5_list_answer.json")


#parse_html_task_1()
#parse_html_task_2()
# parse_xml_task_3()
parse_xml_task_4()
# parse_html_task_5_single()
# parse_html_task_5_list()
