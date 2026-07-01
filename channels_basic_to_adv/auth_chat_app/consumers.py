from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AuthConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        print("=" * 50)

        print("Type :", self.scope["type"])
        print("Path :", self.scope["path"])
        print(self.scope["user"].id)
        username = self.scope["user"].username
        print(username)
        print(self.scope["user"].first_name)
        print(self.scope["user"].first_name)
        print(self.scope["user"].last_name)
        print("User :", self.scope["user"])
        print(self.scope["user"].email)
        print("Cookies :", self.scope["cookies"])
        print("Session :", self.scope["session"])
        print("URL Route :", self.scope.get("url_route"))

        print("=" * 50)

        print("="*50)

        print("User :",self.scope["user"])

        print("Authenticated :",self.scope["user"].is_authenticated)

        print("="*50)

        if not self.scope["user"].is_authenticated:

            print("Connection Rejected")

            await self.close()

            return

        await self.accept()

        await self.send(
            text_data=json.dumps({
                "message":"Welcome "+self.scope["user"].username
            })
        )

    async def disconnect(self,close_code):

        print("Disconnected")