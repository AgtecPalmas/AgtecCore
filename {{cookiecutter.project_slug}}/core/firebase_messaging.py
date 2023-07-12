import json

import requests
from django.conf import settings

MSG_REGISTRO_EXISTENTE = "{0} já cadastrado no sistema."


class FirebaseCloudMessage:
    def __init__(self, device=None, *args, **kwargs):
        super(FirebaseCloudMessage, self).__init__(*args, **kwargs)
        self.key = settings.FCM_KEY
        self.device = device

    def send(self, title: str, message: str) -> bool:
        """Método para enviar as mensagens de notificação para os usuário

        Parameters
        ----------
        title: str
            Título da mensagem enviada via Push Notification
        message: str
            Mensagem enviada via Push Notification

        Returns
        -------
        bool
            True para se a mensagem tiver sido enviada com sucesso.
            False para se a mensagem tiver não tiver sido enviada.
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"key={self.key}",
            }

            body = {
                "notification": {"title": title, "body": message},
                "to": self.device,
                "priority": "high",
            }

            response = requests.post(
                "https://fcm.googleapis.com/fcm/send",
                headers=headers,
                data=json.dumps(body),
            )

            if response.status_code == 200:
                result = response.json()

                if result is not None:
                    if result["success"] == 1:
                        return True

                    if result["failure"] == 1:
                        return False

            return response.status_code == 200

        except Exception as error:
            return False
