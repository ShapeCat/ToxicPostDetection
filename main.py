import os
from vk_mod.api import VK_API
from pathlib import Path
from vk_mod.models.post_classifier import predict_from_url, load_model
from vk_mod.utils.environment import load_config


PREDICTION_TRESH = 0.5
model_path = Path("./models/model.keras")
config_file = Path("./config-dev.ini")


notification_template = '''
Обнаружено потенциальное нарушение
{separator}
Ссылка на пост:
https://vk.com/wall-{group_id}_{post_id}
Id Автора: {author_name} ({author_link})
Текст: {post_data}
Процет уверенности: {confidence}%
{separator}
'''

status_check_template = '''
{separator}
Статус сервера: {status}
Статус отслеживания: {longpoll_status}

Отследиваемое сообщество: {community_name} ({community_link})
Администрация сообщества: {admin_name} ({admin_link})

Ключ сообщества: {community_key}
Ключ администратора: {admin_key}
{separator}
'''


def load_tokens_from_env(config_file:os.PathLike) -> tuple[str, str, str, str]:
    access_token = load_config("ApiKeys", "ACCESS_TOKEN", file_path=config_file)
    community_key = load_config("ApiKeys", "COMMUNITY_KEY", file_path=config_file)
    community_id = load_config("CommunutyInfo", "COMMUNITY_ID", file_path=config_file)
    adminId = load_config("AdminId", "ADMIN_ID", file_path=config_file)
    return access_token, community_id, adminId, community_key


def check_post(model, post_data:dict) -> float:
    text = post_data.get('text', "")
    attachments = post_data.get('attachments', []) 
    photos = [attachment for attachment in attachments if attachment.get("type", "") == "photo"]
    predictions:list[float] = [] 
    if (len(photos) > 0):
        for image in photos:
            if (image['type'] == 'photo'):    
                photo_url = image['photo']['orig_photo']['url']
                predictions.append(round(predict_from_url(model, text, photo_url), 2))                 
    else:
        predictions.append(round(predict_from_url(model, text, ""), 2))
    return max(predictions)


def validate_api_keys(api:VK_API, keys:dict[str,str], community_id:str) -> dict[str, str]:
    key_statuses = {}
    for key_name, key in keys.items():
        if not key:
            key_statuses[key_name] = "Отсутсвует"
            continue
        try:
            community_name = api.community.get_name(community_id)
            key_statuses[key_name] = "Работает" if community_name else "Ошибка"
        except:
                key_statuses[key_name] = "Ошибка"
    return key_statuses


def main():
    access_token, community_id, admin_id, community_key = load_tokens_from_env(config_file)
    model = load_model(model_path)
    vk_api = VK_API(community_key, access_token)

    for event in vk_api.longpoll.listen(community_id=community_id):
        event_type = event.get('type', None)
        event_data = event.get('object', None)
        print(event_type)

        if (event_type == 'wall_post_new'):
            prediction = check_post(model, event_data)
            if prediction > PREDICTION_TRESH:   
                vk_api.wall.delete(community_id, event_data.get("id"))
            print(prediction)

        if (event_type == "wall_reply_new"
            or event_type == "wall_reply_edit"):
            prediction = check_post(model, event_data)
            
            if prediction > PREDICTION_TRESH:
                author = event_data.get('from_id')
                vk_api.chat.send(admin_id,
                                 notification_template.format(
                                     separator='-'*100,
                                     group_id=community_id,
                                     post_id=event_data.get('id'),
                                     author_name=vk_api.user.get_name(author),
                                     author_link=vk_api.user.get_link(author),
                                     post_data=event_data.get('text'),
                                     confidence=prediction*100
                                     ))
            print(prediction)
            
        if (event_type == "message_new"):
            text = event_data.get('message').get('text')
            if (text == "Статус"):
                key_statuses = validate_api_keys(
                    vk_api,
                    {
                        "community_key": community_key,
                        "access_token": access_token
                    }, community_id)
                vk_api.chat.send(admin_id,
                                 status_check_template.format(
                                     separator='-'*100,
                                     status="OK",
                                     longpoll_status="OK",
                                     community_name=vk_api.community.get_name(community_id),
                                     community_link=vk_api.community.get_link(community_id),
                                     admin_name=vk_api.user.get_name(admin_id),
                                     admin_link=vk_api.user.get_link(admin_id),
                                     community_key=key_statuses["community_key"],
                                     admin_key=key_statuses["access_token"]
                                     ))


if __name__ == "__main__":
    main()