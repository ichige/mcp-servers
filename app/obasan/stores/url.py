from pydantic import BaseModel, Field

class InputURL(BaseModel):
    """
    入力URLのストア
    """
    url: str = Field(description="URL", default="")
    path: str = Field(description="URL Path", default="")

    def update(self, url: str):
        """
        URLを更新
        """
        self.url = url

    def reset(self):
        """
        プロパティのリセット
        """
        self.url = ""
        self.path = ""

# Singleton
input_url = InputURL()