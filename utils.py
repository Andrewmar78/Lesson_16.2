from configure import path_users_datas, path_offers_datas, path_orders_datas
import json


def get_users_all():
    """Получение списка всех пользователей из файла"""
    with open(path_users_datas, "r", encoding="utf-8") as file:
        all_users_datas = json.load(file)
    print("Полный список пользователей", all_users_datas)
    return all_users_datas


def get_orders_all():
    """Получение списка всех заказов из файла"""
    with open(path_orders_datas, "r", encoding="utf-8") as file:
        all_orders_datas = json.load(file)
    print("Полный список заказов", all_orders_datas)
    return all_orders_datas


def get_offers_all():
    """Получение списка всех предложений из файла"""
    with open(path_offers_datas, "r", encoding="utf-8") as file:
        all_offers_datas = json.load(file)
    print("Полный список предложений", all_offers_datas)
    return all_offers_datas
