from pydantic import BaseModel, Field

class InputURL(BaseModel):
    """
    入力URLのストア
    """
    url: str = Field(description="URL", default="")

    def update(self, url: str):
        """
        URLを更新
        """
        self.url = url

# Singleton
input_url = InputURL()