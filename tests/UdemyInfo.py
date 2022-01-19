from dataclasses import dataclass


@dataclass
class UdemyInfo:
    title: str
    url: str
    price: str
    headline: str

    @classmethod
    def from_dict(cls, data: dict) -> "UdemyInfo":
        return cls(
            title=data['results']['title'],
            url=data['results']['url'],
            price=data['results']['price'],
            headline=data['results']['headline']
        )
