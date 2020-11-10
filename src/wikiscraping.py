import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4


def get_char_info(name: str, target="all"):
    list_url = "https://revuestarlight.boom-app.wiki/entry/chara-list"
    res = requests.get(list_url)
    soup = bs4(res.content, 'html.parser')

    character_name = [
        tag["alt"].replace(" ", "") for tag in soup.select("a img[width='60']")
    ]
    detail_url = [
        tag.parent["href"] for tag in soup.select("a img[width='60']")
    ]
    name_url = dict(zip(character_name, detail_url))

    char_info = parse_char_info(name_url[name.replace(" ", "")])

    target_columns = {
        "all": ["基本情報", "最大ステ", "アクト性能", "スキル性能", "アクセ付き", "アクセ付きステ"],
        "act": ["アクト性能", "アクセ付き"],
        "skill": ["スキル性能"],
        "status": ["最大ステ", "アクセ付ステ"]
    }
    target = target_columns[target]
    detail_url_base = "https://revuestarlight.boom-app.wiki"
    return (char_info.query("category in @target"),
            detail_url_base + name_url[name.replace(" ", "")])


def parse_char_info(char_url: str):
    detail_url_base = "https://revuestarlight.boom-app.wiki"
    url = detail_url_base + char_url

    tables = pd.read_html(url)
    if len(tables) > 10:
        # アクセありキャラ
        target_table_idx = [0, 2, 4, 5, 6, 8, 9, 3]
    else:
        # アクセなしキャラ3
        target_table_idx = [0, 2, 3, 4, 5, 7]
    target_table = [tables[i] for i in target_table_idx]

    i = 0
    detail_info = target_table[i]
    detail_info["category"] = "基本情報"
    detail_info.columns = ["key", "value", "category"]
    detail_info = detail_info.reindex(["category", "key", "value"], axis=1)

    i += 1
    tmp = pd.DataFrame({"category": "最大ステ"}, index=range(len(target_table[i])))
    tmp["key"] = target_table[i].iloc[0:, 0]
    tmp["value"] = (target_table[i].iloc[0:, 1].astype(str)) + "(" + (
        target_table[i].iloc[0:, 2]) + ")"
    detail_info = pd.concat([detail_info, tmp])

    i += 1
    tmp = pd.DataFrame({"category": "アクト性能"},
                       index=range(len(target_table[i])))
    tmp["key"] = "Act" + pd.Series([str(i) for i in range(1, 4)])
    tmp["value"] = target_table[i].iloc[0:, 1] + target_table[i].iloc[
        0:, 0] + "(Hit数" + (target_table[i].iloc[0:, 2]).astype(str) + ")"
    detail_info = pd.concat([detail_info, tmp])

    i += 1
    tmp = pd.DataFrame({"category": "アクト性能"},
                       index=range(len(target_table[i])))
    tmp["key"] = "クライマックス"
    tmp["value"] = target_table[i].iloc[0:, 1] + target_table[i].iloc[
        0:, 0] + "(Hit数" + (target_table[i].iloc[0:, 2]).astype(str) + ")"
    detail_info = pd.concat([detail_info, tmp])

    i += 1
    tmp = pd.DataFrame({"category": "スキル性能"},
                       index=range(len(target_table[i])))
    tmp["key"] = "オートスキル" + pd.Series([str(i) for i in range(1, 4)])
    tmp["value"] = target_table[i].iloc[0:, 1]
    detail_info = pd.concat([detail_info, tmp])

    i += 1
    tmp = pd.DataFrame({"category": "スキル性能"}, index=[1])
    tmp["key"] = "ユニットスキル"
    tmp["value"] = target_table[i].iloc[0, 1] + target_table[i].iloc[1, 1]
    detail_info = pd.concat([detail_info, tmp])

    if len(tables) > 10:
        i += 1
        tmp = pd.DataFrame({"category": "アクセ付"}, index=[1])
        tmp["key"] = "アクト"
        tmp["value"] = target_table[i].iloc[0, 1] + "(Hit数" + (
            target_table[i].iloc[0, 2]).astype(str) + ")"
        detail_info = pd.concat([detail_info, tmp])
        i += 1
        tmp = pd.DataFrame({"category": "アクセ付ステ"},
                           index=range(len(target_table[i])))
        tmp["key"] = target_table[i].iloc[0:, 0]
        tmp["value"] = (target_table[i].iloc[0:, 1].astype(str))
        detail_info = pd.concat([detail_info, tmp])

    return (detail_info)
